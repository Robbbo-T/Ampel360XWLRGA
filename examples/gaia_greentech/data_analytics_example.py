import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class DataAnalytics:
    def __init__(self, data_sources):
        self.data_sources = data_sources
        self.data = self.load_data()

    def load_data(self):
        data = {}
        for source in self.data_sources:
            data[source] = pd.read_csv(source)
        return data

    def perform_statistical_analysis(self):
        analysis_results = {}
        for source, df in self.data.items():
            analysis_results[source] = df.describe()
        return analysis_results

    def perform_ml_analysis(self, target_column):
        ml_results = {}
        for source, df in self.data.items():
            X = df.drop(columns=[target_column])
            y = df[target_column]
            model = LinearRegression()
            model.fit(X, y)
            predictions = model.predict(X)
            mse = mean_squared_error(y, predictions)
            ml_results[source] = {
                'model': model,
                'predictions': predictions,
                'mse': mse
            }
        return ml_results

    def visualize_results(self, analysis_results, ml_results):
        for source, result in analysis_results.items():
            print(f"Statistical Analysis for {source}:\n", result)
        
        for source, result in ml_results.items():
            plt.figure(figsize=(10, 5))
            plt.plot(result['predictions'], label='Predictions')
            plt.plot(self.data[source][result['predictions'].index], label='Actual')
            plt.xlabel('Index')
            plt.ylabel('Value')
            plt.title(f'ML Analysis for {source}')
            plt.legend()
            plt.show()

# Example usage
if __name__ == "__main__":
    data_sources = ['data_source_1.csv', 'data_source_2.csv']
    da = DataAnalytics(data_sources)

    # Perform statistical analysis
    analysis_results = da.perform_statistical_analysis()

    # Perform machine learning analysis
    ml_results = da.perform_ml_analysis(target_column='target')

    # Visualize results
    da.visualize_results(analysis_results, ml_results)
