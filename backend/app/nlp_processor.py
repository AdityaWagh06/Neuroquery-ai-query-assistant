import re
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class NLPProcessor:
    def __init__(self):
        self.pipeline = None
        self.intent_patterns = {
            'select_all': [
                'show all employees',
                'list all employees',
                'get all employees',
                'display all employees',
                'show all departments',
                'list all departments',
                'get all departments',
                'show all projects',
                'list all projects',
                'get all projects'
            ],
            'select_with_condition': [
                'show employees in IT department',
                'get employees with salary greater than 50000',
                'list employees hired after 2020',
                'show employees in engineering',
                'get high salary employees',
                'find employees in marketing',
                'show recent hires',
                'list senior employees'
            ],
            'count': [
                'how many employees',
                'count employees',
                'number of employees',
                'total employees',
                'how many departments',
                'count departments',
                'how many projects',
                'count projects'
            ],
            'aggregate': [
                'average salary',
                'maximum salary',
                'minimum salary',
                'total salary',
                'sum of salaries',
                'highest paid employee',
                'lowest paid employee',
                'average employee salary'
            ],
            'join': [
                'show employees with their departments',
                'list employees and departments',
                'get employee department information',
                'show department wise employees',
                'employees with department names'
            ]
        }
        self.load_or_train_model()
        
    def preprocess_text(self, text):
        """Preprocess text for NLP"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        
        try:
            tokens = word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words]
            
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(token) for token in tokens]
            
            return ' '.join(tokens)
        except:
            # Fallback if NLTK fails
            return text
    
    def load_or_train_model(self):
        """Load existing model or train new one"""
        model_path = 'models/intent_classifier.pkl'
        
        if os.path.exists(model_path):
            try:
                self.pipeline = joblib.load(model_path)
                return
            except:
                pass
        
        # Train new model
        self.train_model()
        
    def train_model(self):
        """Train the intent classification model"""
        # Prepare training data
        training_data = []
        labels = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                processed_text = self.preprocess_text(pattern)
                training_data.append(processed_text)
                labels.append(intent)
        
        # Create pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        # Train the model
        self.pipeline.fit(training_data, labels)
        
        # Save the model
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.pipeline, 'models/intent_classifier.pkl')
        
    def classify_intent(self, text):
        """Classify the intent of the input text"""
        if not self.pipeline:
            return 'unknown'
            
        processed_text = self.preprocess_text(text)
        try:
            predicted_intent = self.pipeline.predict([processed_text])[0]
            confidence = max(self.pipeline.predict_proba([processed_text])[0])
            
            return predicted_intent if confidence > 0.3 else 'unknown'
        except:
            return 'unknown'
    
    def text_to_sql(self, text):
        """Convert natural language text to SQL query"""
        intent = self.classify_intent(text)
        text_lower = text.lower()
        
        # Extract entities from text
        entities = self.extract_entities(text_lower)
        
        sql_query = ""
        
        if intent == 'select_all':
            if 'employee' in text_lower:
                sql_query = "SELECT * FROM employees e JOIN departments d ON e.department_id = d.id"
            elif 'department' in text_lower:
                sql_query = "SELECT * FROM departments"
            elif 'project' in text_lower:
                sql_query = "SELECT * FROM projects"
            else:
                sql_query = "SELECT * FROM employees e JOIN departments d ON e.department_id = d.id"
                
        elif intent == 'select_with_condition':
            sql_query = self.build_conditional_query(text_lower, entities)
            
        elif intent == 'count':
            if 'employee' in text_lower:
                sql_query = "SELECT COUNT(*) as total_employees FROM employees"
            elif 'department' in text_lower:
                sql_query = "SELECT COUNT(*) as total_departments FROM departments"
            elif 'project' in text_lower:
                sql_query = "SELECT COUNT(*) as total_projects FROM projects"
                
        elif intent == 'aggregate':
            sql_query = self.build_aggregate_query(text_lower)
            
        elif intent == 'join':
            sql_query = "SELECT e.*, d.name as department_name FROM employees e JOIN departments d ON e.department_id = d.id"
            
        else:
            # Default fallback
            sql_query = "SELECT * FROM employees e JOIN departments d ON e.department_id = d.id LIMIT 10"
            
        return sql_query
    
    def extract_entities(self, text):
        """Extract entities like department names, salary values, etc."""
        entities = {
            'department': None,
            'salary': None,
            'date': None,
            'limit': None
        }
        
        # Department extraction
        departments = ['it', 'engineering', 'marketing', 'hr', 'sales', 'finance']
        for dept in departments:
            if dept in text:
                entities['department'] = dept.upper()
                break
        
        # Salary extraction
        salary_match = re.search(r'(\d+(?:,\d{3})*)', text)
        if salary_match and ('salary' in text or 'paid' in text):
            entities['salary'] = int(salary_match.group(1).replace(',', ''))
        
        # Year extraction
        year_match = re.search(r'(20\d{2})', text)
        if year_match:
            entities['date'] = year_match.group(1)
            
        return entities
    
    def build_conditional_query(self, text, entities):
        """Build SQL query with conditions"""
        base_query = "SELECT e.*, d.name as department_name FROM employees e JOIN departments d ON e.department_id = d.id WHERE "
        conditions = []
        
        if entities['department']:
            conditions.append(f"UPPER(d.name) = '{entities['department']}'")
        
        if entities['salary']:
            if 'greater than' in text or 'more than' in text or 'above' in text:
                conditions.append(f"e.salary > {entities['salary']}")
            elif 'less than' in text or 'below' in text:
                conditions.append(f"e.salary < {entities['salary']}")
            else:
                conditions.append(f"e.salary >= {entities['salary']}")
        
        if entities['date']:
            if 'after' in text or 'since' in text:
                conditions.append(f"strftime('%Y', e.hire_date) > '{entities['date']}'")
            elif 'before' in text:
                conditions.append(f"strftime('%Y', e.hire_date) < '{entities['date']}'")
        
        if 'recent' in text:
            conditions.append("e.hire_date >= date('now', '-2 years')")
        
        if conditions:
            return base_query + ' AND '.join(conditions)
        else:
            return "SELECT e.*, d.name as department_name FROM employees e JOIN departments d ON e.department_id = d.id"
    
    def build_aggregate_query(self, text):
        """Build aggregate SQL queries"""
        if 'average salary' in text:
            return "SELECT AVG(salary) as average_salary FROM employees"
        elif 'maximum salary' in text or 'highest' in text:
            return "SELECT MAX(salary) as maximum_salary FROM employees"
        elif 'minimum salary' in text or 'lowest' in text:
            return "SELECT MIN(salary) as minimum_salary FROM employees"
        elif 'total salary' in text or 'sum' in text:
            return "SELECT SUM(salary) as total_salary FROM employees"
        else:
            return "SELECT AVG(salary) as average_salary, MAX(salary) as max_salary, MIN(salary) as min_salary FROM employees"
