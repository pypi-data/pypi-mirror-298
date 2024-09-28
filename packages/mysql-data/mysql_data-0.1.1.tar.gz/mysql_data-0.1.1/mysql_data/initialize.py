import mysql.connector
import pandas as pd
import sys



def create_table(dataset, credentials: dict, table_name: str, force: bool = False):

    status = 0

    if type(dataset) == pd.DataFrame:

        columns = dataset.columns.tolist()
        datatypes = dataset.dtypes.tolist()
        datatypes_altered_numeric = tuple([len(str(x)) for x in datatypes])

        # try connecting to database -------------------------- #
        try:                                                    #
            database = mysql.connector.connect(**credentials)   #                                     #
        except Exception as e:                                  #
            print(f"An error occurred while "                   #
                  f"connecting to database: {e}")               #
            sys.exit(1)                                         #
        cursor = database.cursor()                              #
        # ----------------------------------------------------- #

        # finding suitable length ------------------------------------------------- #
        def longest_entry(column):                                                  #
            return column.astype(str).str.len().max()                               #
                                                                                    #
        max_lengths = dataset.apply(longest_entry).tolist()                         #
        max_lengths_col_name_inc = [max(i,j) for i, j in                            #
                                    zip(max_lengths, datatypes_altered_numeric)]    #
        # ------------------------------------------------------------------------- #

        # table architecture ---------------------------------------------------------------------------------------------- #
        architecture_str = ""                                                                                               #
        for i in range(len(max_lengths)):                                                                                   #
            architecture_str = architecture_str + " " + columns[i] + " varchar(" + str(max_lengths_col_name_inc[i]) + "),"  #
        architecture_str = "(" + architecture_str[1:-1] + ")"                                                               #
        # ----------------------------------------------------------------------------------------------------------------- #

        # force create table / delete if exist -------------------------------- #
        try:                                                                    #
            cursor.execute(f"drop table {table_name}")                          #
            print("Table {table_name} has been dropped: force create used")     #
        except Exception as e:                                                  #
            print(f"Table {table_name} does not exist: force create not used")               #
        # --------------------------------------------------------------------- #

        # create table -------------------------------------------------------- #
        try:                                                                    #
            cursor.execute(f"create table {table_name} {architecture_str}")     #
            status = 1                                                          #
        except Exception as e:                                                  #
            print(f"An error occurred while "                                   #
                  f"creating a table: {e}")                                     #
            sys.exit(1)                                                         #
        # --------------------------------------------------------------------- #

        database.commit()
        cursor.close()
        database.close()

    else:

        print("Dataset type not supported")

    if status == 0:
        print(f"Could not create table {table_name}")
    else:
        print(f"Table {table_name} created successfully")