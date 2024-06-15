import pandas as pd
import requests
from requests.exceptions import RequestException, HTTPError, Timeout
import re

# Load your dataset
df = pd.read_csv('datasets/500.csv')  # Replace with your dataset path

# Function to check if URL is valid
def is_valid_url(url):
    try:
        # Ensure the URL has a valid format
        if not re.match(r'http[s]?://', url):
            url = 'http://' + url

        response = requests.get(url, allow_redirects=True, timeout=10)
        # Consider the URL valid if the status code is in the 200-399 range
        if 200 <= response.status_code < 400:
            return True
        else:
            return False
    except (RequestException, HTTPError, Timeout) as e:
        # Print the error for debugging purposes
        print(f"Error for URL {url}: {e}")
        return False


# Data cleaning
print("\nData Cleaning Process:")

# Check for missing values
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Drop rows with missing values
df = df.dropna()

# Check for duplicates
print("\nNumber of Duplicate Rows Before Cleaning:")
print(df.duplicated().sum())

# Drop duplicate rows
df = df.drop_duplicates()

# Verify the label column has only 'good' and 'bad' values
print("\nUnique Values in the Label Column Before Cleaning:")
print(df['Label'].unique())

# Filter out any rows with invalid labels
df = df[df['Label'].isin(['good', 'bad'])]

# Strip whitespace from URLs (if any)
df['URL'] = df['URL'].str.strip()

# Verify the cleaned dataset
print("\nCleaned Dataset:")
print(df.head())

# Final check for missing values and duplicates
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nNumber of Duplicate Rows After Cleaning:")
print(df.duplicated().sum())

print("\nUnique Values in the Label Column After Cleaning:")
print(df['Label'].unique())

# Apply the function to the 'URL' column
df['is_valid'] = df['URL'].apply(is_valid_url)

# Save the results to a new CSV file
df.to_csv('validated_urls.csv', index=False)