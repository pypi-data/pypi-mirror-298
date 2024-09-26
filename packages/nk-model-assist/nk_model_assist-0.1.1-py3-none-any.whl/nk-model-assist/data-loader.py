# nk_model_assist/data_loader.py
import pandas as pd
import os
from nk_model_assist.preprocess import preprocess_data
from nk_model_assist.data_checker import check_data_suitability
from nk_model_assist.modelling import train_model, inference


def load_dataset(file_path, delimiter=',', header='infer', na_values=None):
    """
    Load dataset from the given file path and validate it.

    Parameters:
    file_path (str): Path to the dataset file.
    delimiter (str): Delimiter to use for the CSV file. Default is ','.
    header (int, list of int, str): Row number(s) to use as the column names. Default is 'infer'.
    na_values (scalar, str, list-like, or dict): Additional strings to recognize as NA/NaN.

    Returns:
    pd.DataFrame: Loaded dataset.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")
    
    if not file_path.endswith('.csv'):
        raise ValueError("File is not a CSV.")

    try:
        data = pd.read_csv(file_path, delimiter=delimiter, header=header, na_values=na_values)
        print(f"Dataset loaded successfully from {file_path}")
        return data
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")


def process_dataset(file_path, target_feature, algorithm, delimiter=',', header='infer', na_values=None, preprocessing_steps=None, feature_selection=None, save_model=False, model_path='model.pkl'):
    """
    Load and preprocess the dataset based on user input.

    Parameters:
    file_path (str): Path to the dataset file.
    target_feature (str): The target feature for the model.
    algorithm (str): The algorithm to use for preprocessing.
    delimiter (str): Delimiter to use for the CSV file. Default is ','.
    header (int, list of int, str): Row number(s) to use as the column names. Default is 'infer'.
    na_values (scalar, str, list-like, or dict): Additional strings to recognize as NA/NaN.
    preprocessing_steps (list): List of preprocessing steps to apply.
    feature_selection (list): List of features to include or exclude.
    save_model (bool): Whether to save the trained model to a file. Default is False.
    model_path (str): Path to save the trained model. Default is 'model.pkl'.
    """
    data = load_dataset(file_path, delimiter, header, na_values)
    X_preprocessed, y = preprocess_data(data, target_feature, algorithm, preprocessing_steps, feature_selection)
    
    if check_data_suitability(X_preprocessed, y):
        print("Data is suitable for model training.")
        results = train_model(X_preprocessed, y, algorithm, save_model, model_path)
        print("Model training complete.")
        return results
    else:
        print("Data is not suitable for model training.")
        return None

