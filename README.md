# AI-Powered Database Query Assistant

A comprehensive web application that allows users to interact with databases using natural language queries and voice commands. The system uses NLP (Natural Language Processing) with Scikit-learn to convert human language into SQL queries and provides real-time results through a modern React frontend.

##  Features

### Core Functionality
- **Natural Language Processing**: Convert plain English to SQL queries using Scikit-learn
- **Voice Recognition**: Support for voice input using Web Speech API and Python SpeechRecognition
- **Real-time Query Execution**: Execute queries and display results instantly
- **Intent Classification**: AI-powered understanding of query intent
- **Interactive Results**: Clean table format with responsive design

### User Experience
- **Modern React Frontend**: Bootstrap-powered responsive UI
- **Example Queries**: Pre-built examples to help users get started
- **Database Schema Viewer**: Interactive schema exploration
- **Error Handling**: User-friendly error messages and validation
- **Real-time Feedback**: Loading states and toast notifications

### Technical Features
- **Modular Architecture**: Well-structured backend and frontend
- **RESTful API**: Clean API design with comprehensive endpoints
- **SQLite Database**: Sample database with employees, departments, and projects
- **Cross-platform**: Works on Windows, macOS, and Linux

##  Architecture

```
ai-query-assistant/
├── backend/                 # Python Flask API
│   ├── app/                # Application modules
│   │   ├── __init__.py     # Flask app factory
│   │   ├── routes.py       # API endpoints
│   │   ├── models.py       # Database models
│   │   ├── nlp_processor.py # NLP and intent classification
│   │   ├── speech_service.py # Voice recognition
│   │   └── database.py     # Database operations
│   ├── models/             # ML models storage
│   ├── data/               # Database files
│   ├── tests/              # Unit tests
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Application entry point
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   ├── styles/         # CSS styles
│   │   ├── App.js         # Main application component
│   │   └── index.js       # React entry point
│   ├── public/            # Static files
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

##  Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Frontend Requirements
- Node.js 14 or higher
- npm or yarn package manager

### System Requirements
- Microphone access (for voice input)
- Modern web browser with JavaScript enabled

##  Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-query-assistant
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env
# Edit .env with your settings if needed
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
# or
yarn install
```

##  Running the Application

### 1. Start the Backend Server

```bash
cd backend
python run.py
```

The backend API will be available at `http://localhost:5000`

Available endpoints:
- `GET /api/health` - Health check
- `POST /api/query` - Process natural language queries
- `POST /api/voice` - Process voice input
- `GET /api/schema` - Get database schema
- `POST /api/sql` - Execute direct SQL queries
- `GET /api/examples` - Get example queries

### 2. Start the Frontend Development Server

```bash
cd frontend
npm start
# or
yarn start
```

The frontend will be available at `http://localhost:3000`

### 3. Using the Application

1. **Text Queries**: Type natural language questions like:
   - "Show all employees"
   - "How many people work in IT?"
   - "Find employees with salary greater than 70000"

2. **Voice Queries**: Click the microphone button and speak your question

3. **Example Queries**: Click on pre-built examples in the sidebar

4. **Database Schema**: Explore the database structure in the schema viewer

##  Sample Database

The application comes with a pre-populated SQLite database containing:

### Tables
- **employees**: Employee information (name, email, department, salary, hire date)
- **departments**: Department details (name, description, manager)
- **projects**: Project data (name, description, dates, budget, status)

### Sample Data
- 10 employees across 5 departments
- 4 projects with different statuses
- Realistic salary and date ranges

##  NLP Features

### Intent Classification
The system recognizes various query intents:
- **select_all**: "Show all employees"
- **select_with_condition**: "Find employees in IT department"
- **count**: "How many employees are there?"
- **aggregate**: "What's the average salary?"
- **join**: "Show employees with their departments"

### Entity Extraction
Automatically extracts:
- Department names (IT, Engineering, Marketing, etc.)
- Salary ranges and comparisons
- Date ranges and filters
- Numeric limits and thresholds

### Machine Learning Model
- **Algorithm**: Naive Bayes with TF-IDF vectorization
- **Training Data**: Built-in patterns for common queries
- **Features**: N-gram analysis, stop word removal, lemmatization
- **Accuracy**: Continuously improved through pattern matching

##  Voice Recognition

### Supported Features
- Real-time speech-to-text conversion
- Google Web Speech API integration
- Noise cancellation and audio processing
- Cross-browser compatibility

### Usage Tips
- Speak clearly and at moderate pace
- Use natural language, avoid technical jargon
- Wait for the recording indicator before speaking
- Click stop when finished speaking

##  Configuration

### Backend Configuration (.env)
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///query_assistant.db
FLASK_DEBUG=True
PORT=5000
```

### Frontend Configuration
Environment variables can be set in `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:5000
```


##  Security Features

### SQL Injection Protection
- Parameterized queries
- Input validation and sanitization
- Whitelist-based query filtering
- Read-only query enforcement

### Data Privacy
- No sensitive data logging
- Secure audio processing
- Local data storage only
- No external API calls for core functionality

##  Customization

### Adding New Intents
1. Update `intent_patterns` in `nlp_processor.py`
2. Add corresponding query logic in `text_to_sql` method
3. Retrain the model by restarting the application

### Custom Database
1. Update models in `models.py`
2. Modify sample data in `database.py`
3. Update schema information accordingly



**Happy Querying!** 

Try starting with simple queries like "Show all employees" and gradually move to more complex requests. The AI will learn and improve its responses over time.
