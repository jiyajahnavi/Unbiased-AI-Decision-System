import React, { useState } from 'react';
import axios from 'axios';

const DatasetAnalysis = ({ results, updateResults }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/analyze-dataset', formData);
      updateResults('dataset', response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const data = results.dataset;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Dataset Bias Analysis</h2>
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload Dataset (CSV or Excel)
        </label>
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button
          onClick={handleAnalyze}
          disabled={!file || loading}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze Dataset'}
        </button>
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {data && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800">Sensitive Attributes</h3>
              <p className="text-2xl font-bold">{data.sensitive_attributes?.join(', ') || 'None detected'}</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-medium text-green-800">Fairness Score</h3>
              <p className="text-2xl font-bold">{data.fairness_score}/100</p>
            </div>
          </div>
          
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-2">Distribution Analysis</h3>
            <pre className="bg-gray-50 p-4 rounded overflow-auto text-xs">
              {JSON.stringify(data.distribution_analysis, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default DatasetAnalysis;
