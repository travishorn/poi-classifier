import pandas as pd
import joblib

# Load the trained model
model = joblib.load('trained_model.pkl')

# Prepare new POI data on which types need to be classified
data = pd.read_csv('poi_to_classify.csv')

# Extract the columns for classification (latitude, longitude, name)
X_new = data[['latitude', 'longitude', 'name']]

# Preprocess the new data using the same preprocessor from the training phase
preprocessor = model.named_steps['preprocessor']
X_new_preprocessed = preprocessor.transform(X_new)

# Use the loaded model to make classifications
classified_types = model.classify(X_new)

# Aad the classifications to the DataFrame:
data['type'] = classified_types

# Display the DataFrame with the classified types
print(data[['latitude', 'longitude', 'name', 'type']])

# Write a new file with classified types included
data.to_csv('poi_classified.csv')
