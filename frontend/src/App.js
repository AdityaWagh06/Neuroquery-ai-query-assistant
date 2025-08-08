import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Alert } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import QueryInput from './components/QueryInput';
import VoiceInput from './components/VoiceInput';
import ResultsTable from './components/ResultsTable';
import ExampleQueries from './components/ExampleQueries';
import DatabaseSchema from './components/DatabaseSchema';
import LoadingSpinner from './components/LoadingSpinner';
import { apiService } from './services/api';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';
import './styles/App.css';

function App() {
  const [queryResults, setQueryResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await apiService.healthCheck();
      setApiStatus('connected');
    } catch (error) {
      setApiStatus('disconnected');
      toast.error('Unable to connect to API server');
    }
  };

  const handleQuerySubmit = async (queryText, isVoice = false) => {
    setLoading(true);
    setError(null);

    try {
      const result = isVoice 
        ? await apiService.processVoice(queryText)
        : await apiService.processQuery(queryText);

      if (result.success) {
        setQueryResults(result);
        if (isVoice) {
          toast.success(`Voice recognized: "${result.transcribed_text}"`);
        }
      } else {
        setError(result.error);
        toast.error(result.error);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'An error occurred while processing your query';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleQuery = (exampleText) => {
    handleQuerySubmit(exampleText);
  };

  const clearResults = () => {
    setQueryResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <Container fluid className="py-4">
        <Row>
          <Col>
            <div className="text-center mb-4">
              <h1 className="display-4 text-primary mb-2">
                🤖 AI Query Assistant
              </h1>
              <p className="lead text-muted">
                Ask questions about your database in natural language or use voice commands
              </p>
              
              {/* API Status Indicator */}
              <div className="mb-3">
                {apiStatus === 'checking' && (
                  <Alert variant="info" className="d-inline-block">
                    <span className="spinner-border spinner-border-sm me-2" role="status" />
                    Connecting to API...
                  </Alert>
                )}
                {apiStatus === 'connected' && (
                  <Alert variant="success" className="d-inline-block">
                    ✅ API Connected
                  </Alert>
                )}
                {apiStatus === 'disconnected' && (
                  <Alert variant="danger" className="d-inline-block">
                    ❌ API Disconnected
                  </Alert>
                )}
              </div>
            </div>
          </Col>
        </Row>

        <Row>
          <Col lg={8}>
            {/* Query Input Section */}
            <Card className="mb-4 shadow-sm">
              <Card.Body>
                <h5 className="card-title mb-3">
                  💬 Ask Your Question
                </h5>
                <QueryInput 
                  onSubmit={handleQuerySubmit} 
                  loading={loading}
                  disabled={apiStatus !== 'connected'}
                />
                
                <div className="text-center mt-3">
                  <span className="text-muted me-3">or</span>
                </div>
                
                <div className="text-center mt-3">
                  <VoiceInput 
                    onVoiceSubmit={handleQuerySubmit}
                    loading={loading}
                    disabled={apiStatus !== 'connected'}
                  />
                </div>
              </Card.Body>
            </Card>

            {/* Loading Spinner */}
            {loading && <LoadingSpinner />}

            {/* Error Display */}
            {error && (
              <Alert variant="danger" className="mb-4">
                <h6>❌ Error</h6>
                {error}
              </Alert>
            )}

            {/* Query Results */}
            {queryResults && !loading && (
              <Card className="mb-4 shadow-sm">
                <Card.Body>
                  <div className="d-flex justify-content-between align-items-center mb-3">
                    <h5 className="card-title mb-0">
                      📊 Query Results
                    </h5>
                    <button 
                      className="btn btn-outline-secondary btn-sm"
                      onClick={clearResults}
                    >
                      Clear Results
                    </button>
                  </div>
                  
                  {/* Query Information */}
                  <div className="mb-3">
                    <small className="text-muted">
                      <strong>Original Query:</strong> {queryResults.original_query || queryResults.transcribed_text}
                    </small>
                    <br />
                    <small className="text-muted">
                      <strong>SQL Query:</strong> <code>{queryResults.sql_query}</code>
                    </small>
                    <br />
                    <small className="text-muted">
                      <strong>Intent:</strong> <span className="badge bg-info">{queryResults.intent}</span>
                    </small>
                    <br />
                    <small className="text-muted">
                      <strong>Results:</strong> {queryResults.row_count} row(s) found
                    </small>
                  </div>

                  <ResultsTable 
                    data={queryResults.results} 
                    columns={queryResults.columns}
                  />
                </Card.Body>
              </Card>
            )}
          </Col>

          <Col lg={4}>
            {/* Example Queries */}
            <ExampleQueries 
              onExampleClick={handleExampleQuery}
              disabled={loading || apiStatus !== 'connected'}
            />

            {/* Database Schema */}
            <DatabaseSchema />
          </Col>
        </Row>
      </Container>

      {/* Toast Notifications */}
      <ToastContainer
        position="bottom-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}

export default App;
