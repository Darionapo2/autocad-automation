import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def read_Florim_USA_coordinates_extraction(CSV_datasource):
    table = pd.read_csv(CSV_datasource)

    table.fillna('NA', inplace = True)

    print(table)



def main():
    read_Florim_USA_coordinates_extraction('Florim_USA_coordinates/florim_usa_coordinates_new_warehouse_extraction.csv')


if __name__ == '__main__':
    main()