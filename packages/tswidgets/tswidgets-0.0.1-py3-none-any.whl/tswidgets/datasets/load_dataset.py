import os
import pandas as pd
import pkg_resources  # Works for both installed packages and local development

# Define the path to the datasets directory
DATASETS_DIR = pkg_resources.resource_filename(__name__, 'datasets')
# DATASETS_DIR = os.path.join(os.path.dirname(__file__))

def load_dataset(name: str) -> pd.DataFrame:
    """
    Load a dataset by name from the datasets directory.
    """
    file_path = os.path.join(DATASETS_DIR, f"{name}.pkl")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset '{name}' not found in datasets directory at '{file_path}'.")
    
    return pd.read_pickle(file_path)






