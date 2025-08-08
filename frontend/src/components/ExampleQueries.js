import React, { useState, useEffect } from 'react';
import { Card, ListGroup, Badge, Spinner, Alert } from 'react-bootstrap';
import { apiService } from '../services/api';

const ExampleQueries = ({ onExampleClick, disabled }) => {
  const [examples, setExamples] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadExamples();
  }, []);

  const loadExamples = async () => {
    try {
      setLoading(true);
      const response = await apiService.getExamples();
      if (response.success) {
        setExamples(response.examples);
      } else {
        setError(response.error);
      }
    } catch (error) {
      setError('Failed to load examples');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleText) => {
    if (!disabled) {
      onExampleClick(exampleText);
    }
  };

  if (loading) {
    return (
      <Card className="mb-4 shadow-sm">
        <Card.Body className="text-center">
          <Spinner animation="border" size="sm" className="me-2" />
          Loading examples...
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="mb-4 shadow-sm">
        <Card.Body>
          <Alert variant="warning" className="mb-0">
            <small>Could not load examples: {error}</small>
          </Alert>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Header className="bg-light">
        <h6 className="mb-0">
          💡 Example Queries
        </h6>
      </Card.Header>
      <Card.Body className="p-0">
        <ListGroup variant="flush">
          {examples.map((example, index) => (
            <ListGroup.Item
              key={index}
              className={`cursor-pointer ${disabled ? 'disabled' : 'list-group-item-action'}`}
              onClick={() => handleExampleClick(example.text)}
              style={{ 
                cursor: disabled ? 'not-allowed' : 'pointer',
                opacity: disabled ? 0.6 : 1
              }}
            >
              <div className="d-flex justify-content-between align-items-start">
                <div className="flex-grow-1">
                  <div className="fw-semibold text-primary mb-1">
                    "{example.text}"
                  </div>
                  <small className="text-muted">
                    {example.description}
                  </small>
                </div>
                <Badge bg="secondary" pill className="ms-2">
                  Try it
                </Badge>
              </div>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Card.Body>
      <Card.Footer className="bg-light">
        <small className="text-muted">
          Click on any example to try it out
        </small>
      </Card.Footer>
    </Card>
  );
};

export default ExampleQueries;
