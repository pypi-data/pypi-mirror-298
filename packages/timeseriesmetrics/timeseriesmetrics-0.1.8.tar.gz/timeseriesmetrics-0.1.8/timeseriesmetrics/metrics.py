import numpy as np
import pandas as pd

def ensure_numpy_array(arr):
    """
    Helper function to ensure that the input is converted to a numpy array.
    
    Parameters:
        arr: Can be a list, pd.Series, or numpy array.
        
    Returns:
        numpy array: The converted array.
    """
    if isinstance(arr, pd.Series):
        return arr.to_numpy()
    elif isinstance(arr, list):
        return np.array(arr)
    return arr

def theil(y_true, y_pred):
    """
    Theil's U metric to compare model performance against a Random Walk model.
    
    Parameters:
        y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
        y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

    Returns:
        float: Theil's U value.
    """
    y_true = ensure_numpy_array(y_true)
    y_pred = ensure_numpy_array(y_pred)

    if len(y_true) < 2 or len(y_pred) < 2:
        return np.nan

    # Naive prediction: one-period shift
    naive_pred = np.roll(y_true, 1)[1:]
    y_true = y_true[1:]  # Remove the first value (no prediction)
    y_pred = y_pred[1:]  # Remove the first value (no prediction)

    numerator = np.sum((y_true - y_pred) ** 2)
    denominator = np.sum((y_true - naive_pred) ** 2)

    return numerator / denominator if denominator != 0 else np.nan


def mape(y_true, y_pred):
    """
    Mean Absolute Percentage Error (MAPE).
    
    Parameters:
        y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
        y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

    Returns:
        float: MAPE value.
    """
    y_true = ensure_numpy_array(y_true)
    y_pred = ensure_numpy_array(y_pred)

    # Avoid division by zero when true values are zero
    with np.errstate(divide='ignore', invalid='ignore'):
        percentage_errors = np.abs((y_true - y_pred) / y_true)
        percentage_errors = np.where(np.isfinite(percentage_errors), percentage_errors, np.nan)
    
    return np.nanmean(percentage_errors) * 100


def arv(y_true, y_pred):
    """
    Average Relative Variance (ARV).
    
    Parameters:
        y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
        y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

    Returns:
        float: ARV value.
    """
    y_true = ensure_numpy_array(y_true)
    y_pred = ensure_numpy_array(y_pred)

    y_mean = np.mean(y_true)

    numerator = np.sum((y_true - y_pred) ** 2)
    denominator = np.sum((y_true - y_mean) ** 2)

    return numerator / denominator if denominator != 0 else np.nan


def disagreement_index(y_true, y_pred):
    """
    Index of Disagreement (ID).
    
    Parameters:
        y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
        y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

    Returns:
        float: ID value.
    """
    y_true = ensure_numpy_array(y_true)
    y_pred = ensure_numpy_array(y_pred)

    y_mean = np.mean(y_pred)

    numerator = np.sum((y_pred - y_true) ** 2)
    denominator = np.sum((np.abs(y_pred - y_mean) + np.abs(y_true - y_mean)) ** 2)

    return numerator / denominator if denominator != 0 else np.nan


def wpocid(y_true, y_pred):
    """
    WPOCID.

    Parameters:
        y_true: Actual values of the time series (can be list, pd.Series, or numpy array).
        y_pred: Predicted values by the model (can be list, pd.Series, or numpy array).

    Returns:
        float: WPOCID value.
    """
    y_true = ensure_numpy_array(y_true)
    y_pred = ensure_numpy_array(y_pred)

    sum_D_t = 0

    for t in range(1, len(y_true)):
        if (y_true[t] - y_true[t-1]) * (y_pred[t] - y_pred[t-1]) >= 0:
            sum_D_t += 1

    N = len(y_true)
    return 1 - (sum_D_t / (N - 1)) if N > 1 else np.nan
