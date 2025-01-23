import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class DataProcessing:
    def __init__(self, data):
        self.data = data
        self.cleaned_data = None
        self.scaled_data = None
        self.pca_data = None

    def filter_data(self, threshold=0.5):
        self.cleaned_data = self.data[self.data['value'] > threshold]
        print(f"Filtered data: {self.cleaned_data}")

    def clean_data(self):
        self.cleaned_data = self.data.dropna()
        print(f"Cleaned data: {self.cleaned_data}")

    def scale_data(self):
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(self.cleaned_data)
        print(f"Scaled data: {self.scaled_data}")

    def perform_pca(self, n_components=2):
        pca = PCA(n_components=n_components)
        self.pca_data = pca.fit_transform(self.scaled_data)
        print(f"PCA data: {self.pca_data}")

    def visualize_data(self):
        plt.scatter(self.pca_data[:, 0], self.pca_data[:, 1])
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.title('PCA of Processed Data')
        plt.show()

# Example usage
if __name__ == "__main__":
    # Simulate data collection from space-based assets
    data = pd.DataFrame({
        'value': np.random.rand(100),
        'sensor_1': np.random.rand(100),
        'sensor_2': np.random.rand(100)
    })

    dp = DataProcessing(data)

    # Filter and clean data
    dp.filter_data(threshold=0.5)
    dp.clean_data()

    # Scale and perform PCA
    dp.scale_data()
    dp.perform_pca(n_components=2)

    # Visualize the processed data
    dp.visualize_data()
