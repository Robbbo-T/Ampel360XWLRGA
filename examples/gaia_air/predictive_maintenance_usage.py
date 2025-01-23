import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load historical sensor data
data = pd.read_csv('sensor_data.csv')

# Preprocess data
data = data.dropna()  # Remove missing values
X = data.drop('failure', axis=1)  # Features
y = data['failure']  # Target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a machine learning model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict future maintenance needs
y_pred = model.predict(X_test)

# Output recommendations
print(classification_report(y_test, y_pred))
