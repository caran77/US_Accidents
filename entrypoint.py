import logging
from data.data import get_accidents_dataset
from features.features import prepare_dataset


def main():
    try:
        logging.info(f"Staring application with parameters")
        df = get_accidents_dataset()
        df = prepare_dataset(df)
        print(df.to_string())
    except:
        logging.exception("library has finished with errors")


if __name__ == '__main__':
    main()
