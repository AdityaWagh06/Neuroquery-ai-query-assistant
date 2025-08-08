import unittest
import json
from app import create_app

class APITestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        
    def test_query_endpoint(self):
        """Test natural language query processing"""
        query_data = {
            'query': 'Show all employees'
        }
        
        response = self.client.post('/api/query', 
                                   data=json.dumps(query_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('sql_query', data)
        self.assertIn('results', data)
        
    def test_schema_endpoint(self):
        """Test database schema endpoint"""
        response = self.client.get('/api/schema')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('schema', data)
        
    def test_examples_endpoint(self):
        """Test examples endpoint"""
        response = self.client.get('/api/examples')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('examples', data)
        self.assertIsInstance(data['examples'], list)
        
    def test_invalid_query(self):
        """Test invalid query handling"""
        query_data = {
            'query': ''
        }
        
        response = self.client.post('/api/query',
                                   data=json.dumps(query_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        
if __name__ == '__main__':
    unittest.main()
