import React, { useState } from 'react';
import axios from 'axios';

const MitigationTools = ({ results, updateResults }) => {
  const [method, setMethod] = useState('reweighing');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleApply = async () => {
    if (!results.dataset?.data) return;
    setLoading(true);
    setError(null);

    const firstAttr = results.dataset.sensitive_attributes[0];
    const target = results.dataset.target_column;

    try {
      const response = await axios.post('/mitigate-bias', {
        data: results.dataset.data,
        sensitive_attribute: firstAttr,
        target_column: target,
        method: method
      });
      updateResults('mitigation', response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Mitigation failed');
    } finally {
      setLoading(false);
    }
  };

  const data = results.mitigation;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Bias Mitigation Tools</h2>
      
      {!results.dataset && (
        <p className="text-orange-600 mb-4">Please analyze a dataset first to enable mitigation tools.</p>
      )}

      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Select Mitigation Method</label>
          <select 
            value={method} 
            onChange={(e) => setMethod(e.target.value)}
            className="block w-full p-2 border border-gray-300 rounded-md"
          >
            <option value="reweighing">Reweighing (Pre-processing)</option>
            <option value="oversampling">Oversampling (Pre-processing)</option>
            <option value="undersampling">Undersampling (Pre-processing)</option>
            <option value="threshold">Threshold Adjustment (Post-processing)</option>
          </select>
        </div>
        
        <button
          onClick={handleApply}
          disabled={!results.dataset || loading}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:bg-gray-400"
        >
          {loading ? 'Applying...' : 'Apply Mitigation'}
        </button>
      </div>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {data && (
        <div className="mt-6">
          <h3 className="text-lg font-medium mb-2">Mitigation Results</h3>
          <p className="text-sm text-gray-600 mb-4">Original vs Mitigated acceptance rates</p>
          <pre className="bg-gray-50 p-4 rounded overflow-auto text-xs">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default MitigationTools;
