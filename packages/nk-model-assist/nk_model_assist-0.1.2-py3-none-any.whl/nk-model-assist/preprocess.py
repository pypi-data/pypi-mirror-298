from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.utils import resample
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(data, target_feature, algorithm, preprocessing_steps=None, feature_selection=None, 
                    numeric_impute_strategy='mean', categorical_impute_strategy='constant', fill_value='missing'):
    """
    Preprocess the dataset based on user input.

    Parameters:
    data (pd.DataFrame): The dataset to preprocess.
    target_feature (str): The target feature for the model.
    algorithm (str): The algorithm to use for preprocessing.
    preprocessing_steps (list): List of preprocessing steps to apply.
    feature_selection (list): List of features to include or exclude.
    numeric_impute_strategy (str): Strategy for imputing missing numeric values. Default is 'mean'.
    categorical_impute_strategy (str): Strategy for imputing missing categorical values. Default is 'constant'.
    fill_value (str): Fill value for imputing missing categorical values when strategy is 'constant'. Default is 'missing'.

    Returns:
    np.ndarray: Preprocessed features.
    pd.Series: Target feature.
    """
    logging.info(f"Preprocessing data with target feature '{target_feature}' using algorithm '{algorithm}'")
    
    try:
        if feature_selection:
            missing_features = [feature for feature in feature_selection if feature not in data.columns]
            if missing_features:
                raise ValueError(f"Selected features not found in the dataset: {missing_features}")
            data = data[feature_selection]
            logging.info(f"Selected features: {feature_selection}")

        if target_feature not in data.columns:
            raise ValueError(f"Target feature '{target_feature}' not found in the dataset")

        # Separate features and target
        X = data.drop(columns=[target_feature])
        y = data[target_feature]

        # Handle unexpected data types
        X = X.select_dtypes(include=['number', 'object'])
        logging.info(f"Data types after selection: {X.dtypes}")

        # Define preprocessing steps
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
        categorical_features = X.select_dtypes(include=['object']).columns

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy=numeric_impute_strategy)),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy=categorical_impute_strategy, fill_value=fill_value)),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # Apply preprocessing steps
        X_preprocessed = preprocessor.fit_transform(X)

        # Handle specific algorithm requirements
        if algorithm in ['Linear regression', 'Logistic regression', 'SVM algorithm']:
            # These algorithms require scaled features
            X_preprocessed = StandardScaler().fit_transform(X_preprocessed)
        elif algorithm in ['Decision tree', 'Random forest algorithm']:
            # These algorithms can handle unscaled features
            pass
        elif algorithm in ['KNN algorithm', 'K-means']:
            # These algorithms benefit from scaled features
            X_preprocessed = StandardScaler().fit_transform(X_preprocessed)
        elif algorithm in ['Naive Bayes algorithm']:
            # Naive Bayes can handle categorical features directly
            pass
        elif algorithm in ['Dimensionality reduction algorithms']:
            # Apply dimensionality reduction techniques
            # Example: PCA
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            X_preprocessed = pca.fit_transform(X_preprocessed)
        elif algorithm in ['Gradient boosting algorithm', 'AdaBoosting algorithm']:
            # These algorithms can handle unscaled features
            pass

        # Handle imbalanced data
        if y.value_counts(normalize=True).max() > 0.9:
            logging.info("Handling imbalanced data")
            X_preprocessed, y = resample(X_preprocessed, y, 
                                         replace=True, 
                                         n_samples=len(y), 
                                         random_state=42, 
                                         stratify=y)

        logging.info("Preprocessing complete.")
        return X_preprocessed, y

    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        raise RuntimeError(f"Error during preprocessing: {e}")
