import numpy as np
import pandas as pd

class ZScoreAnomalyDetector:
    def __init__(self, threshold=3):
        """
        Z-Score Anomaly Detector
        threshold: The Z-Score value beyond which data points are considered anomalies.
                   The default value is 3 if not provided.
        """
        self.threshold = threshold
    
    def select_numeric_columns(self, data):
        """
        Selects only the numeric and continuous columns from the dataset.
        data: Pandas DataFrame containing the data
        Returns: DataFrame with only numeric columns
        """
        # Select only numerical columns (excluding object and categorical types)
        numeric_data = data.select_dtypes(include=[np.number])
        return numeric_data

    def z_score(self, data):
        """
        Calculates Z-Scores for each column in a multi-dimensional dataset.
        data: Pandas DataFrame containing the data
        Returns: DataFrame of Z-Scores for each column
        """
        numeric_data = self.select_numeric_columns(data)
        return (numeric_data - numeric_data.mean()) / numeric_data.std()

    def detect_anomalies(self, data):
        """
        Detects anomalies based on Z-Scores for each column in a multi-dimensional dataset.
        data: Pandas DataFrame containing the data
        Returns: DataFrame with boolean values indicating anomalies (True if anomaly)
        """
        z_scores = self.z_score(data)
        return (z_scores.abs() > self.threshold)

    def create_dataframe_with_anomalies(self, data):
        """
        Creates a DataFrame with the original dataset, marking anomalies as 1 (True) or 0 (False).
        data: Pandas DataFrame containing the data
        Returns: Pandas DataFrame with an additional 'Anomaly' column indicating rows with anomalies
        """
        anomalies = self.detect_anomalies(data)
        anomaly_rows = anomalies.any(axis=1)  # Mark row as an anomaly if any column has an anomaly
        data['Anomaly'] = anomaly_rows.astype(int)  # Convert True/False to 1/0
        return data

    def style_dataframe(self, df):
        """
        Styles the DataFrame to highlight anomalies in red.
        df: pandas DataFrame
        Returns: Styled DataFrame
        """
        def highlight_anomalies(row):
            color = 'background-color: red' if row['Anomaly'] == 1 else ''
            return [color] * len(row)
        
        return df.style.apply(highlight_anomalies, axis=1)

