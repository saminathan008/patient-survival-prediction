from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("multi_cancer_model.pkl")

cancer_types = [
    "Breast",
    "Lung",
    "Colon",
    "Liver",
    "Skin",
    "Prostate",
    "Ovary",
    "Pancreas",
    "Kidney",
    "Thyroid"
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        cancer_types=cancer_types
    )


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    sample = {
        "age": float(data["age"]),
        "cancer_type": data["cancer_type"],
        "tumor_size": float(data["tumor_size"]),
        "cell_size": float(data["cell_size"]),
        "cell_shape": float(data["cell_shape"]),
        "cell_density": float(data["cell_density"]),
        "cell_uniformity": float(data["cell_uniformity"]),
        "nucleus_area": float(data["nucleus_area"]),
        "concavity": float(data["concavity"]),
        "perimeter": float(data["perimeter"]),
        "texture": float(data["texture"])
    }

    input_data = pd.DataFrame([sample])

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    classes = list(model.classes_)

    probability_data = {
        classes[i]: round(
            float(probabilities[i]) * 100,
            2
        )
        for i in range(len(classes))
    }

    confidence = round(
        float(max(probabilities)) * 100,
        2
    )

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "probabilities": probability_data
    })


if __name__ == "__main__":
    app.run(debug=True)