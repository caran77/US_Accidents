import logging
from data.data import get_accidents_dataset, get_states
from data.data import export_dataset, export_dataset_grouped_by_year, export_black_points_by_year
from features.features import prepare_dataset


def main():
    try:
        logging.info(f"Staring application with parameters")
        df_states = get_states()
        df = get_accidents_dataset()
        df = prepare_dataset(df, df_states)
        export_dataset_grouped_by_year(df)
        export_black_points_by_year(df)
        export_dataset(df)
    except:
        logging.exception("library has finished with errors")


if __name__ == '__main__':
    main()
