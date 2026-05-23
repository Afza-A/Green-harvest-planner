from datasets import load_dataset


def load_crop_dataset():
    dataset = load_dataset("dhyann2815/india-crop-yield-prediction")

    train_df = dataset["train"].to_pandas()
    test_df = dataset["test"].to_pandas()

    train_df.columns = train_df.columns.str.strip()
    test_df.columns = test_df.columns.str.strip()

    required_columns = [
        "Year",
        "State",
        "Crop",
        "Season",
        "Area",
        "Annual_Rainfall",
        "Fertilizer",
        "Pesticide",
        "Yield"
    ]

    train_df = train_df[required_columns].dropna()
    test_df = test_df[required_columns].dropna()

    return train_df, test_df 