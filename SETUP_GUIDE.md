# Unbiased AI Decision: Fairness Auditor Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git

## Step-by-Step Setup

### 1. Clone or Download the Project
```bash
cd your-desired-directory
# If cloning: git clone <repository-url>
# If downloaded: unzip the project files
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Alternative: Install Core Packages
If requirements.txt installation fails:
```bash
pip install fastapi uvicorn pandas numpy scikit-learn matplotlib seaborn fpdf joblib xgboost
```

#### Optional: Install Advanced Libraries
```bash
pip install shap lime aif360 fairlearn
```

#### Train Sample Models (Optional)
```bash
python train_sample_models.py
```

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd ../frontend
npm install
```

#### Configure Tailwind CSS
```bash
npx tailwindcss init -p
```
The tailwind.config.js is already configured.

### 4. Start the Application

#### Terminal 1: Start Backend
```bash
cd backend
python main.py
```
Backend will run on http://localhost:8000

#### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```
Frontend will run on http://localhost:3000

### 5. Access the Application
Open your browser and go to http://localhost:3000

## Demo Walkthrough

### 1. Dataset Analysis
1. Click on "Dataset Analysis" tab
2. Upload one of the sample datasets:
   - `data/hiring_dataset.csv` - Hiring decisions
   - `data/loan_dataset.csv` - Loan approvals
   - `data/healthcare_dataset.csv` - Medical diagnoses
3. Click "Analyze Dataset"
4. View:
   - Detected sensitive attributes
   - Distribution analysis
   - Fairness metrics (Disparate Impact, Statistical Parity)
   - Fairness score

### 2. Model Analysis
1. Click on "Model Analysis" tab
2. Upload a trained model (joblib format) or use sample models from `models/` directory
3. Upload corresponding test data
4. Click "Analyze Model"
5. View:
   - Confusion matrices by demographic group
   - Accuracy differences
   - FPR/FNR differences

### 3. Fairness Dashboard
1. Click on "Fairness Dashboard" tab
2. View interactive charts:
   - Distribution visualizations
   - Fairness metrics comparison
   - Overall fairness score
   - Risk indicators

### 4. Bias Mitigation
1. Click on "Bias Mitigation" tab
2. Select a mitigation method:
   - Reweighing
   - Oversampling
   - Undersampling
   - Threshold Adjustment
3. Click "Apply Mitigation"
4. View before/after comparisons

### 5. Explainability
1. Click on "Explainability" tab
2. Select SHAP or LIME
3. Click "Generate Explanations"
4. View:
   - Global feature importance
   - Group-wise explanations
   - Sensitive attribute analysis

### 6. Report Generation
1. Click on "Generate Report" tab
2. Click "Generate PDF Report"
3. Download the comprehensive fairness audit report

## Sample Datasets Description

### Hiring Dataset (`data/hiring_dataset.csv`)
- Features: gender, age, education, years_experience, score
- Target: hired (0/1)
- Sensitive attributes: gender, age

### Loan Dataset (`data/loan_dataset.csv`)
- Features: gender, age, income, credit_score, loan_amount
- Target: approved (0/1)
- Sensitive attributes: gender, age

### Healthcare Dataset (`data/healthcare_dataset.csv`)
- Features: gender, age, race, income, smoker
- Target: diagnosis (0/1)
- Sensitive attributes: gender, age, race

## Troubleshooting

### Backend Issues
- **Port 8000 already in use**: Change port in main.py
- **Import errors**: Install missing packages manually
- **Model loading errors**: Ensure models are in joblib format

### Frontend Issues
- **Port 3000 already in use**: `npm start` will auto-select another port
- **API connection errors**: Ensure backend is running on port 8000
- **Build errors**: Clear node_modules and reinstall

### Common Errors
- **CORS errors**: Backend allows all origins by default
- **File upload errors**: Check file format (CSV/Excel for data, joblib for models)
- **Memory errors**: Reduce dataset size or use smaller models

## API Documentation

The backend provides a FastAPI automatic API documentation at:
http://localhost:8000/docs

## Development

### Adding New Features
1. Backend: Add functions to respective modules
2. Frontend: Create new components in `src/components/`
3. Update API endpoints in `main.py`
4. Update UI routing in `App.js`

### Testing
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Production Deployment

### Backend
```bash
# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Using gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
npm run build
# Serve build/ directory with any static server
```

## Support

For issues or questions:
1. Check this setup guide
2. Review error messages in terminal
3. Check browser developer console
4. Open an issue on the project repository

## License

This project is licensed under the MIT License.