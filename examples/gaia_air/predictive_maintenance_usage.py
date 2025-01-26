import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load historical sensor data
try:
    data = pd.read_csv('sensor_data.csv')
    logging.info("Sensor data loaded successfully.")
except FileNotFoundError:
    logging.error("File not found. Please check the file path.")
    raise
except pd.errors.EmptyDataError:
    logging.error("No data found. Please check the file content.")
    raise
except Exception as e:
    logging.error(f"An error occurred: {e}")
    raise

# Preprocess data
data = data.dropna()  # Remove missing values
X = data.drop('failure', axis=1)  # Features
y = data['failure']  # Target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train machine learning models
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)

# Predict future maintenance needs
rf_y_pred = rf_model.predict(X_test)
gb_y_pred = gb_model.predict(X_test)

# Output recommendations
print("Random Forest Classifier Report:")
print(classification_report(y_test, rf_y_pred))
print("Gradient Boosting Classifier Report:")
print(classification_report(y_test, gb_y_pred))

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Predictive Maintenance Dashboard'),
    dcc.Graph(id='maintenance-graph'),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

@app.callback(
    Output('maintenance-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    figure = {
        'data': [
            {'x': X_test.index, 'y': rf_y_pred, 'type': 'line', 'name': 'RF Predicted Failures'},
            {'x': X_test.index, 'y': gb_y_pred, 'type': 'line', 'name': 'GB Predicted Failures'}
        ],
        'layout': {
            'title': 'Predictive Maintenance Results'
        }
    }
    return figure

def visualize_results():
    app.run_server(debug=True)

# Example usage
if __name__ == "__main__":
    visualize_results()
