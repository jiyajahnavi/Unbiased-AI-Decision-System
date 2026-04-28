from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
import os
from bias_detection import analyze_dataset_bias, analyze_model_bias
from fairness_metrics import calculate_fairness_metrics
from mitigation import apply_mitigation

app = FastAPI(title="Unbiased AI Decision: Fairness Auditor", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-dataset")
async def analyze_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported")
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        result = analyze_dataset_bias(df)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-model")
async def analyze_model(model_file: UploadFile = File(...), data_file: UploadFile = File(...)):
    try:
        # Load model (assuming joblib format)
        import joblib
        model = joblib.load(model_file.file)
        
        # Load data
        if data_file.filename.endswith('.csv'):
            df = pd.read_csv(data_file.file)
        else:
            df = pd.read_excel(data_file.file)
        
        result = analyze_model_bias(model, df)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-metrics")
async def calculate_metrics(data: Dict[str, Any]):
    try:
        result = calculate_fairness_metrics(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel


class MitigationRequest(BaseModel):
    data: list[Dict[str, Any]]
    sensitive_attribute: str
    target_column: str | None = None
    method: str


@app.post("/mitigate-bias")
async def mitigate_bias(request: MitigationRequest):
    try:
        result = apply_mitigation(request.dict(), request.method)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain-model")
async def explain_model_endpoint(model_file: UploadFile = File(...), data_file: UploadFile = File(...)):
    try:
        import joblib
        from explainability import explain_model

        model = joblib.load(model_file.file)
        
        if data_file.filename.endswith('.csv'):
            df = pd.read_csv(data_file.file)
        else:
            df = pd.read_excel(data_file.file)
        
        result = explain_model(model, df)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-report")
async def generate_report_endpoint(data: Dict[str, Any]):
    try:
        from report_generator import generate_report

        report_path = generate_report(data)
        return FileResponse(report_path, media_type='application/pdf', filename='fairness_report.pdf')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Fairness Auditor API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)