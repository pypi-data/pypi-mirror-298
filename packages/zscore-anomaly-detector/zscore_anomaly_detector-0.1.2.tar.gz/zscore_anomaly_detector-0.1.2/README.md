# Zscore Anomaly Detector

** Zscore Anomaly Detector** is a Python package designed to detect anomalies in numerical datasets using Z-Score analysis. This package identifies outliers by calculating the Z-Score for each numerical column and flags data points that deviate significantly from the mean. The package can handle mixed datasets containing numerical, categorical, and object types.

## Installation

You can install the package using pip. Run the following command:

```bash
pip install zscore-anomaly-detector


## Usage
Here is an example of how to use the ZScore Anomaly Detector package with a realistic dataset containing both numerical and categorical columns:

import pandas as pd

from zscore_anomaly.zscore_anomaly_detector import ZScoreAnomalyDetector

## Sample Dataset

data = pd.DataFrame({
    'Age': [25, 32, 47, 51, 62, 35, 27, 100, 29, 38],  # Numeric
    'Salary': [50000, 54000, 58000, 62000, 65000, 52000, 51000, 200000, 53000, 56000],  # Numeric
    'Department': ['HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR'],  # Categorical
    'Has_Debt': [True, False, True, True, False, False, True, True, False, True],  # Boolean
    'City': ['New York', 'San Francisco', 'Los Angeles', 'New York', 'San Francisco', 'Los Angeles', 'New York', 'San Francisco', 'Los Angeles', 'New York'],  # Object
})


#### Initialize the ZscoreAnomalyDetector

detector = ZScoreAnomalyDetector(threshold=2)  # The user can specify the threshold value for detecting anomalies. By default, the threshold is set to 3 if not provided.



#### Create a DataFrame that Includes Anomalies Marked

df_with_anomalies = detector.create_dataframe_with_anomalies(data)


#### Style the DataFrame to Highlight Anomalies in Red

styled_df = detector.style_dataframe(df_with_anomalies)


#### Display the Styled DataFrame

styled_df


Explanation
Age and Salary are numeric columns where Z-Scores will be calculated to detect anomalies.

Department is a categorical column, and City is an object column. These will not be included in Z-Score calculations, but they remain in the dataset.

Has_Debt is a boolean column.

This example shows how to detect anomalies in the numeric columns (Age and Salary) while leaving the non-numeric columns intact.

Output

After running the above code, the DataFrame will display anomalies detected in the numeric columns. Anomalies will be highlighted in red if used in a Jupyter notebook or a similar environment that supports DataFrame styling.




