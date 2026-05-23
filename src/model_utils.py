from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES = [
    "Year",
    "State",
    "Crop",
    "Season",
    "Area",
    "Annual_Rainfall",
    "Fertilizer",
    "Pesticide"
]

TARGET = "Yield"


def get_preprocessor():
    categorical_features = ["State", "Crop", "Season"]
    numerical_features = [
        "Year",
        "Area",
        "Annual_Rainfall",
        "Fertilizer",
        "Pesticide"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numerical_features)
        ]
    )

    return preprocessor


def build_models():
    preprocessor = get_preprocessor()

    models = {
        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=18,
            min_samples_split=8,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        ),

        "Extra Trees": ExtraTreesRegressor(
            n_estimators=200,
            max_depth=18,
            min_samples_split=8,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=180,
            learning_rate=0.05,
            max_depth=4,
            random_state=42
        )
    }

    pipelines = {}

    for name, model in models.items():
        pipelines[name] = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model)
            ]
        )

    return pipelines 