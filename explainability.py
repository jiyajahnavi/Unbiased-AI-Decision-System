import pandas as pd
import numpy as np
from typing import Dict, List, Any
import shap
import lime
import lime.lime_tabular

def explain_model(model, df: pd.DataFrame, method: str = 'shap') -> Dict[str, Any]:
    """Explain model using SHAP or LIME"""
    # Assume last column is target
    target_col = df.columns[-1]
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Detect sensitive attributes
    from bias_detection import detect_sensitive_attributes
    sensitive_attrs = detect_sensitive_attributes(df)
    
    if method == 'shap':
        return explain_with_shap(model, X, sensitive_attrs)
    elif method == 'lime':
        return explain_with_lime(model, X, sensitive_attrs)
    else:
        return {'error': f'Method {method} not supported'}

def explain_with_shap(model, X: pd.DataFrame, sensitive_attrs: List[str]) -> Dict[str, Any]:
    """Explain model using SHAP"""
    try:
        # Create explainer
        if hasattr(model, 'predict_proba'):
            explainer = shap.Explainer(model.predict_proba, X)
        else:
            explainer = shap.Explainer(model.predict, X)
        
        # Calculate SHAP values for a sample
        sample_size = min(100, len(X))
        X_sample = X.sample(sample_size, random_state=42)
        
        shap_values = explainer(X_sample)
        
        # Global feature importance
        feature_importance = {}
        for i, feature in enumerate(X.columns):
            importance = np.mean(np.abs(shap_values.values[:, i]))
            feature_importance[feature] = float(importance)
        
        # Check if sensitive features are important
        sensitive_importance = {}
        for attr in sensitive_attrs:
            if attr in feature_importance:
                sensitive_importance[attr] = feature_importance[attr]
        
        # Group-wise explanations
        group_explanations = {}
        if sensitive_attrs:
            sensitive_attr = sensitive_attrs[0]  # Use first one
            if sensitive_attr in X.columns:
                groups = X[sensitive_attr].unique()
                for group in groups:
                    group_mask = X[sensitive_attr] == group
                    if group_mask.sum() > 10:  # Enough samples
                        X_group = X[group_mask].sample(min(50, group_mask.sum()), random_state=42)
                        shap_group = explainer(X_group)
                        
                        group_importance = {}
                        for i, feature in enumerate(X.columns):
                            importance = np.mean(np.abs(shap_group.values[:, i]))
                            group_importance[feature] = float(importance)
                        
                        group_explanations[str(group)] = group_importance
        
        return {
            'method': 'shap',
            'global_feature_importance': feature_importance,
            'sensitive_feature_importance': sensitive_importance,
            'group_explanations': group_explanations,
            'description': 'SHAP-based feature importance analysis'
        }
        
    except Exception as e:
        return {'error': f'SHAP explanation failed: {str(e)}'}

def explain_with_lime(model, X: pd.DataFrame, sensitive_attrs: List[str]) -> Dict[str, Any]:
    """Explain model using LIME"""
    try:
        # Create LIME explainer
        explainer = lime.lime_tabular.LimeTabularExplainer(
            X.values, 
            feature_names=X.columns.tolist(),
            class_names=['Negative', 'Positive'] if hasattr(model, 'classes_') else None,
            discretize_continuous=True
        )
        
        # Explain a few samples
        sample_size = min(10, len(X))
        explanations = []
        
        for idx in np.random.choice(len(X), sample_size, replace=False):
            exp = explainer.explain_instance(X.iloc[idx].values, model.predict_proba)
            
            feature_importance = {}
            for feature, importance in exp.as_list():
                feature_importance[feature] = importance
            
            explanations.append({
                'sample_index': int(idx),
                'feature_importance': feature_importance,
                'prediction': float(model.predict_proba([X.iloc[idx].values])[0][1])
            })
        
        # Check sensitive features in explanations
        sensitive_in_explanations = {}
        for attr in sensitive_attrs:
            if attr in X.columns:
                attr_importances = [exp['feature_importance'].get(attr, 0) for exp in explanations]
                sensitive_in_explanations[attr] = {
                    'mean_importance': float(np.mean(attr_importances)),
                    'max_importance': float(np.max(attr_importances))
                }
        
        return {
            'method': 'lime',
            'sample_explanations': explanations,
            'sensitive_features': sensitive_in_explanations,
            'description': 'LIME-based local explanations for sample predictions'
        }
        
    except Exception as e:
        return {'error': f'LIME explanation failed: {str(e)}'}

def detect_discriminatory_features(explanation_result: Dict[str, Any], threshold: float = 0.1) -> List[str]:
    """Detect features that might be discriminatory based on explanations"""
    discriminatory = []
    
    if 'global_feature_importance' in explanation_result:
        for feature, importance in explanation_result['global_feature_importance'].items():
            if importance > threshold:
                discriminatory.append(feature)
    
    return discriminatory