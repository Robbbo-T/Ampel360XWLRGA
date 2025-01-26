import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class SmartGridOptimizer:
    def __init__(self, energy_data, price_data):
        self.energy_data = energy_data
        self.price_data = price_data

    def predict_energy_consumption(self, data):
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array(data).reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)
        return predictions, mse

    def adjust_energy_prices(self):
        predictions, mse = self.predict_energy_consumption(self.energy_data)
        adjusted_prices = self.price_data * (1 + predictions / np.max(predictions))
        return adjusted_prices

    def integrate_renewable_sources(self, renewable_data):
        total_energy = self.energy_data + renewable_data
        return total_energy

    def optimize_energy_distribution(self, total_energy):
        optimized_distribution = total_energy / np.sum(total_energy)
        return optimized_distribution

    def plot_energy_data(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.energy_data, label='Energy Consumption')
        plt.plot(self.price_data, label='Energy Prices')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Smart Grid Energy Data')
        plt.legend()
        plt.show()

# Example usage
energy_data = [100, 120, 130, 125, 140, 150, 160, 170, 165, 155]
price_data = [10, 12, 14, 13, 15, 16, 18, 20, 19, 17]
renewable_data = [20, 25, 30, 28, 35, 40, 45, 50, 48, 42]

optimizer = SmartGridOptimizer(energy_data, price_data)
adjusted_prices = optimizer.adjust_energy_prices()
total_energy = optimizer.integrate_renewable_sources(renewable_data)
optimized_distribution = optimizer.optimize_energy_distribution(total_energy)
optimizer.plot_energy_data()

print("Adjusted Energy Prices:", adjusted_prices)
print("Total Energy:", total_energy)
print("Optimized Energy Distribution:", optimized_distribution)
