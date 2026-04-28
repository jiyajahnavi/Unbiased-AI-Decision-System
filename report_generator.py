import os
from fpdf import FPDF
from typing import Dict, List, Any
import json

class FairnessReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Unbiased AI Decision: Fairness Audit Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section(self, title: str, content: str):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, content)
        self.ln(5)

def generate_report(data: Dict[str, Any]) -> str:
    """Generate PDF fairness report"""
    pdf = FairnessReport()
    pdf.add_page()
    
    # Executive Summary
    pdf.add_section('Executive Summary', 
                   'This report presents the results of a comprehensive fairness audit '
                   'conducted on the provided dataset and/or machine learning model.')
    
    # Dataset Analysis
    if 'dataset_analysis' in data:
        pdf.add_section('Dataset Bias Analysis', 
                       json.dumps(data['dataset_analysis'], indent=2))
    
    # Model Analysis
    if 'model_analysis' in data:
        pdf.add_section('Model Bias Analysis', 
                       json.dumps(data['model_analysis'], indent=2))
    
    # Fairness Metrics
    if 'fairness_metrics' in data:
        pdf.add_section('Fairness Metrics', 
                       json.dumps(data['fairness_metrics'], indent=2))
    
    # Mitigation Results
    if 'mitigation_results' in data:
        pdf.add_section('Bias Mitigation Results', 
                       json.dumps(data['mitigation_results'], indent=2))
    
    # Explanations
    if 'explanations' in data:
        pdf.add_section('Model Explanations', 
                       json.dumps(data['explanations'], indent=2))
    
    # Recommendations
    recommendations = generate_recommendations(data)
    pdf.add_section('Recommendations', '\n'.join(recommendations))
    
    # Save report
    report_path = os.path.join(os.getcwd(), 'fairness_report.pdf')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    pdf.output(report_path)
    
    return report_path

def generate_recommendations(data: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on analysis results"""
    recommendations = []
    
    # Dataset recommendations
    if 'dataset_analysis' in data:
        analysis = data['dataset_analysis']
        if analysis.get('missing_groups'):
            recommendations.append('Consider collecting more data for underrepresented groups.')
        
        for attr, imbalance in analysis.get('representation_imbalance', {}).items():
            if imbalance.get('is_imbalanced'):
                recommendations.append(f'Address imbalance in {attr} attribute through data collection or augmentation.')
    
    # Model recommendations
    if 'model_analysis' in data:
        analysis = data['model_analysis']
        for attr, acc_diff in analysis.get('accuracy_differences', {}).items():
            if acc_diff > 0.1:  # 10% difference
                recommendations.append(f'Investigate accuracy differences across {attr} groups.')
    
    # Fairness metrics recommendations
    if 'fairness_metrics' in data:
        metrics = data['fairness_metrics']
        if 'statistical_parity' in metrics:
            spd = abs(metrics['statistical_parity']['value'])
            if spd > 0.1:
                recommendations.append('Consider reweighing or resampling to reduce statistical parity difference.')
        
        if 'disparate_impact_ratio' in metrics:
            di = metrics['disparate_impact_ratio']['value']
            if di < 0.8 or di > 1.25:
                recommendations.append('Disparate impact detected. Consider threshold adjustment or model retraining.')
    
    # Explanation recommendations
    if 'explanations' in data:
        exp = data['explanations']
        if 'sensitive_feature_importance' in exp:
            for attr, imp in exp['sensitive_feature_importance'].items():
                if imp > 0.1:
                    recommendations.append(f'Consider removing or masking {attr} feature if it leads to discrimination.')
    
    if not recommendations:
        recommendations.append('No major fairness issues detected. Continue monitoring.')
    
    return recommendations