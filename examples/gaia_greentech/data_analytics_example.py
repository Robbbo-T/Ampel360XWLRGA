```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For better visualizations
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

class DataAnalytics:
    """
    Performs data analysis on data from multiple CSV files.

    Args:
        data_sources (list): A list of paths to CSV data files.
    """

    def __init__(self, data_sources: list):
        self.data_sources = data_sources
        self.data = self.load_data()

    def load_data(self) -> dict:
        """Loads data from the specified CSV files.

        Returns:
            dict: A dictionary where keys are data source names and values are Pandas DataFrames.

        Raises:
            FileNotFoundError: If a specified file does not exist.
            pd.errors.ParserError: If there's an error parsing a CSV file.
        """
        data = {}
        for source in self.data_sources:
            try:
                data[source] = pd.read_csv(source)
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {source}")
            except pd.errors.ParserError:
                raise pd.errors.ParserError(f"Error parsing CSV file: {source}")
            except Exception as e:  # Catch other potential errors during load
                 raise Exception(f"An unexpected error occurred reading {source}: {e}")
        return data
    
    def preprocess_data(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """Preprocesses the data: handles missing values, and encodes categorical variables.

        Args:
            df (pd.DataFrame): The input DataFrame.
            target_column (str): The name of the target column

        Returns:
            pd.DataFrame: The preprocessed DataFrame.
        """

        # Handle missing values (impute with mean for numeric, mode for categorical)
        for col in df.columns:
            if df[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])

        #Ensure the target column exists, and drop it from the input if it does.
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame.")
        
        return df



    def perform_statistical_analysis(self) -> dict:
        """Performs statistical analysis on the loaded data.

        Returns:
            dict: A dictionary of DataFrames with descriptive statistics for each data source.
        """
        analysis_results = {}
        for source, df in self.data.items():
            if not df.empty:  # Check for empty DataFrames
                analysis_results[source] = df.describe()
            else:
                 analysis_results[source] = pd.DataFrame() #Return empty frame
        return analysis_results


    def perform_ml_analysis(self, target_column: str, test_size: float = 0.2, random_state: int = 42) -> dict:
        """Performs machine learning analysis (linear regression) on the data.

        Args:
            target_column (str): The name of the target variable column.
            test_size (float): The proportion of data to use for testing (0 to 1).
            random_state (int):  Random seed for reproducibility.

        Returns:
            dict: A dictionary containing model results for each data source.
                  Includes the trained model, predictions, MSE, R-squared, and MAE.
        """
		
        ml_results = {}
        for source, df in self.data.items():

            if df.empty:
                ml_results[source] = {} # Return empty dict for empty data.
                continue # Skip to the next file
            
            df = self.preprocess_data(df, target_column)  # Preprocess
                
            # Prepare data
            X = df.drop(columns=[target_column])
            y = df[target_column]

			# Identify categorical and numerical features
            categorical_features = X.select_dtypes(include=['object', 'category']).columns
            numerical_features = X.select_dtypes(include=['number']).columns
			
			# Create preprocessing pipelines for numeric and categorical features.
            numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])		
            categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))]) # Handle unseen values.
            
			# Combine preprocessing steps using ColumnTransformer
            preprocessor = ColumnTransformer(
				transformers=[
					('num', numeric_transformer, numerical_features),
					('cat', categorical_transformer, categorical_features)
				]
			)

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

            # Build the model pipeline: preprocessing + linear regression
            model = Pipeline(steps=[('preprocessor', preprocessor),
                                    ('regressor', LinearRegression())])

			# Train the Model
            model.fit(X_train, y_train)
			
            # Make predictions
            y_pred = model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)

            ml_results[source] = {
                'model': model,
                'predictions': y_pred,
                'mse': mse,
                'r2': r2,
                'mae': mae,
                'X_test': X_test,  # Store test data for visualization
                'y_test': y_test   # Store for visualization
            }
        return ml_results


    def visualize_results(self, analysis_results: dict, ml_results: dict):
        """Visualizes the results of statistical and ML analyses.

        Args:
            analysis_results (dict): Results from perform_statistical_analysis.
            ml_results (dict): Results from perform_ml_analysis.
        """
        for source, result in analysis_results.items():
            print(f"Statistical Analysis for {source}:\n", result)

            if not result.empty: # Do not try to make visualisations if the dataframe is empty
                # Histograms for numerical features
                df = self.data[source]  # Get the original DataFrame
                numerical_cols = df.select_dtypes(include=np.number).columns
                if not numerical_cols.empty:
                  df[numerical_cols].hist(figsize=(10, 8))
                  plt.suptitle(f"Histograms for {source}")
                  plt.tight_layout()
                  plt.show()

                # Correlation matrix
                if len(numerical_cols) > 1:
                  corr_matrix = df[numerical_cols].corr()
                  plt.figure(figsize=(8, 6))
                  sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
                  plt.title(f"Correlation Matrix for {source}")
                  plt.tight_layout()
                  plt.show()

        for source, result in ml_results.items():
          if result:
            # Scatter plot of actual vs. predicted values
            plt.figure(figsize=(8, 6))
            plt.scatter(result['y_test'], result['predictions'], alpha=0.5)
            plt.xlabel('Actual Values')
            plt.ylabel('Predicted Values')
            plt.title(f'Actual vs. Predicted Values for {source}')
            plt.plot([result['y_test'].min(), result['y_test'].max()], [result['y_test'].min(), result['y_test'].max()], 'k--', lw=2)  # Diagonal line
            plt.tight_layout()
            plt.show()

            # Residual plot
            residuals = result['y_test'] - result['predictions']
            plt.figure(figsize=(8, 6))
            plt.scatter(result['predictions'], residuals, alpha=0.5)
            plt.xlabel('Predicted Values')
            plt.ylabel('Residuals')
            plt.title(f'Residual Plot for {source}')
            plt.axhline(y=0, color='k', linestyle='--')  # Horizontal line at y=0
            plt.tight_layout()
            plt.show()

# --- Example Usage ---
if __name__ == "__main__":
    # Create dummy CSV files for demonstration
    data1 = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [2, 4, 1, 5, 3, 6, 8, 7, 9, 10],
        'target':   [3, 6, 4, 9, 8, 12, 15, 14, 18, 20]
    })
    data2 = pd.DataFrame({
        'featureA': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A'],
        'featureB': [0.5, 0.2, 0.8, 0.1, 0.6, 0.9, 0.3, 0.7, 0.4, 1.0],
        'target':   [1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
    })

    data1.to_csv('data_source_1.csv', index=False)
    data2.to_csv('data_source_2.csv', index=False)


    data_sources = ['data_source_1.csv', 'data_source_2.csv']
    # data_sources = ['data_source_1.csv', 'file_does_not_exist.csv', 'data_source_2.csv'] # Test the error handling.
    try:
        da = DataAnalytics(data_sources)

        # Perform statistical analysis
        analysis_results = da.perform_statistical_analysis()

        # Perform machine learning analysis
        ml_results = da.perform_ml_analysis(target_column='target')

        # Visualize results
        da.visualize_results(analysis_results, ml_results)

    except (FileNotFoundError, pd.errors.ParserError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e: # Catch other potential exceptions.
        print(f"An unexpected error occurred: {e}")

