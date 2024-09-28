import mysql.connector
import pandas as pd
import sys



def dataframe_dataset(dataset, credentials: dict, table_name: str):

    status = 0

    if type(dataset) == pd.DataFrame:

        # alter dataset dtype to string --------------------------- #
        datatypes = dataset.dtypes.tolist()                         #
        columns = dataset.columns.tolist()                          #
        datatypes_altered = tuple([str(x) for x in datatypes])      #
                                                                    #
        cols_to_alter_type = []                                     #
        for i in range(len(datatypes)):                             #
            if datatypes[i] != 'O':                                 #
                cols_to_alter_type.append(i)                        #
                                                                    #
        for i in cols_to_alter_type:                                #
            dataset[columns[i]] = dataset[columns[i]].astype(str)   #
                                                                    #
        dataset.fillna('', inplace=True)                            #
        # --------------------------------------------------------- #

        # try connecting to database -------------------------- #
        try:                                                    #
            database = mysql.connector.connect(**credentials)   #
        except Exception as e:                                  #
            print(f"An error occurred while "                   #
                  f"connecting to database: {e}")               #
            sys.exit(1)                                         #
        cursor = database.cursor()                              #
        # ----------------------------------------------------- #

        # inserting dataset into database ------------------------------------- #
                                                                                #
        cursor.execute(f"insert into {table_name} values {datatypes_altered}")  #
        placeholders = ", ".join(["%s"] * len(columns))                         #
        insert_query = f" insert into {table_name} values ({placeholders}) "    #
        dataset_tuples = [tuple(row) for row in                                 #
                          dataset.itertuples(index=False, name=None)]           #
        try:                                                                    #
            cursor.executemany(insert_query, dataset_tuples)                    #
            status = 1                                                          #
        except Exception as e:                                                  #
            print(f"An error occurred while "                                   #
                  f"uploading data to the database: {e}")                       #
            sys.exit(1)                                                         #
        # --------------------------------------------------------------------- #

        database.commit()
        cursor.close()
        database.close()

    else:

        print("Dataset is not a pandas DataFrame")

    if status == 0:
        print(f"Could not upload dataset into table {table_name}")
    else:
        print(f"Successfully uploaded dataset into table {table_name}")