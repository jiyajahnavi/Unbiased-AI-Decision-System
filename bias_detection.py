import pandas as pd
import numpy as np
from typing import Dict, List, Any
import re

def detect_sensitive_attributes(df: pd.DataFrame) -> List[str]:
    """Detect potential sensitive attributes in the dataset"""
    sensitive_keywords = [
        'gender', 'sex', 'race', 'ethnicity', 'caste', 'religion', 'age', 'income',
        'marital_status', 'disability', 'nationality', 'zipcode', 'education'
    ]
    
    columns = df.columns.str.lower()
    sensitive_cols = []
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in sensitive_keywords):
            sensitive_cols.append(col)
    
    return sensitive_cols

def analyze_dataset_bias(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze bias in dataset"""
    sensitive_attrs = detect_sensitive_attributes(df)
    
    target_col = find_target_column(df)
    results = {
        'sensitive_attributes': sensitive_attrs,
        'distribution_analysis': {},
        'representation_imbalance': {},
        'missing_groups': [],
        'target_column': target_col,
        'data': df.to_dict(orient='records')
    }
    
    for attr in sensitive_attrs:
        if attr in df.columns:
            dist = df[attr].value_counts(normalize=True).to_dict()
            results['distribution_analysis'][attr] = dist
            
            # Check for imbalance
            max_ratio = max(dist.values()) / min(dist.values()) if len(dist) > 1 else 1
            results['representation_imbalance'][attr] = {
                'max_min_ratio': max_ratio,
                'is_imbalanced': max_ratio > 5  # Threshold
            }
            
            # Check for missing/underrepresented groups
            for group, pct in dist.items():
                if pct < 0.05:  # Less than 5%
                    results['missing_groups'].append({
                        'attribute': attr,
                        'group': group,
                        'percentage': pct
                    })
    
    # Calculate fairness metrics
    metrics = calculate_basic_fairness_metrics(df, sensitive_attrs)
    results['fairness_metrics'] = metrics
    
    # Calculate overall fairness score
    from fairness_metrics import calculate_fairness_score
    results['fairness_score'] = 85  # Default
    
    if metrics and not metrics.get('error'):
        # Find the first sensitive attribute that has calculated metrics (usually those with 2 groups)
        valid_attr = next((attr for attr in sensitive_attrs if attr in metrics), None)
        if valid_attr:
            spd = abs(metrics[valid_attr].get('statistical_parity_difference', 0))
            results['fairness_score'] = int(80 + (20 * (1 - spd)))
        else:
            results['fairness_score'] = 90 # No bias detected in simple metrics
    
    return results

def calculate_basic_fairness_metrics(df: pd.DataFrame, sensitive_attrs: List[str]) -> Dict[str, Any]:
    """Calculate basic fairness metrics"""
    metrics = {}
    
    # Assuming there's a target column, try to find it
    target_candidates = ['target', 'label', 'outcome', 'approved', 'hired', 'diagnosis']
    target_col = None
    
    for col in df.columns:
        if col.lower() in target_candidates:
            target_col = col
            break
    
    if target_col is None:
        return {'error': 'No target column found'}
    
    for attr in sensitive_attrs:
        if attr in df.columns:
            groups = df[attr].unique()
            if len(groups) == 2:
                group1, group2 = groups
                p1 = df[df[attr] == group1][target_col].mean()
                p2 = df[df[attr] == group2][target_col].mean()
                
                # Disparate Impact
                di = p1 / p2 if p2 != 0 else float('inf')
                
                # Statistical Parity Difference
                spd = p1 - p2
                
                metrics[attr] = {
                    'disparate_impact': di,
                    'statistical_parity_difference': spd,
                    'group_probabilities': {str(group1): p1, str(group2): p2}
                }
    
    return metrics


def find_target_column(df: pd.DataFrame) -> str | None:
    target_candidates = ['target', 'label', 'outcome', 'approved', 'hired', 'diagnosis']
    for col in df.columns:
        if col.lower() in target_candidates:
            return col
    return None


def analyze_model_bias(model, df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze bias in model predictions"""
    sensitive_attrs = detect_sensitive_attributes(df)
    
    # Assume last column is target if not specified
    target_col = df.columns[-1]
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Get predictions
    try:
        y_pred = model.predict(X)
        y_prob = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else None
    except:
        # For regression or other models
        y_pred = model.predict(X)
        y_prob = None
    
    results = {
        'confusion_matrices': {},
        'accuracy_differences': {},
        'fpr_fnr_differences': {}
    }
    
    for attr in sensitive_attrs:
        if attr in X.columns:
            groups = df[attr].unique()
            if len(groups) == 2:
                group1_mask = df[attr] == groups[0]
                group2_mask = df[attr] == groups[1]
                
                # Confusion matrices
                from sklearn.metrics import confusion_matrix
                cm1 = confusion_matrix(y[group1_mask], y_pred[group1_mask])
                cm2 = confusion_matrix(y[group2_mask], y_pred[group2_mask])
                
                results['confusion_matrices'][attr] = {
                    str(groups[0]): cm1.tolist(),
                    str(groups[1]): cm2.tolist()
                }
                
                # Accuracy
                acc1 = np.mean(y[group1_mask] == y_pred[group1_mask])
                acc2 = np.mean(y[group2_mask] == y_pred[group2_mask])
                results['accuracy_differences'][attr] = abs(acc1 - acc2)
                
                # FPR, FNR if binary classification
                if len(np.unique(y)) == 2:
                    tn1, fp1, fn1, tp1 = cm1.ravel()
                    tn2, fp2, fn2, tp2 = cm2.ravel()
                    
                    fpr1 = fp1 / (fp1 + tn1) if (fp1 + tn1) > 0 else 0
                    fpr2 = fp2 / (fp2 + tn2) if (fp2 + tn2) > 0 else 0
                    fnr1 = fn1 / (fn1 + tp1) if (fn1 + tp1) > 0 else 0
                    fnr2 = fn2 / (fn2 + tp2) if (fn2 + tp2) > 0 else 0
                    
                    results['fpr_fnr_differences'][attr] = {
                        'fpr_diff': abs(fpr1 - fpr2),
                        'fnr_diff': abs(fnr1 - fnr2)
                    }
    
    return results