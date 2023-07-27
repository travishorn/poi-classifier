import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from joblib import dump

# Load the training data
data = pd.read_csv('poi_training.csv')

# Preprocess the data
# ColumnTransformer handles different preprocessing for different columns
preprocessor = ColumnTransformer(
    transformers=[
        # Use CountVectorizer to convert POI names into numerical representations
        ('name', CountVectorizer(), 'name'),
        # Use Pipeline with StandardScaler to scale the coordinates
        ('lat_lon', Pipeline(steps=[('scaler', StandardScaler())]), ['latitude', 'longitude'])
    ])

# Split the data into training and testing sets. We want to use the lat, lng,
# and name to classify the type
X = data[['latitude', 'longitude', 'name']]
y = data['type']

# 80% of the data will be used for training. 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Use a RandomForestClassifier machine learning algorithm
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', RandomForestClassifier())])

# Train the model on the training data
model.fit(X_train, y_train)

# Write the trained model to disk for use later
dump(model, 'trained_model.pkl')

# Evaluate the model on the testing data
y_pred = model.predict(X_test)

# Score the accuracy, precision, recall, and F1 for the trained model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
f1 = f1_score(y_test, y_pred, average='weighted')

# Print the scores
print("Accuracy: {:.1f}%".format(accuracy * 100))
print("Precision: {:.1f}%".format(precision * 100))
print("Recall: {:.1f}%".format(recall * 100))
print("F1-score: {:.1f}%".format(f1 * 100))
