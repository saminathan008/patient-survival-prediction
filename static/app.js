const fields = [

    "age",
    "cancer_type",
    "tumor_size",
    "cell_size",
    "cell_shape",
    "cell_density",
    "cell_uniformity",
    "nucleus_area",
    "concavity",
    "perimeter",
    "texture"

];


const form =
    document.getElementById(
        "predictionForm"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const data = {};


        fields.forEach(
            function(field) {

                data[field] =
                    document.getElementById(
                        field
                    ).value;

            }
        );


        try {

            const response =
                await fetch(
                    "/predict",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)

                    }
                );


            const result =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    result.error
                );

            }


            showResult(result);


        } catch(error) {

            alert(
                "Prediction error: "
                + error.message
            );

        }

    }
);


function showResult(result) {


    document
        .getElementById(
            "emptyState"
        )
        .classList
        .add("hidden");


    document
        .getElementById(
            "resultState"
        )
        .classList
        .remove("hidden");


    const badge =
        document.getElementById(
            "predictionBadge"
        );


    badge.textContent =
        result.prediction.toUpperCase();


    badge.classList.toggle(
        "benign",
        result.prediction === "Benign"
    );


    const confidence =
        result.confidence;


    document
        .getElementById(
            "confidence"
        )
        .textContent =
        confidence.toFixed(2)
        + "%";


    const circle =
        document.getElementById(
            "confidenceCircle"
        );


    circle.style.background =
        `conic-gradient(
            #76efc2
            ${confidence * 3.6}deg,
            #29343e
            0deg
        )`;


    circle.querySelector(
        "span"
    ).textContent =
        Math.round(confidence)
        + "%";


    const benign =
        result.probabilities.Benign;


    const malignant =
        result.probabilities.Malignant;


    document
        .getElementById(
            "benignValue"
        )
        .textContent =
        benign.toFixed(2)
        + "%";


    document
        .getElementById(
            "malignantValue"
        )
        .textContent =
        malignant.toFixed(2)
        + "%";


    document
        .getElementById(
            "benignBar"
        )
        .style.width =
        benign + "%";


    document
        .getElementById(
            "malignantBar"
        )
        .style.width =
        malignant + "%";


    document
        .getElementById(
            "resultMessage"
        )
        .textContent =

        result.prediction === "Malignant"

        ?

        "The model classified this sample as Malignant. This is an academic machine-learning demonstration and not a medical diagnosis."

        :

        "The model classified this sample as Benign. This is an academic machine-learning demonstration and not a medical diagnosis.";

}



// Demo button

document
    .getElementById(
        "demoButton"
    )
    .addEventListener(
        "click",
        function() {

            document.getElementById(
                "age"
            ).value = 55;

            document.getElementById(
                "cancer_type"
            ).value = "Breast";

            document.getElementById(
                "tumor_size"
            ).value = 24;

            document.getElementById(
                "cell_size"
            ).value = 28;

            document.getElementById(
                "cell_shape"
            ).value = 25;

            document.getElementById(
                "cell_density"
            ).value = 35;

            document.getElementById(
                "cell_uniformity"
            ).value = 40;

            document.getElementById(
                "nucleus_area"
            ).value = 180;

            document.getElementById(
                "concavity"
            ).value = 22;

            document.getElementById(
                "perimeter"
            ).value = 95;

            document.getElementById(
                "texture"
            ).value = 32;

        }
    );


// Reset

document
    .getElementById(
        "resetButton"
    )
    .addEventListener(
        "click",
        function() {

            location.reload();

        }
    );
