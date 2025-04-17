import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """Load raw data from a CSV file."""
    data = pd.read_csv(file_path)
    return data

def clean_data(data):
    """Clean the data by handling missing values and duplicates."""
    data = data.drop_duplicates()
    data = data.dropna()
    return data

def preprocess_data(file_path, test_size=0.2, random_state=42):
    """Load, clean, and preprocess the data."""
    data = load_data(file_path)
    data = clean_data(data)
    
    # Assuming the target variable is named 'target'
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, scaler