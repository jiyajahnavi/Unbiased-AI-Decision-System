# Unbiased AI Decision: Demo Script

## Overview
This demo script walks through the key features of the Fairness Auditor system using sample data.

## Prerequisites
- Backend running on port 8000
- Frontend running on port 3000
- Sample datasets in `data/` directory

## Demo Scenario: Hiring Bias Analysis

### Step 1: Dataset Analysis
1. Open browser to http://localhost:3000
2. Click "Dataset Analysis" tab
3. Upload `data/hiring_dataset.csv`
4. Click "Analyze Dataset"

**Expected Results:**
- Sensitive attributes detected: gender, age
- Distribution: ~50% Male, ~50% Female
- Fairness metrics:
  - Disparate Impact: ~0.85 (women 15% less likely to be hired)
  - Statistical Parity Difference: ~-0.15
- Fairness Score: ~75/100 (moderate bias)

### Step 2: Model Analysis
1. Click "Model Analysis" tab
2. Upload `models/hiring_model.joblib` (or train one first)
3. Upload `data/hiring_dataset.csv` as test data
4. Click "Analyze Model"

**Expected Results:**
- Confusion matrices showing different error rates
- Accuracy differences: ~8-12% between groups
- FPR/FNR differences indicating bias patterns

### Step 3: Fairness Dashboard
1. Click "Fairness Dashboard" tab

**Visualizations:**
- Bar chart showing gender distribution
- Fairness metrics comparison chart
- Overall fairness score with color coding
- Risk alerts for high-bias areas

### Step 4: Bias Mitigation
1. Click "Bias Mitigation" tab
2. Select "Reweighing" method
3. Click "Apply Mitigation"

**Results:**
- Sample weights adjusted for balanced outcomes
- Before/after acceptance rate comparison
- Improved fairness metrics

### Step 5: Explainability
1. Click "Explainability" tab
2. Select "SHAP" method
3. Click "Generate Explanations"

**Insights:**
- Feature importance rankings
- Gender as sensitive attribute in top features
- Group-wise explanation differences
- Recommendations for model improvement

### Step 6: Report Generation
1. Click "Generate Report" tab
2. Click "Generate PDF Report"

**Output:**
- Comprehensive PDF with:
  - Executive summary
  - Analysis results
  - Visualizations
  - Recommendations
  - Actionable insights

## Advanced Demo: Multi-Dataset Comparison

### Compare All Sample Datasets
1. Repeat analysis for loan and healthcare datasets
2. Note different bias patterns:
   - Hiring: Gender discrimination
   - Loans: Age + gender discrimination
   - Healthcare: Race + gender discrimination

### Mitigation Comparison
1. Apply different mitigation techniques
2. Compare effectiveness:
   - Reweighing: Good for outcome balancing
   - Oversampling: Good for representation
   - Threshold adjustment: Good for acceptance rates

## Key Demo Points

### Bias Detection Capabilities
- Automatic sensitive attribute detection
- Multiple fairness metrics calculation
- Statistical significance testing
- Risk level assessment

### Visualization Features
- Interactive charts with Recharts
- Color-coded risk indicators
- Group comparison views
- Trend analysis

### Mitigation Effectiveness
- Before/after metric comparison
- Technique-specific recommendations
- Scalable to large datasets

### Explainability Depth
- Global vs local explanations
- Group-wise feature analysis
- Sensitive attribute flagging
- Model transparency insights

### Report Quality
- Professional PDF formatting
- Stakeholder-ready content
- Regulatory compliance ready
- Actionable recommendations

## Demo Script for Presentations

### 5-Minute Version
1. Dataset upload and analysis (2 min)
2. Dashboard overview (1.5 min)
3. Mitigation demo (1 min)
4. Report generation (0.5 min)

### 10-Minute Version
Add model analysis and explainability sections

### 15-Minute Version
Include multi-dataset comparison and advanced features

## Troubleshooting Demo Issues

### Data Loading Errors
- Ensure CSV files have headers
- Check for special characters
- Verify file encoding (UTF-8)

### Model Loading Errors
- Use joblib format (.joblib or .pkl)
- Ensure model is trained on similar features
- Check scikit-learn version compatibility

### API Connection Issues
- Verify backend is running on port 8000
- Check CORS settings
- Review network/firewall settings

### Visualization Issues
- Ensure modern browser
- Check JavaScript console for errors
- Verify Recharts library loaded

## Success Metrics

### Technical Success
- All API endpoints responding
- Models loading correctly
- Visualizations rendering
- PDF generation working

### User Experience Success
- Intuitive interface navigation
- Clear result interpretation
- Actionable recommendations
- Professional report output

### Business Value Success
- Bias detection accuracy
- Mitigation effectiveness
- Regulatory compliance readiness
- Stakeholder communication

## Next Steps After Demo

1. **Customization**: Adapt for specific use cases
2. **Integration**: Connect to existing ML pipelines
3. **Scaling**: Handle larger datasets and models
4. **Compliance**: Meet regulatory requirements
5. **Monitoring**: Set up continuous fairness monitoring

---

*This demo showcases a production-ready fairness auditing system for responsible AI development.*