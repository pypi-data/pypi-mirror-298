import mysql.connector
import pandas as pd
import sys



def as_dataframe(credentials: dict, table_name: str) -> pd.DataFrame:

    status = 0

    # try connecting to database -------------------------- #
    try:                                                    #
        database = mysql.connector.connect(**credentials)   #
    except Exception as e:                                  #
        print(f"An error occurred while "                   #
              f"connecting to database: {e}")               #
        sys.exit(1)                                         #
    cursor = database.cursor()                              #
    # ----------------------------------------------------- #

    # check if table exists or if table empty ----------------- #
    try:                                                        #
        cursor.execute(f"select count(*) from {table_name}")    #
        count = cursor.fetchall()[0][0]                         #
        if count == 0:                                          #
            print(f"error: {table_name} has no entries")        #
            sys.exit(1)                                         #
    except Exception as e:                                      #
        print(f"An error occurred while "                       #
              f"fetching table {table_name}: {e}")              #
        sys.exit(1)                                             #
    # --------------------------------------------------------- #

    # fetching data ----------------------------------------------- #
                                                                    #
    cursor.execute(f"show columns from {table_name}")               #
    columns = cursor.fetchall()                                     #
    column_names = [x[0] for x in columns]                          #
    cursor.execute(f"select * from {table_name}")                   #
    dataset_list = cursor.fetchall()                                #
                                                                    #
    datatypes = list(dataset_list[0])                               #
    df = pd.DataFrame(dataset_list[1:], columns=column_names)       #
    type_dict = dict(zip(column_names, datatypes))                  #
    df = df.astype(type_dict)                                       #
    status = 1                                                      #
                                                                    #
    # ------------------------------------------------------------- #

    cursor.close()
    database.close()

    if status == 0:
        print(f"Could not download dataset as dataframe")
    else:
        print(f"Successfully downloaded dataset as dataframe")

    return df