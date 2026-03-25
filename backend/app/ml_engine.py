import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import logging
from datetime import datetime

logger = logging.getLogger("EcoTrack-ML")

class MLEngine:
    def __init__(self, experiment_name="EcoTrack-Forecasting"):
        self.experiment_name = experiment_name
        mlflow.set_experiment(self.experiment_name)

    def train_arima(self, series: pd.Series, order=(5, 1, 0)):
        """ Trains an ARIMA model for time-series forecasting. """
        try:
            model = ARIMA(series, order=order)
            model_fit = model.fit()
            return model_fit
        except Exception as e:
            logger.error(f"ARIMA Training Error: {e}")
            return None

    def train_xgboost(self, X: pd.DataFrame, y: pd.Series):
        """ Trains an XGBoost regressor for multivariate prediction. """
        try:
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                objective='reg:squarederror'
            )
            model.fit(X, y)
            return model
        except Exception as e:
            logger.error(f"XGBoost Training Error: {e}")
            return None

    def evaluate_and_log(self, model_name: str, y_true: np.ndarray, y_pred: np.ndarray, params: dict):
        """ Logs metrics and parameters to MLflow. """
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        
        with mlflow.start_run(run_name=f"{model_name}-{datetime.now().strftime('%Y%m%d-%H%M')}"):
            mlflow.log_params(params)
            mlflow.log_metric("rmse", rmse)
            logger.info(f"Logged {model_name} to MLflow. RMSE: {rmse}")
            
        return rmse

    def compare_models(self, data: pd.DataFrame, target_col: str):
        """ 
        Heuristic-based model comparison. 
        In a real scenario, we'd use a validation set.
        """
        # Simplified: ARIMA for time-only, XGBoost for features
        # We'll stick to a strategy-based selection for now
        if len(data.columns) > 2:
            return "xgboost"
        return "arima"

    def retrain(self, history_data: pd.DataFrame, target_col: str):
        """ Re-trains specialized models on the full history. """
        logger.info(f"🚀 Re-training on {len(history_data)} records...")
        # 1. XGBoost Retraining
        X = history_data.drop(columns=[target_col])
        y = history_data[target_col]
        
        # Log to MLflow
        with mlflow.start_run(run_name=f"Retrain-XGB-{datetime.now().strftime('%Y%b%d')}"):
             new_xgb = self.train_xgboost(X, y)
             mlflow.log_param("data_size", len(history_data))
             mlflow.set_tag("retrain", "AUTOMATED-v9")
             
        return new_xgb

def get_forecast_ensemble(history: pd.Series, steps: int = 12):
    """ Returns a forecast using an ensemble of ARIMA and Exponential Smoothing. """
    # Simple ensemble: weighted average
    try:
        # 1. ARIMA
        arima_model = ARIMA(history, order=(1, 1, 1)).fit()
        arima_fc = arima_model.forecast(steps=steps)
        
        # 2. Naive Trend (Fallback)
        last_val = history.iloc[-1]
        trend = (history.iloc[-1] - history.iloc[0]) / len(history)
        naive_fc = [last_val + (i * trend) for i in range(1, steps + 1)]
        
        # Weighted average (70% ARIMA, 30% Naive)
        ensemble_fc = (arima_fc * 0.7) + (np.array(naive_fc) * 0.3)
        return ensemble_fc.tolist()
    except Exception as e:
        logger.warning(f"Ensemble failure, using naive fallback: {e}")
        return [history.mean()] * steps
