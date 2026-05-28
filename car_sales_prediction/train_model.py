"""
Machine Learning Model Training Script
Trains a RandomForestRegressor to predict car selling prices
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os

# Load dataset
print("Loading dataset...")
df = pd.read_csv('dataset/car_data.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Missing values:\n{df.isnull().sum()}")

# Data Preprocessing
print("\nPreprocessing data...")

# Create a copy for processing
X = df.drop('Selling_Price', axis=1).copy()
y = df['Selling_Price'].copy()

# Label Encode categorical variables
label_encoders = {}
categorical_columns = ['Car_Name', 'Fuel_Type', 'Seller_Type', 'Transmission']

for col in categorical_columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le
    print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

print(f"\nFeatures after encoding:\n{X.head()}")
print(f"Target (Selling_Price):\n{y.head()}")

# Train-Test Split
print("\nSplitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set size: {X_train.shape}")
print(f"Test set size: {X_test.shape}")

# Train RandomForestRegressor Model
print("\nTraining RandomForestRegressor model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("Model training completed!")

# Model Evaluation
print("\nEvaluating model...")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_mae = mean_absolute_error(y_test, y_pred_test)

print(f"\nModel Performance:")
print(f"Training R² Score: {train_r2:.4f}")
print(f"Test R² Score: {test_r2:.4f}")
print(f"Training RMSE: {train_rmse:.4f}")
print(f"Test RMSE: {test_rmse:.4f}")
print(f"Test MAE: {test_mae:.4f}")

# Feature Importance
print("\nFeature Importance:")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance)

# Save the model and label encoders
print("\nSaving model and encoders...")
joblib.dump(model, 'model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')
print("✓ Model saved as model.pkl")
print("✓ Label encoders saved as label_encoders.pkl")

print("\nModel training and saving completed successfully!")
