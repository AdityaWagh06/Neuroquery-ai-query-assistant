import React, { useState, useEffect } from 'react';
import { Card, Accordion, Badge, Spinner, Alert } from 'react-bootstrap';
import { apiService } from '../services/api';

const DatabaseSchema = () => {
  const [schema, setSchema] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    try {
      setLoading(true);
      const response = await apiService.getDatabaseSchema();
      if (response.success) {
        setSchema(response.schema);
      } else {
        setError(response.error);
      }
    } catch (error) {
      setError('Failed to load schema');
    } finally {
      setLoading(false);
    }
  };

  const getColumnTypeColor = (type) => {
    const typeUpper = type.toUpperCase();
    if (typeUpper.includes('INT')) return 'primary';
    if (typeUpper.includes('VARCHAR') || typeUpper.includes('TEXT')) return 'success';
    if (typeUpper.includes('DATE') || typeUpper.includes('TIME')) return 'warning';
    if (typeUpper.includes('FLOAT') || typeUpper.includes('DECIMAL')) return 'info';
    return 'secondary';
  };

  if (loading) {
    return (
      <Card className="mb-4 shadow-sm">
        <Card.Body className="text-center">
          <Spinner animation="border" size="sm" className="me-2" />
          Loading schema...
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="mb-4 shadow-sm">
        <Card.Body>
          <Alert variant="warning" className="mb-0">
            <small>Could not load schema: {error}</small>
          </Alert>
        </Card.Body>
      </Card>
    );
  }

  if (!schema || !schema.tables) {
    return (
      <Card className="mb-4 shadow-sm">
        <Card.Body>
          <Alert variant="info" className="mb-0">
            <small>No schema information available</small>
          </Alert>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card className="shadow-sm">
      <Card.Header className="bg-light">
        <h6 className="mb-0">
          🗂️ Database Schema
        </h6>
      </Card.Header>
      <Card.Body className="p-0">
        <Accordion flush>
          {schema.tables.map((table, tableIndex) => (
            <Accordion.Item key={tableIndex} eventKey={tableIndex.toString()}>
              <Accordion.Header>
                <div className="d-flex justify-content-between align-items-center w-100 me-3">
                  <span className="fw-semibold">{table.name}</span>
                  <Badge bg="secondary" pill>
                    {table.columns.length} columns
                  </Badge>
                </div>
              </Accordion.Header>
              <Accordion.Body className="p-3">
                <div className="table-responsive">
                  <table className="table table-sm">
                    <thead>
                      <tr>
                        <th>Column</th>
                        <th>Type</th>
                        <th>Key</th>
                      </tr>
                    </thead>
                    <tbody>
                      {table.columns.map((column, columnIndex) => (
                        <tr key={columnIndex}>
                          <td>
                            <span className="fw-semibold">
                              {column.name}
                            </span>
                            {!column.nullable && (
                              <Badge bg="danger" pill size="sm" className="ms-2">
                                Required
                              </Badge>
                            )}
                          </td>
                          <td>
                            <Badge bg={getColumnTypeColor(column.type)}>
                              {column.type}
                            </Badge>
                          </td>
                          <td>
                            {column.primary_key && (
                              <Badge bg="warning">
                                PK
                              </Badge>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Accordion.Body>
            </Accordion.Item>
          ))}
        </Accordion>
      </Card.Body>
      <Card.Footer className="bg-light">
        <small className="text-muted">
          Database structure for reference when asking questions
        </small>
      </Card.Footer>
    </Card>
  );
};

export default DatabaseSchema;
