from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix, classification_report
import joblib

def train_model(X, y, algorithm, save_model=False, model_path='model.pkl'):
    """
    Train a model based on the specified algorithm.

    Parameters:
    X (np.ndarray): Preprocessed features.
    y (pd.Series): Target feature.
    algorithm (str): The algorithm to use for training.
    save_model (bool): Whether to save the trained model to a file. Default is False.
    model_path (str): Path to save the trained model. Default is 'model.pkl'.

    Returns:
    dict: A dictionary containing the trained model, accuracy, MSE, confusion matrix, and classification report.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Select and train the model based on the algorithm
    if algorithm == 'Linear regression':
        model = LinearRegression()
    elif algorithm == 'Logistic regression':
        model = LogisticRegression()
    elif algorithm == 'Decision tree':
        model = DecisionTreeClassifier()
    elif algorithm == 'SVM algorithm':
        model = SVC()
    elif algorithm == 'Naive Bayes algorithm':
        model = GaussianNB()
    elif algorithm == 'KNN algorithm':
        model = KNeighborsClassifier()
    elif algorithm == 'K-means':
        model = KMeans(n_clusters=3)  # Example: 3 clusters
    elif algorithm == 'Random forest algorithm':
        model = RandomForestClassifier()
    elif algorithm == 'Dimensionality reduction algorithms':
        model = PCA(n_components=2)  # Example: PCA with 2 components
    elif algorithm == 'Gradient boosting algorithm':
        model = GradientBoostingClassifier()
    elif algorithm == 'AdaBoosting algorithm':
        model = AdaBoostClassifier()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    results = {}

    if algorithm == 'Linear regression':
        mse = mean_squared_error(y_test, y_pred)
        results['mse'] = mse
        print(f"Mean Squared Error: {mse}")
    else:
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)
        results['accuracy'] = accuracy
        results['confusion_matrix'] = conf_matrix
        results['classification_report'] = class_report
        print(f"Accuracy: {accuracy}")
        print(f"Confusion Matrix:\n{conf_matrix}")
        print(f"Classification Report:\n{class_report}")

    # Save the model if required
    if save_model:
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")

    results['model'] = model
    return results

def inference(model, X_new):
    """
    Perform inference using the trained model.

    Parameters:
    model: Trained model.
    X_new (np.ndarray): New data for prediction.

    Returns:
    np.ndarray: Predictions for the new data.
    """
    return model.predict(X_new)
