import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_stores(file_path=DATA_DIR/"stores.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"{file_path} does not exist")
        return None

def load_products(file_path=DATA_DIR/"products.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"{file_path} does not exist")
        return None

def load_offers(file_path=DATA_DIR/"offers.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"{file_path} does not exist")
        return None

def main():
    stores = load_stores()
    products = load_products()
    offers = load_offers()

    if stores is not None:
        print("Stores:")
        print(stores.head())
        print()

    if products is not None:
        print("Products:")
        print(products.head())
        print()

    if offers is not None:
        print("Offers:")
        print(offers.head())
        print()

if __name__ == "__main__":
    main()