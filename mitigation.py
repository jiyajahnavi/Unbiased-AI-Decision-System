import pandas as pd
import numpy as np
from sklearn.utils import resample
from typing import Dict, List, Any

def apply_mitigation(data: Dict[str, Any], method: str) -> Dict[str, Any]:
    """Apply bias mitigation technique"""
    df = pd.DataFrame(data['data'])
    sensitive_attr = data['sensitive_attribute']
    target_col = data.get('target_column')

    if target_col not in df.columns:
        target_col = find_target_column(df)
    
    if target_col is None:
        return {'error': 'No target column found for mitigation'}
    
    if method == 'reweighing':
        return apply_reweighing(df, sensitive_attr, target_col)
    elif method == 'oversampling':
        return apply_oversampling(df, sensitive_attr, target_col)
    elif method == 'undersampling':
        return apply_undersampling(df, sensitive_attr, target_col)
    elif method == 'threshold_adjustment':
        return apply_threshold_adjustment(data)
    else:
        return {'error': f'Method {method} not implemented'}

def apply_reweighing(df: pd.DataFrame, sensitive_attr: str, target_col: str) -> Dict[str, Any]:
    """Apply reweighing technique"""
    # Calculate weights
    total_samples = len(df)
    group_weights = {}
    
    for group in df[sensitive_attr].unique():
        group_data = df[df[sensitive_attr] == group]
        group_size = len(group_data)
        positive_rate = group_data[target_col].mean()
        
        # Weight = (total/group_size) * (overall_positive_rate / group_positive_rate)
        overall_positive_rate = df[target_col].mean()
        
        if positive_rate > 0:
            weight = (total_samples / group_size) * (overall_positive_rate / positive_rate)
        else:
            weight = 1.0
            
        group_weights[group] = weight
    
    # Apply weights
    df_weighted = df.copy()
    df_weighted['weight'] = df[sensitive_attr].map(group_weights)
    
    return {
        'method': 'reweighing',
        'weights': group_weights,
        'data': df_weighted.to_dict('records'),
        'description': 'Reweighed the dataset to balance group outcomes'
    }

def apply_oversampling(df: pd.DataFrame, sensitive_attr: str, target_col: str) -> Dict[str, Any]:
    """Apply oversampling to balance underrepresented groups"""
    groups = df[sensitive_attr].unique()
    max_group_size = df[sensitive_attr].value_counts().max()
    
    balanced_dfs = []
    
    for group in groups:
        group_data = df[df[sensitive_attr] == group]
        if len(group_data) < max_group_size:
            # Oversample
            oversampled = resample(group_data, 
                                 replace=True, 
                                 n_samples=max_group_size, 
                                 random_state=42)
            balanced_dfs.append(oversampled)
        else:
            balanced_dfs.append(group_data)
    
    balanced_df = pd.concat(balanced_dfs).reset_index(drop=True)
    
    return {
        'method': 'oversampling',
        'original_sizes': df[sensitive_attr].value_counts().to_dict(),
        'balanced_sizes': balanced_df[sensitive_attr].value_counts().to_dict(),
        'data': balanced_df.to_dict('records'),
        'description': 'Oversampled underrepresented groups to balance dataset'
    }

def apply_undersampling(df: pd.DataFrame, sensitive_attr: str, target_col: str) -> Dict[str, Any]:
    """Apply undersampling to balance overrepresented groups"""
    groups = df[sensitive_attr].unique()
    min_group_size = df[sensitive_attr].value_counts().min()
    
    balanced_dfs = []
    
    for group in groups:
        group_data = df[df[sensitive_attr] == group]
        if len(group_data) > min_group_size:
            # Undersample
            undersampled = resample(group_data, 
                                  replace=False, 
                                  n_samples=min_group_size, 
                                  random_state=42)
            balanced_dfs.append(undersampled)
        else:
            balanced_dfs.append(group_data)
    
    balanced_df = pd.concat(balanced_dfs).reset_index(drop=True)
    
    return {
        'method': 'undersampling',
        'original_sizes': df[sensitive_attr].value_counts().to_dict(),
        'balanced_sizes': balanced_df[sensitive_attr].value_counts().to_dict(),
        'data': balanced_df.to_dict('records'),
        'description': 'Undersampled overrepresented groups to balance dataset'
    }

def find_target_column(df: pd.DataFrame) -> str | None:
    target_candidates = ['target', 'label', 'outcome', 'approved', 'hired', 'diagnosis']
    for col in df.columns:
        if col.lower() in target_candidates:
            return col
    return None


def apply_threshold_adjustment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply threshold adjustment for fairness"""
    predictions = np.array(data['predictions'])
    sensitive_attr = np.array(data['sensitive_attribute'])
    
    unique_groups = np.unique(sensitive_attr)
    if len(unique_groups) != 2:
        return {'error': 'Threshold adjustment requires exactly 2 groups'}
    
    group1, group2 = unique_groups
    mask1 = sensitive_attr == group1
    mask2 = sensitive_attr == group2
    
    # Find thresholds that achieve equal acceptance rates
    probs = np.array(data['probabilities'])
    
    # Simple approach: adjust threshold for one group
    current_threshold = 0.5
    target_rate = (np.mean(predictions[mask1]) + np.mean(predictions[mask2])) / 2
    
    # Adjust threshold for group2 to match group1's acceptance rate
    group1_rate = np.mean(predictions[mask1])
    
    # Find threshold for group2 that gives similar rate
    sorted_indices = np.argsort(probs[mask2])[::-1]
    cumulative = np.cumsum(np.ones(len(sorted_indices)))
    rates = cumulative / len(sorted_indices)
    
    # Find closest rate to group1_rate
    idx = np.argmin(np.abs(rates - group1_rate))
    new_threshold = probs[mask2][sorted_indices[idx]] if idx < len(sorted_indices) else 0.5
    
    adjusted_predictions = predictions.copy()
    adjusted_predictions[mask2] = (probs[mask2] >= new_threshold).astype(int)
    
    return {
        'method': 'threshold_adjustment',
        'original_rates': {
            str(group1): float(np.mean(predictions[mask1])),
            str(group2): float(np.mean(predictions[mask2]))
        },
        'adjusted_rates': {
            str(group1): float(np.mean(adjusted_predictions[mask1])),
            str(group2): float(np.mean(adjusted_predictions[mask2]))
        },
        'new_threshold_group2': float(new_threshold),
        'predictions': adjusted_predictions.tolist(),
        'description': f'Adjusted decision threshold for group {group2} to achieve similar acceptance rates'
    }