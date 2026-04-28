import numpy as np
from typing import Dict, List, Any

def calculate_fairness_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate comprehensive fairness metrics"""
    # Extract data
    predictions = np.array(data['predictions'])
    labels = np.array(data['labels'])
    sensitive_attr = np.array(data['sensitive_attribute'])
    
    unique_groups = np.unique(sensitive_attr)
    if len(unique_groups) != 2:
        return {'error': 'Fairness metrics require exactly 2 groups'}
    
    group1, group2 = unique_groups
    mask1 = sensitive_attr == group1
    mask2 = sensitive_attr == group2
    
    # Statistical Parity
    p1 = np.mean(predictions[mask1])
    p2 = np.mean(predictions[mask2])
    statistical_parity = p1 - p2
    
    # Equal Opportunity (TPR difference)
    tp1 = np.sum((predictions[mask1] == 1) & (labels[mask1] == 1))
    fn1 = np.sum((predictions[mask1] == 0) & (labels[mask1] == 1))
    tpr1 = tp1 / (tp1 + fn1) if (tp1 + fn1) > 0 else 0
    
    tp2 = np.sum((predictions[mask2] == 1) & (labels[mask2] == 1))
    fn2 = np.sum((predictions[mask2] == 0) & (labels[mask2] == 1))
    tpr2 = tp2 / (tp2 + fn2) if (tp2 + fn2) > 0 else 0
    
    equal_opportunity = tpr1 - tpr2
    
    # Equalized Odds (both TPR and FPR)
    fp1 = np.sum((predictions[mask1] == 1) & (labels[mask1] == 0))
    tn1 = np.sum((predictions[mask1] == 0) & (labels[mask1] == 0))
    fpr1 = fp1 / (fp1 + tn1) if (fp1 + tn1) > 0 else 0
    
    fp2 = np.sum((predictions[mask2] == 1) & (labels[mask2] == 0))
    tn2 = np.sum((predictions[mask2] == 0) & (labels[mask2] == 0))
    fpr2 = fp2 / (fp2 + tn2) if (fp2 + tn2) > 0 else 0
    
    equalized_odds_tpr = equal_opportunity
    equalized_odds_fpr = fpr1 - fpr2
    
    # Disparate Impact Ratio
    disparate_impact = p1 / p2 if p2 > 0 else float('inf')
    
    # Accuracy
    acc1 = np.mean(predictions[mask1] == labels[mask1])
    acc2 = np.mean(predictions[mask2] == labels[mask2])
    accuracy_difference = acc1 - acc2
    
    return {
        'statistical_parity': {
            'value': statistical_parity,
            'interpretation': f"Group {group1} has {abs(statistical_parity):.3f} {'higher' if statistical_parity > 0 else 'lower'} acceptance rate than group {group2}"
        },
        'equal_opportunity': {
            'value': equal_opportunity,
            'interpretation': f"Group {group1} has {abs(equal_opportunity):.3f} {'higher' if equal_opportunity > 0 else 'lower'} true positive rate than group {group2}"
        },
        'equalized_odds': {
            'tpr_difference': equalized_odds_tpr,
            'fpr_difference': equalized_odds_fpr,
            'interpretation': f"TPR difference: {equalized_odds_tpr:.3f}, FPR difference: {equalized_odds_fpr:.3f}"
        },
        'disparate_impact_ratio': {
            'value': disparate_impact,
            'interpretation': f"Group {group1} is {disparate_impact:.2f} times more likely to be accepted than group {group2}"
        },
        'accuracy_difference': {
            'value': accuracy_difference,
            'interpretation': f"Group {group1} has {abs(accuracy_difference):.3f} {'higher' if accuracy_difference > 0 else 'lower'} accuracy than group {group2}"
        },
        'groups': {
            'group1': str(group1),
            'group2': str(group2)
        }
    }

def calculate_fairness_score(metrics: Dict[str, Any]) -> float:
    """Calculate overall fairness score (0-100)"""
    # Simple scoring based on absolute differences
    scores = []
    
    if 'statistical_parity' in metrics:
        scores.append(1 - min(abs(metrics['statistical_parity']['value']), 1))
    
    if 'equal_opportunity' in metrics:
        scores.append(1 - min(abs(metrics['equal_opportunity']['value']), 1))
    
    if 'equalized_odds' in metrics:
        tpr_diff = abs(metrics['equalized_odds']['tpr_difference'])
        fpr_diff = abs(metrics['equalized_odds']['fpr_difference'])
        scores.append(1 - min((tpr_diff + fpr_diff) / 2, 1))
    
    if 'disparate_impact_ratio' in metrics:
        di = metrics['disparate_impact_ratio']['value']
        if di > 1:
            di = 1/di  # Make it symmetric
        scores.append(di)
    
    if scores:
        avg_score = np.mean(scores)
        return max(0, min(100, avg_score * 100))
    else:
        return 50  # Neutral score