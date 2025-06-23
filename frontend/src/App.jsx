import './App.css';
import { useState } from 'react';
import CaseForms from './components/CaseForms.tsx';
import CaseList from './components/CaseList.tsx';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App() {
    const [refreshList, setRefreshList] = useState(false);
    const [editingCase, setEditingCase] = useState(null);
  
    const handleCaseEdited = () => {
      setRefreshList(prev => !prev); // Alternar para forzar la recarga
      setEditingCase(null); // Limpiar el formulario de edición
    };
  
    const handleEditClick = (caseToEdit) => {
      setEditingCase(caseToEdit);
    };
  return (
    <div className="App">
    <header className="App-header">
      <h1>Support Cases</h1>
    </header>
    <main>
      <section>
        <h2>{editingCase ? 'Edit Case' : 'Add New Case'}</h2>
        <CaseForms
          API_BASE_URL={API_BASE_URL}
          onCaseAdded={handleCaseEdited}
          onCaseUpdated={handleCaseEdited}
          editingCase={editingCase}
        />
        {editingCase && (
          <button style={{marginTop: '10px'}} className="button-support" onClick={() => setEditingCase(null)}>Cancel Edit</button>
        )}
      </section>
      <section>
        <h2>All Cases</h2>
        <CaseList
          API_BASE_URL={API_BASE_URL}
          refreshList={refreshList}
          onEditCase={handleEditClick}
          onCaseDeleted={handleCaseEdited}
        />
      </section>
    </main>
  </div>
  );
}

export default App;
