// frontend/src/components/CaseList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Case {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  created_at: string;
}

function CaseList({ API_BASE_URL, refreshList, onEditCase, onCaseDeleted }) {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchCases = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_BASE_URL}/cases/`);
      setCases(response.data);
    } catch (err) {
      console.error("Error fetching cases:", err.response || err);
      setError(err.response?.data?.detail || 'Failed to load cases.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCases();
  }, [refreshList]);

  const handleDelete = async (caseId) => {
    if (window.confirm("Are you sure you want to delete this case?")) {
      try {
        await axios.delete(`${API_BASE_URL}/cases/${caseId}`);
        alert('Case deleted successfully!');
        onCaseDeleted();
      } catch (err) {
        console.error("Error deleting case:", err.response || err);
        setError(err.response?.data?.detail || 'Failed to delete case.');
      }
    }
  };

  if (loading) return <p>Loading cases...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;
  if (cases.length === 0) return <p>No support cases found. Add one above!</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Status</th>
          <th>Priority</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {cases.map((caseItem) => (
          <tr key={caseItem.id}>
            <td>{caseItem.title}</td>
            <td>{caseItem.description.substring(0, 100)}{caseItem.description.length > 100 ? '...' : ''}</td>
            <td>{caseItem.status}</td>
            <td>{caseItem.priority}</td>
            <td>{new Date(caseItem.created_at).toLocaleDateString()}</td>
            <td>
              <button onClick={() => onEditCase(caseItem)}>Edit</button>
              <button onClick={() => handleDelete(caseItem.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default CaseList;