import React, { useState } from 'react';
import axios from 'axios';

const ModelAnalysis = ({ results, updateResults }) => {
  const [modelFile, setModelFile] = useState(null);
  const [dataFile, setDataFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!modelFile || !dataFile) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('model_file', modelFile);
    formData.append('data_file', dataFile);

    try {
      const response = await axios.post('/analyze-model', formData);
      updateResults('model', response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const data = results.model;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Model Bias Analysis</h2>
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Upload Model (.joblib)</label>
          <input type="file" onChange={(e) => setModelFile(e.target.files[0])} className="block w-full text-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Upload Test Data (.csv, .xlsx)</label>
          <input type="file" onChange={(e) => setDataFile(e.target.files[0])} className="block w-full text-sm" />
        </div>
        <button
          onClick={handleAnalyze}
          disabled={!modelFile || !dataFile || loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze Model'}
        </button>
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {data && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(data.accuracy_differences || {}).map(([attr, diff]) => (
              <div key={attr} className="p-4 bg-orange-50 rounded-lg">
                <h3 className="font-medium text-orange-800">Accuracy Diff ({attr})</h3>
                <p className="text-2xl font-bold">{(diff * 100).toFixed(2)}%</p>
              </div>
            ))}
          </div>
          
          <div>
            <h3 className="text-lg font-medium mb-2">Confusion Matrices</h3>
            <pre className="bg-gray-50 p-4 rounded overflow-auto text-xs">
              {JSON.stringify(data.confusion_matrices, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelAnalysis;
