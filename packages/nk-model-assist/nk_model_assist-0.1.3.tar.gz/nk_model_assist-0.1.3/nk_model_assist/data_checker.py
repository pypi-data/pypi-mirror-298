import numpy as np
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_data_suitability(X, y, min_samples=10, min_classes=2):
    """
    Check if the preprocessed data is suitable for model training.

    Parameters:
    X (np.ndarray): Preprocessed features.
    y (pd.Series): Target feature.
    min_samples (int): Minimum number of samples required for training. Default is 10.
    min_classes (int): Minimum number of classes required for classification problems. Default is 2.

    Returns:
    bool: True if the data is suitable for model training, False otherwise.
    """
    try:
        # Check for missing values
        if np.any(np.isnan(X)) or np.any(pd.isnull(y)):
            logging.error("Data contains missing values.")
            return False

        # Check data types
        if not isinstance(X, np.ndarray) or not isinstance(y, pd.Series):
            logging.error("Incorrect data types. X should be np.ndarray and y should be pd.Series.")
            return False

        # Check feature-target consistency
        if X.shape[0] != len(y):
            logging.error("Mismatch between number of samples in features and target.")
            return False

        # Check for sufficient data
        if X.shape[0] < min_samples:
            logging.error(f"Insufficient data. At least {min_samples} samples are required.")
            return False

        # Check for class balance in classification problems
        if y.nunique() < min_classes:
            logging.error(f"Insufficient number of classes. At least {min_classes} classes are required.")
            return False

        class_counts = y.value_counts()
        if class_counts.min() / class_counts.max() < 0.1:
            logging.warning("Imbalanced classes detected. Consider using techniques to handle class imbalance.")

        logging.info("Data is suitable for model training.")
        return True

    except Exception as e:
        logging.error(f"Error during data suitability check: {e}")
        return False