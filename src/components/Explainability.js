import React, { useState } from 'react';
import axios from 'axios';

const Explainability = ({ results, updateResults }) => {
  const [modelFile, setModelFile] = useState(null);
  const [dataFile, setDataFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleExplain = async () => {
    if (!modelFile || !dataFile) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('model_file', modelFile);
    formData.append('data_file', dataFile);

    try {
      const response = await axios.post('/explain-model', formData);
      updateResults('explain', response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Explanation generation failed');
    } finally {
      setLoading(false);
    }
  };

  const data = results.explain;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Model Explainability (SHAP/LIME)</h2>
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Model File (.joblib)</label>
          <input type="file" onChange={(e) => setModelFile(e.target.files[0])} className="block w-full text-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Reference Data (.csv)</label>
          <input type="file" onChange={(e) => setDataFile(e.target.files[0])} className="block w-full text-sm" />
        </div>
        <button
          onClick={handleExplain}
          disabled={!modelFile || !dataFile || loading}
          className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:bg-gray-400"
        >
          {loading ? 'Generating Explanations...' : 'Explain Model'}
        </button>
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {data && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Feature Importance</h3>
          <div className="space-y-2">
            {Object.entries(data.global_importance || {}).map(([feature, importance]) => (
              <div key={feature} className="flex items-center">
                <div className="w-32 text-sm text-gray-600 truncate">{feature}</div>
                <div className="flex-1 bg-gray-100 h-4 rounded overflow-hidden">
                  <div 
                    className="bg-purple-500 h-full" 
                    style={{ width: `${Math.min(importance * 100, 100)}%` }}
                  ></div>
                </div>
                <div className="w-16 text-right text-xs text-gray-400 ml-2">{(importance * 100).toFixed(1)}%</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Explainability;
