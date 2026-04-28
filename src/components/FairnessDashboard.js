import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const FairnessDashboard = ({ results }) => {
  const dataset = results.dataset;
  const model = results.model;

  if (!dataset && !model) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md text-center">
        <p className="text-gray-500">Please complete Dataset or Model analysis first.</p>
      </div>
    );
  }

  const prepareDistData = () => {
    if (!dataset?.distribution_analysis || Object.keys(dataset.distribution_analysis).length === 0) return [];
    const firstAttr = Object.keys(dataset.distribution_analysis)[0];
    const dist = dataset.distribution_analysis[firstAttr];
    if (!dist) return [];
    return Object.entries(dist).map(([group, val]) => ({
      name: group,
      value: val * 100
    }));
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-gray-500 text-sm font-medium">Fairness Score</h3>
          <p className={`text-4xl font-bold ${dataset?.fairness_score > 80 ? 'text-green-600' : 'text-orange-600'}`}>
            {dataset?.fairness_score || '--'}
          </p>
          <p className="text-xs text-gray-400 mt-2">Scale: 0-100 (100 is best)</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-gray-500 text-sm font-medium">Sensitive Attributes</h3>
          <p className="text-2xl font-bold">{dataset?.sensitive_attributes?.length || 0}</p>
          <p className="text-xs text-gray-400 mt-2">Detected in dataset</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-gray-500 text-sm font-medium">Risk Status</h3>
          <p className={`text-2xl font-bold ${(dataset?.missing_groups?.length > 0) ? 'text-red-600' : 'text-green-600'}`}>
            {dataset?.missing_groups?.length > 0 ? 'HIGH RISK' : 'LOW RISK'}
          </p>
          <p className="text-xs text-gray-400 mt-2">Based on group representation</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">Group Distribution</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={prepareDistData()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" name="Percentage (%)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {dataset?.missing_groups?.length > 0 && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <h3 className="text-red-800 font-bold">Bias Alerts</h3>
          <ul className="list-disc list-inside text-red-700 mt-2">
            {dataset.missing_groups.map((g, i) => (
              <li key={i}>
                Underrepresented group: <strong>{g.group}</strong> in attribute <strong>{g.attribute}</strong> ({(g.percentage * 100).toFixed(1)}%)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FairnessDashboard;
