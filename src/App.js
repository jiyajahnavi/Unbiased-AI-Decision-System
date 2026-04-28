import React, { useState } from 'react';
import DatasetAnalysis from './components/DatasetAnalysis';
import ModelAnalysis from './components/ModelAnalysis';
import FairnessDashboard from './components/FairnessDashboard';
import MitigationTools from './components/MitigationTools';
import Explainability from './components/Explainability';
import ReportGenerator from './components/ReportGenerator';

function App() {
  const [activeTab, setActiveTab] = useState('dataset');
  const [results, setResults] = useState({});

  const tabs = [
    { id: 'dataset', label: 'Dataset Analysis', component: DatasetAnalysis },
    { id: 'model', label: 'Model Analysis', component: ModelAnalysis },
    { id: 'dashboard', label: 'Fairness Dashboard', component: FairnessDashboard },
    { id: 'mitigation', label: 'Bias Mitigation', component: MitigationTools },
    { id: 'explain', label: 'Explainability', component: Explainability },
    { id: 'report', label: 'Generate Report', component: ReportGenerator },
  ];

  const updateResults = (key, data) => {
    setResults(prev => ({ ...prev, [key]: data }));
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              Unbiased AI Decision: Fairness Auditor
            </h1>
          </div>
        </div>
      </header>

      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {tabs.map(tab => (
            activeTab === tab.id && (
              <tab.component 
                key={tab.id} 
                results={results} 
                updateResults={updateResults} 
              />
            )
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;