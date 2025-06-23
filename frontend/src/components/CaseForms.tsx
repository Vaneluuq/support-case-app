import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Definir los tipos de estado y prioridad para usar en el formulario
const CaseStatusOptions = ["Open", "In Progress", "Resolved", "Closed"];
const CasePriorityOptions = ["Low", "Medium", "High", "Critical"];

function CaseForms({ API_BASE_URL, onCaseAdded, onCaseUpdated, editingCase }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState(CaseStatusOptions[0]);
  const [priority, setPriority] = useState(CasePriorityOptions[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Rellenar el formulario si estamos en modo edición
  useEffect(() => {
    if (editingCase) {
      setTitle(editingCase.title);
      setDescription(editingCase.description);
      setStatus(editingCase.status);
      setPriority(editingCase.priority);
    } else {
      // Limpiar el formulario si no estamos editando
      setTitle('');
      setDescription('');
      setStatus(CaseStatusOptions[0]);
      setPriority(CasePriorityOptions[0]);
    }
  }, [editingCase]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const caseData = { title, description, status, priority };

    try {
      if (editingCase) {
        // Modo edición (PUT)
        await axios.put(`${API_BASE_URL}/cases/${editingCase?.id}`, caseData);
        alert('Case updated successfully!');
        onCaseUpdated();
      } else {
        // Modo añadir (POST)
        await axios.post(`${API_BASE_URL}/cases/`, caseData);
        alert('Case added successfully!');
        onCaseAdded();
      }
    } catch (err) {
      console.error("Error submitting case:", err.response || err);
      setError(err.response?.data?.detail || 'Failed to submit case.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <label>Title:</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          disabled={loading}
        />
      </div>
      <div>
        <label>Description:</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
          required
          disabled={loading}
        ></textarea>
      </div>
      <div>
        <label>Status:</label>
        <select value={status} onChange={(e) => setStatus(e.target.value)} disabled={loading}>
          {CaseStatusOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
      </div>
      <div>
        <label>Priority:</label>
        <select value={priority} onChange={(e) => setPriority(e.target.value)} disabled={loading}>
          {CasePriorityOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Submitting...' : (editingCase ? 'Update Case' : 'Add Case')}
      </button>
    </form>
  );
}

export default CaseForms;
