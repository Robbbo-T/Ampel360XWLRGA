import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class RenewableEnergyManager:
    def __init__(self, solar_data, wind_data, storage_capacity):
        self.solar_data = solar_data
        self.wind_data = wind_data
        self.storage_capacity = storage_capacity
        self.energy_storage = 0

    def predict_energy_output(self, data):
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array(data).reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)
        return predictions, mse

    def optimize_energy_distribution(self):
        solar_predictions, solar_mse = self.predict_energy_output(self.solar_data)
        wind_predictions, wind_mse = self.predict_energy_output(self.wind_data)
        total_energy = solar_predictions + wind_predictions
        energy_to_store = np.minimum(total_energy, self.storage_capacity - self.energy_storage)
        self.energy_storage += energy_to_store
        energy_to_distribute = total_energy - energy_to_store
        return energy_to_distribute

    def manage_energy_storage(self):
        if self.energy_storage > self.storage_capacity:
            self.energy_storage = self.storage_capacity
        elif self.energy_storage < 0:
            self.energy_storage = 0

    def plot_energy_data(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.solar_data, label='Solar Energy')
        plt.plot(self.wind_data, label='Wind Energy')
        plt.xlabel('Time')
        plt.ylabel('Energy Output')
        plt.title('Renewable Energy Output')
        plt.legend()
        plt.show()

# Example usage
solar_data = [10, 12, 14, 13, 15, 16, 18, 20, 19, 17]
wind_data = [5, 6, 7, 8, 7, 6, 5, 4, 3, 2]
storage_capacity = 50

manager = RenewableEnergyManager(solar_data, wind_data, storage_capacity)
energy_distribution = manager.optimize_energy_distribution()
manager.manage_energy_storage()
manager.plot_energy_data()

print("Energy Distribution:", energy_distribution)
print("Energy Storage:", manager.energy_storage)
