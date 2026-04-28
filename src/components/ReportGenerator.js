import React, { useState } from 'react';
import axios from 'axios';

const ReportGenerator = ({ results }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);

    try {
      const mappedResults = {
        dataset_analysis: results.dataset,
        model_analysis: results.model,
        fairness_metrics: results.dataset?.fairness_metrics,
        mitigation_results: results.mitigation,
        explanations: results.explain
      };

      const response = await axios.post('/generate-report', mappedResults, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'fairness_audit_report.pdf');
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      setError('Report generation failed. Ensure you have enough analysis results.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md text-center">
      <h2 className="text-xl font-semibold mb-4">Generate Fairness Audit Report</h2>
      <p className="text-gray-600 mb-6">
        Download a comprehensive PDF report containing all your analysis results, visualizations, and bias mitigation findings.
      </p>
      
      <button
        onClick={handleGenerate}
        disabled={loading || Object.keys(results).length === 0}
        className="bg-red-600 text-white px-8 py-3 rounded-full font-bold hover:bg-red-700 shadow-lg transition-all disabled:bg-gray-300"
      >
        {loading ? 'Generating PDF...' : 'Download PDF Report'}
      </button>

      {error && <div className="text-red-500 mt-4">{error}</div>}
      
      {Object.keys(results).length === 0 && (
        <p className="text-xs text-orange-500 mt-4">
          Perform at least one analysis to generate a report.
        </p>
      )}
    </div>
  );
};

export default ReportGenerator;
