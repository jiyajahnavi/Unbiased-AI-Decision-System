import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def create_sample_model(dataset_path, model_path):
    """Create and save a sample ML model with potential bias"""
    
    # Load dataset
    df = pd.read_csv(dataset_path)
    
    # Preprocess
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object', 'string']):
        df[col] = le.fit_transform(df[col])
    
    # Assume last column is target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    
    # Save test data
    test_data_path = model_path.replace('.joblib', '_test.csv')
    X_test['target'] = y_test
    X_test.to_csv(test_data_path, index=False)
    
    print(f"Model saved to {model_path}")
    print(f"Test data saved to {test_data_path}")
    
    return model

if __name__ == "__main__":
    # Create models for sample datasets
    datasets = [
        ('data/hiring_dataset.csv', 'models/hiring_model.joblib'),
        ('data/loan_dataset.csv', 'models/loan_model.joblib'),
        ('data/healthcare_dataset.csv', 'models/healthcare_model.joblib')
    ]
    
    for dataset, model in datasets:
        if os.path.exists(dataset):
            create_sample_model(dataset, model)