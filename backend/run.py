from app import create_app
import os

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting AI Query Assistant API on port {port}...")
    print("Available endpoints:")
    print("- POST /api/query - Process natural language queries")
    print("- POST /api/voice - Process voice input")
    print("- GET /api/schema - Get database schema")
    print("- POST /api/sql - Execute direct SQL queries")
    print("- GET /api/examples - Get example queries")
    print("- GET /api/health - Health check")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
