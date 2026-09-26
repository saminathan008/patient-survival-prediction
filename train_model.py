import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv(
    "multicancer_100000_approx_93_accuracy.csv"
)

print("Dataset loaded")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# -----------------------------------
# INPUT AND TARGET
# -----------------------------------

X = df.drop(columns=["target"])

y = df["target"]


# -----------------------------------
# FEATURES
# -----------------------------------

categorical_features = [
    "cancer_type"
]

numeric_features = [
    "age",
    "tumor_size",
    "cell_size",
    "cell_shape",
    "cell_density",
    "cell_uniformity",
    "nucleus_area",
    "concavity",
    "perimeter",
    "texture"
]


# -----------------------------------
# PREPROCESSING
# -----------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),

        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# -----------------------------------
# RANDOM FOREST
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# -----------------------------------
# COMPLETE PIPELINE
# -----------------------------------

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )
    ]
)


# -----------------------------------
# TRAIN / TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print()
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------------
# TRAIN
# -----------------------------------

pipeline.fit(
    X_train,
    y_train
)

print()
print("Training completed!")


# -----------------------------------
# TEST
# -----------------------------------

y_pred = pipeline.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    y_pred
)


print()
print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# -----------------------------------
# CONFUSION MATRIX
# -----------------------------------

print()
print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# -----------------------------------
# CLASSIFICATION REPORT
# -----------------------------------

print()
print("Classification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# -----------------------------------
# SAVE MODEL
# -----------------------------------

joblib.dump(
    pipeline,
    "multi_cancer_model.pkl"
)

print()
print(
    "Model saved as multi_cancer_model.pkl"
)