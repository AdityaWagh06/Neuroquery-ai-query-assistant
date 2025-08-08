from app import db
from app.models import Employee, Department, Project
from datetime import date, datetime
import sqlite3
import pandas as pd

def init_sample_data():
    """Initialize sample data in the database"""
    
    # Check if data already exists
    if Department.query.first():
        return
    
    # Create departments
    departments = [
        Department(name='IT', description='Information Technology Department'),
        Department(name='HR', description='Human Resources Department'),
        Department(name='Engineering', description='Software Engineering Department'),
        Department(name='Marketing', description='Marketing and Sales Department'),
        Department(name='Finance', description='Finance and Accounting Department'),
    ]
    
    for dept in departments:
        db.session.add(dept)
    
    db.session.commit()
    
    # Create employees
    employees = [
        Employee(
            first_name='John', last_name='Doe', email='john.doe@company.com',
            department_id=1, salary=75000, hire_date=date(2020, 1, 15)
        ),
        Employee(
            first_name='Jane', last_name='Smith', email='jane.smith@company.com',
            department_id=2, salary=65000, hire_date=date(2019, 3, 22)
        ),
        Employee(
            first_name='Bob', last_name='Johnson', email='bob.johnson@company.com',
            department_id=3, salary=95000, hire_date=date(2021, 6, 10)
        ),
        Employee(
            first_name='Alice', last_name='Williams', email='alice.williams@company.com',
            department_id=4, salary=70000, hire_date=date(2020, 11, 5)
        ),
        Employee(
            first_name='Charlie', last_name='Brown', email='charlie.brown@company.com',
            department_id=5, salary=80000, hire_date=date(2018, 8, 30)
        ),
        Employee(
            first_name='Diana', last_name='Davis', email='diana.davis@company.com',
            department_id=3, salary=85000, hire_date=date(2021, 2, 18)
        ),
        Employee(
            first_name='Edward', last_name='Wilson', email='edward.wilson@company.com',
            department_id=1, salary=72000, hire_date=date(2019, 12, 12)
        ),
        Employee(
            first_name='Fiona', last_name='Moore', email='fiona.moore@company.com',
            department_id=4, salary=68000, hire_date=date(2022, 4, 25)
        ),
        Employee(
            first_name='George', last_name='Taylor', email='george.taylor@company.com',
            department_id=2, salary=62000, hire_date=date(2020, 7, 8)
        ),
        Employee(
            first_name='Helen', last_name='Anderson', email='helen.anderson@company.com',
            department_id=5, salary=77000, hire_date=date(2021, 9, 14)
        ),
    ]
    
    for emp in employees:
        db.session.add(emp)
    
    db.session.commit()
    
    # Create projects
    projects = [
        Project(
            name='Web Application Redesign',
            description='Redesign the company website with modern UI/UX',
            start_date=date(2023, 1, 1),
            end_date=date(2023, 6, 30),
            budget=150000,
            status='completed'
        ),
        Project(
            name='Mobile App Development',
            description='Develop iOS and Android mobile applications',
            start_date=date(2023, 3, 15),
            end_date=date(2023, 12, 31),
            budget=200000,
            status='active'
        ),
        Project(
            name='Data Analytics Platform',
            description='Build internal data analytics and reporting platform',
            start_date=date(2023, 7, 1),
            budget=300000,
            status='active'
        ),
        Project(
            name='Customer Support System',
            description='Implement new customer support ticketing system',
            start_date=date(2022, 10, 1),
            end_date=date(2023, 2, 28),
            budget=75000,
            status='completed'
        ),
    ]
    
    for project in projects:
        db.session.add(project)
    
    db.session.commit()

def execute_sql_query(query):
    """Execute SQL query and return results"""
    try:
        # Use raw SQL execution for more flexibility
        result = db.session.execute(query)
        
        # Convert to list of dictionaries
        columns = result.keys() if hasattr(result, 'keys') else []
        rows = result.fetchall()
        
        data = []
        for row in rows:
            row_dict = {}
            for i, column in enumerate(columns):
                row_dict[column] = row[i] if i < len(row) else None
            data.append(row_dict)
        
        return {
            'success': True,
            'data': data,
            'columns': list(columns),
            'row_count': len(data),
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': [],
            'columns': [],
            'row_count': 0,
            'error': str(e)
        }

def get_database_schema():
    """Get database schema information"""
    try:
        schema_info = {
            'tables': []
        }
        
        # Get table information
        tables = ['employees', 'departments', 'projects']
        
        for table_name in tables:
            # Get column information
            result = db.session.execute(f"PRAGMA table_info({table_name})")
            columns = []
            
            for row in result.fetchall():
                columns.append({
                    'name': row[1],
                    'type': row[2],
                    'nullable': not row[3],
                    'primary_key': bool(row[5])
                })
            
            schema_info['tables'].append({
                'name': table_name,
                'columns': columns
            })
        
        return {
            'success': True,
            'schema': schema_info,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'schema': {},
            'error': str(e)
        }
