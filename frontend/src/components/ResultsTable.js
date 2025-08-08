import React, { useMemo } from 'react';
import { Table, Alert } from 'react-bootstrap';

const ResultsTable = ({ data, columns }) => {
  const tableData = useMemo(() => {
    if (!data || !Array.isArray(data) || data.length === 0) {
      return [];
    }
    return data;
  }, [data]);

  const tableColumns = useMemo(() => {
    if (!columns || !Array.isArray(columns) || columns.length === 0) {
      // If no columns provided, infer from first data row
      if (tableData.length > 0) {
        return Object.keys(tableData[0]);
      }
      return [];
    }
    return columns;
  }, [columns, tableData]);

  if (!tableData.length) {
    return (
      <Alert variant="info" className="text-center">
        <h6>📋 No Results</h6>
        No data found for your query.
      </Alert>
    );
  }

  const formatCellValue = (value) => {
    if (value === null || value === undefined) {
      return <span className="text-muted">-</span>;
    }
    
    if (typeof value === 'boolean') {
      return value ? '✓' : '✗';
    }
    
    if (typeof value === 'number') {
      // Format numbers with commas for large values
      if (value > 999) {
        return value.toLocaleString();
      }
      return value.toString();
    }
    
    if (typeof value === 'string') {
      // Truncate very long strings
      if (value.length > 100) {
        return (
          <span title={value}>
            {value.substring(0, 97)}...
          </span>
        );
      }
    }
    
    return value.toString();
  };

  const formatColumnName = (columnName) => {
    // Convert snake_case to Title Case
    return columnName
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="table-responsive">
      <Table striped bordered hover size="sm">
        <thead className="table-dark">
          <tr>
            {tableColumns.map((column, index) => (
              <th key={index} className="text-nowrap">
                {formatColumnName(column)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {tableColumns.map((column, colIndex) => (
                <td key={colIndex} className="align-middle">
                  {formatCellValue(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>
      
      <div className="mt-2">
        <small className="text-muted">
          Showing {tableData.length} result{tableData.length !== 1 ? 's' : ''} 
          {tableColumns.length > 0 && ` with ${tableColumns.length} column${tableColumns.length !== 1 ? 's' : ''}`}
        </small>
      </div>
    </div>
  );
};

export default ResultsTable;
