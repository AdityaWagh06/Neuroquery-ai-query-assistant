import React from 'react';
import { Card, Spinner } from 'react-bootstrap';

const LoadingSpinner = () => {
  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body className="text-center py-5">
        <Spinner animation="border" role="status" className="mb-3">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <h6 className="text-muted">Processing your query...</h6>
        <p className="text-muted mb-0">
          <small>This may take a few seconds</small>
        </p>
      </Card.Body>
    </Card>
  );
};

export default LoadingSpinner;
