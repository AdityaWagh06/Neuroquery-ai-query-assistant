from flask import Blueprint, request, jsonify
from app.nlp_processor import NLPProcessor
from app.speech_service import SpeechService
from app.database import execute_sql_query, get_database_schema
import logging

# Create blueprint
bp = Blueprint('main', __name__)

# Initialize services
nlp_processor = NLPProcessor()
speech_service = SpeechService()

@bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Query Assistant API is running'
    })

@bp.route('/api/query', methods=['POST'])
def process_query():
    """Process natural language query and return SQL results"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Query text is required'
            }), 400
        
        query_text = data['query'].strip()
        
        if not query_text:
            return jsonify({
                'success': False,
                'error': 'Query text cannot be empty'
            }), 400
        
        # Convert natural language to SQL
        sql_query = nlp_processor.text_to_sql(query_text)
        
        # Execute SQL query
        query_result = execute_sql_query(sql_query)
        
        # Get intent classification for debugging
        intent = nlp_processor.classify_intent(query_text)
        
        return jsonify({
            'success': True,
            'original_query': query_text,
            'sql_query': sql_query,
            'intent': intent,
            'results': query_result['data'],
            'columns': query_result['columns'],
            'row_count': query_result['row_count'],
            'error': query_result['error']
        })
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@bp.route('/api/voice', methods=['POST'])
def process_voice():
    """Process voice input and return transcribed text"""
    try:
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Audio file is required'
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No audio file selected'
            }), 400
        
        # Read audio data
        audio_data = audio_file.read()
        
        # Convert speech to text
        speech_result = speech_service.audio_to_text(audio_data)
        
        if not speech_result['success']:
            return jsonify({
                'success': False,
                'error': speech_result['error']
            }), 400
        
        # Process the transcribed text as a query
        query_text = speech_result['text']
        
        # Convert to SQL and execute
        sql_query = nlp_processor.text_to_sql(query_text)
        query_result = execute_sql_query(sql_query)
        intent = nlp_processor.classify_intent(query_text)
        
        return jsonify({
            'success': True,
            'transcribed_text': query_text,
            'sql_query': sql_query,
            'intent': intent,
            'results': query_result['data'],
            'columns': query_result['columns'],
            'row_count': query_result['row_count'],
            'error': query_result['error']
        })
        
    except Exception as e:
        logging.error(f"Error processing voice input: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@bp.route('/api/schema', methods=['GET'])
def get_schema():
    """Get database schema information"""
    try:
        schema_result = get_database_schema()
        
        return jsonify({
            'success': schema_result['success'],
            'schema': schema_result['schema'],
            'error': schema_result['error']
        })
        
    except Exception as e:
        logging.error(f"Error getting schema: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@bp.route('/api/sql', methods=['POST'])
def execute_direct_sql():
    """Execute direct SQL query (for advanced users)"""
    try:
        data = request.get_json()
        
        if not data or 'sql' not in data:
            return jsonify({
                'success': False,
                'error': 'SQL query is required'
            }), 400
        
        sql_query = data['sql'].strip()
        
        if not sql_query:
            return jsonify({
                'success': False,
                'error': 'SQL query cannot be empty'
            }), 400
        
        # Basic SQL injection protection (very basic - implement proper sanitization)
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        sql_upper = sql_query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return jsonify({
                    'success': False,
                    'error': f'Dangerous SQL operation detected: {keyword}. Only SELECT queries are allowed.'
                }), 400
        
        # Execute SQL query
        query_result = execute_sql_query(sql_query)
        
        return jsonify({
            'success': True,
            'sql_query': sql_query,
            'results': query_result['data'],
            'columns': query_result['columns'],
            'row_count': query_result['row_count'],
            'error': query_result['error']
        })
        
    except Exception as e:
        logging.error(f"Error executing SQL: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@bp.route('/api/examples', methods=['GET'])
def get_query_examples():
    """Get example queries for users"""
    examples = [
        {
            'text': 'Show all employees',
            'description': 'Display all employees with their department information'
        },
        {
            'text': 'How many employees work in IT?',
            'description': 'Count employees in the IT department'
        },
        {
            'text': 'Show employees with salary greater than 70000',
            'description': 'Filter employees by salary threshold'
        },
        {
            'text': 'What is the average salary?',
            'description': 'Calculate average salary across all employees'
        },
        {
            'text': 'List employees hired after 2020',
            'description': 'Show recently hired employees'
        },
        {
            'text': 'Show all projects',
            'description': 'Display all projects in the database'
        },
        {
            'text': 'Count employees in each department',
            'description': 'Group employees by department'
        },
        {
            'text': 'Show highest paid employee',
            'description': 'Find the employee with maximum salary'
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })

@bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
