import React, { useState } from 'react';
import { Form, Button, InputGroup } from 'react-bootstrap';
import { FiSearch } from 'react-icons/fi';

const QueryInput = ({ onSubmit, loading, disabled }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !loading && !disabled) {
      onSubmit(query.trim());
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <InputGroup>
        <Form.Control
          as="textarea"
          rows={3}
          placeholder="Type your question here... (e.g., 'Show all employees' or 'How many people work in IT?')"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={disabled}
          style={{ resize: 'none' }}
        />
        <Button 
          variant="primary" 
          type="submit" 
          disabled={!query.trim() || loading || disabled}
          style={{ minWidth: '100px' }}
        >
          {loading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" />
              Processing...
            </>
          ) : (
            <>
              <FiSearch className="me-2" />
              Ask
            </>
          )}
        </Button>
      </InputGroup>
      <Form.Text className="text-muted">
        Press Enter to submit, or Shift+Enter for a new line
      </Form.Text>
    </Form>
  );
};

export default QueryInput;
