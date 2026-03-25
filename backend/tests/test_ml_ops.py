import pytest
import pandas as pd
from app.ml_ops import DataValidator, DriftDetector

def test_data_validation():
    features = ["f1", "f2"]
    valid_data = {"f1": 10.0, "f2": 20.0}
    invalid_data = {"f1": 10.0}
    
    assert DataValidator.validate_schema(valid_data, features) is True
    assert DataValidator.validate_schema(invalid_data, features) is False

def test_drift_detection():
    # Detect drift between two distributions
    s1 = pd.Series([10, 11, 12, 10, 11] * 20)
    s2 = pd.Series([50, 51, 52, 50, 51] * 20)
    
    assert DriftDetector.detect_distribution_drift(s1, s2) is True
    assert DriftDetector.detect_distribution_drift(s1, s1) is False
