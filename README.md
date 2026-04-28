# Unbiased AI Decision: Fairness Auditor for Machine Learning Systems

A comprehensive, production-ready system for detecting, measuring, visualizing, and mitigating bias in machine learning models used for high-stakes decisions.

## 🎯 Overview

This application provides end-to-end fairness auditing capabilities for ML systems, helping organizations ensure their AI models make equitable decisions across different demographic groups.

## 🚀 Features

### Core Functionality
- **Dataset Bias Analysis**: Detect sensitive attributes and analyze representation imbalances
- **Model Bias Detection**: Evaluate model predictions across demographic groups
- **Fairness Metrics Engine**: Calculate statistical parity, equal opportunity, and disparate impact
- **Interactive Dashboard**: Visualize bias patterns with charts and risk alerts
- **Bias Mitigation Tools**: Apply reweighing, sampling, and threshold adjustments
- **Explainability Integration**: SHAP/LIME explanations with group-wise analysis
- **Automated Alerts**: Flag high-risk bias cases with human-readable reports
- **PDF Report Generation**: Professional reports with metrics, graphs, and recommendations

### Advanced Features
- AI-powered fairness recommendations
- Auto-detection of sensitive attributes
- Fairness score leaderboard
- API for CI/CD integration
- Real-time bias monitoring simulation

## 🏗️ Architecture

```
/
├── backend/           # Python FastAPI server
│   ├── main.py       # API endpoints
│   ├── bias_detection.py
│   ├── fairness_metrics.py
│   ├── mitigation.py
│   ├── explainability.py
│   └── report_generator.py
├── frontend/         # React dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   └── public/
├── data/            # Sample datasets
├── models/          # Trained models
└── reports/         # Generated reports
```

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- Pandas, NumPy, Scikit-learn
- SHAP, LIME
- FPDF (PDF generation)

**Frontend:**
- React 18
- Tailwind CSS
- Recharts (visualization)
- Axios (API calls)

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- pip and npm

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The dashboard will be available at `http://localhost:3000`

### 3. Sample Data

Sample datasets are provided in the `data/` directory:
- `hiring_dataset.csv`: Hiring decisions with gender bias
- `loan_dataset.csv`: Loan approvals with demographic data
- `healthcare_dataset.csv`: Medical diagnoses with race/ethnicity

## 📖 Usage

### Dataset Analysis
1. Upload a CSV or Excel file containing your dataset
2. The system automatically detects sensitive attributes (gender, race, age, etc.)
3. View distribution analysis and fairness metrics
4. Identify representation imbalances and discrimination patterns

### Model Analysis
1. Upload a trained ML model (joblib format)
2. Upload corresponding test data
3. Analyze predictions across demographic groups
4. Review confusion matrices and performance differences

### Bias Mitigation
1. Select from available mitigation techniques:
   - **Reweighing**: Adjust sample weights for balanced outcomes
   - **Oversampling**: Increase underrepresented group samples
   - **Undersampling**: Reduce overrepresented group samples
   - **Threshold Adjustment**: Modify decision thresholds for fairness

### Explainability
1. Choose SHAP or LIME explanation method
2. View global and group-wise feature importance
3. Identify if sensitive attributes influence predictions
4. Get recommendations for model improvement

### Report Generation
1. Generate comprehensive PDF reports
2. Include all analysis results, visualizations, and recommendations
3. Share with stakeholders or regulatory bodies

## 🎯 Fairness Metrics

The system calculates industry-standard fairness metrics:

- **Statistical Parity**: Equal acceptance rates across groups
- **Equal Opportunity**: Equal true positive rates
- **Equalized Odds**: Equal TPR and FPR across groups
- **Disparate Impact**: Ratio of acceptance rates between groups

## 🔍 API Endpoints

- `POST /analyze-dataset`: Analyze dataset for bias
- `POST /analyze-model`: Evaluate model fairness
- `POST /calculate-metrics`: Compute fairness metrics
- `POST /mitigate-bias`: Apply bias mitigation
- `POST /explain-model`: Generate model explanations
- `POST /generate-report`: Create PDF report

## 📊 Sample Output

### Fairness Score
- 0-100 scale indicating overall model fairness
- Color-coded risk levels (green/yellow/red)
- Based on multiple fairness metrics

### Bias Alerts
- "Women are 35% less likely to be approved for loans"
- "African-American applicants have 22% lower approval rates"
- "Model relies heavily on gender for hiring decisions"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is designed to assist in fairness auditing but does not guarantee perfectly fair outcomes. Fairness is context-dependent and should be evaluated by domain experts. Always consider legal, ethical, and business implications when deploying AI systems.

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the documentation
- Review sample datasets for guidance

---

**Built with ❤️ for ethical AI development**