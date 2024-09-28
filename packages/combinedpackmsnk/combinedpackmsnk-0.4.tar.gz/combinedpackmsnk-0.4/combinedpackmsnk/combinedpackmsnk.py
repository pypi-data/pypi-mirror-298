import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from xgboost import XGBClassifier, XGBRegressor
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR

# Create a dictionary to store encoders for each column
encoders = {}

def load_data(file_loc, header_row_number=0):
    """
    Load data from CSV or JSON file and convert it into a pandas DataFrame.
    """
    if file_loc.endswith('.csv'):
        if header_row_number == 0:
            df = pd.read_csv(file_loc)
        else:
            df = pd.read_csv(file_loc, header=header_row_number)
    elif file_loc.endswith('.json'):
        df = pd.read_json(file_loc)
    else:
        raise ValueError("Unsupported file format. Only CSV and JSON are supported.")
    
    return df

def load_data_from_api(api_url):
    """
    Fetch data from an API and load it into a pandas DataFrame.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        # Flattening nested JSON if necessary
        df = pd.json_normalize(data)
    else:
        raise Exception(f"Failed to fetch data from API. Status Code: {response.status_code}")
    
    return df

def encode_categorical_columns(df):
    """
    Encode categorical columns and store the encoders. Handle NaN values by filling them with a placeholder.
    """
    global encoders
    categorical_vars = df.select_dtypes(include=['object']).columns
    for col in categorical_vars:
        df[col] = df[col].fillna('missing')  # Fill NaN with placeholder
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le  # Store the encoder to decode later
    return df

def decode_categorical_columns(df):
    """
    Decode categorical columns back to their original categories.
    """
    global encoders
    for col, le in encoders.items():
        if col in df.columns:
            df[col] = le.inverse_transform(df[col].astype(int))
            df[col] = df[col].replace('missing', pd.NA)  # Restore NaN values
    return df

def func(file_loc=None, api_url=None, header_row_number=0):
    """
    Main function that handles data from CSV/JSON files or APIs and allows analysis, 
    classification, regression, and clustering.
    """
    if file_loc:
        df = load_data(file_loc, header_row_number)
    elif api_url:
        df = load_data_from_api(api_url)
    else:
        raise ValueError("Either file_loc or api_url must be provided.")
    
    print("First 3 rows of the dataset:")
    print(df.head(3))

    # Encode categorical variables
    df = encode_categorical_columns(df)

    # Handle missing values
    df = df.fillna(df.mean())  # Fill numeric columns with mean
    df = df.fillna(df.mode().iloc[0])  # Fill categorical columns with mode

    # Data normalization
    scaler_choice = input('Choose a scaler: StandardScaler (S) or MinMaxScaler (M): ')
    if scaler_choice.upper() == 'S':
        scaler = StandardScaler()
    elif scaler_choice.upper() == 'M':
        scaler = MinMaxScaler()
    else:
        scaler = None

    target = input(f'\nFrom the list of columns to choose from: {df.columns}\n Specify which column that you want to use as target variable: \n')
    id_col = input(' If there is an ID column you would like to exclude from analysis, please specify the ID column: If not, press Enter')

    if id_col in df.columns:
        X = df.drop([target], axis=1).drop(id_col, axis=1)
        y = df[target]
    else:
        X = df.drop(target, axis=1)
        y = df[target]

    # Apply scaling
    if scaler:
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # VIF dataframe 
    vif_data = pd.DataFrame() 
    vif_data["feature"] = X.columns 
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print("\nVariance Inflation Factor (VIF):\n", vif_data)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print("Training set shape:", X_train.shape, y_train.shape)
    print("Testing set shape:", X_test.shape, y_test.shape)

    inp = input('Which ML model would you like to perform? Enter C for Classification, R for Regression, SR for OLS Regression, CL for Clustering, PCA for Dimensionality Reduction: ')
    
    y_pred = None
    if inp.upper() == 'C':
        model_choice = input('Choose a model: RF for RandomForest, LR for LogisticRegression, SVM for SupportVectorMachine, GB for GradientBoosting, AB for AdaBoost, XGB for XGBoost: ')
        if model_choice.upper() == 'RF':
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_choice.upper() == 'LR':
            clf = LogisticRegression(random_state=42)
        elif model_choice.upper() == 'SVM':
            clf = SVC(random_state=42)
        elif model_choice.upper() == 'GB':
            clf = GradientBoostingClassifier(n_estimators=100, random_state=42)
        elif model_choice.upper() == 'AB':
            clf = AdaBoostClassifier(n_estimators=100, random_state=42)
        elif model_choice.upper() == 'XGB':
            clf = XGBClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)
        precision = precision_score(y_test, y_pred, average='micro')
        recall = recall_score(y_test, y_pred, average='micro')
        print("Precision:", precision)
        print("Recall:", recall)

    elif inp.upper() == 'R':
        model_choice = input('Choose a model: RF for RandomForest, LR for LinearRegression, SVM for SupportVectorMachine, GB for GradientBoosting, AB for AdaBoost, XGB for XGBoost: ')
        if model_choice.upper() == 'RF':
            clf = RandomForestRegressor(random_state=42)
        elif model_choice.upper() == 'LR':
            clf = LinearRegression()
        elif model_choice.upper() == 'SVM':
            clf = SVR()
        elif model_choice.upper() == 'GB':
            clf = GradientBoostingRegressor(n_estimators=100, random_state=42)
        elif model_choice.upper() == 'AB':
            clf = AdaBoostRegressor(n_estimators=100, random_state=42)
        elif model_choice.upper() == 'XGB':
            clf = XGBRegressor(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

    # Decode the categorical columns back to original categories
    df = decode_categorical_columns(df)

    # Return processed dataset and prediction results
    if y_pred is not None:
        prediction_df = pd.DataFrame({'ID': X_test.index, 'Prediction': y_pred})
        result_df = pd.concat([X_test, prediction_df], axis=1)
        # Decode X_test categorical columns back to original
        result_df = decode_categorical_columns(result_df)
        return result_df
    else:
        # Decode df categorical columns back to original
        df = decode_categorical_columns(df)
        return df  # Return the preprocessed dataframe
