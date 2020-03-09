import sys
import os
from pathlib import Path

etl_dir = Path(__file__).parent.absolute()
server_dir = etl_dir.joinpath('../Server')
sys.path.append(str(server_dir))

from CollegeRanking.models import Variable, NumericVariable, FactorVariable
from mongoengine import connect
import pandas as pd
import argparse

def get_type(row):
    if row['API data type'] == 'string':
        # I don't want to handle strings yet
        return 'skip'
    elif row['API data type'] == 'integer' and pd.notna(row['LABEL']):
        # Integer types with labels should be interpreted like enums, not integers
        return 'factor'
    else:
        # The variable contains a number
        return 'quantity'

def main(dictionary_file):
    df = pd.read_excel(dictionary_file, sheet_name='institution_data_dictionary')
    
    results = []
    for idx, row in df.iterrows():
        if pd.notna(row['NAME OF DATA ELEMENT']):
            # Rows with a name are a variable, create it based on it's type
            type = get_type(row)
            if type == 'skip':
                continue
            elif type == 'quantity':
                results.append(NumericVariable(
                    _id = len(results),
                    name = row['NAME OF DATA ELEMENT'],
                    variable_name = row['VARIABLE NAME'],
                    category = row['dev-category'],
                    developer_name = row['developer-friendly name'],
                    source = row['SOURCE'],
                    consumer = row['NOTES'] == 'Shown/used on consumer website.'    # Variables with this note are probably important
                ))
            elif type == 'factor':
                results.append(FactorVariable(
                    _id = len(results),
                    name = row['NAME OF DATA ELEMENT'],
                    variable_name = row['VARIABLE NAME'],
                    category = row['dev-category'],
                    developer_name = row['developer-friendly name'],
                    source = row['SOURCE'],
                    consumer = row['NOTES'] == 'Shown/used on consumer website.',
                    factors = {str(int(row['VALUE'])):row['LABEL']}
                ))
                in_factor = True
            else:
                raise ValueError(f'Got unexpected type {type}')
        else:
            # The row does not specify an name, it must reference additional factors for the previous row
            results[-1].factors[str(int(row['VALUE']))] = row['LABEL']

    print("inserting")
    Variable.objects.insert(results)
    print("done")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dictionary', type=argparse.FileType('rb'), help='Path to a the CollageScorecardDataDictionary. Expected to be a `xlsx` file.')
    parser.add_argument('--mongo', type=str, default='CollegeRank', help="Mongoengine connection string")
    args = parser.parse_args()

    connect(args.mongo)    
    main(args.dictionary)
    args.dictionary.close()