import streamlit as st
import pyodbc 
import pandas as pd

# Database connection
#conn = pyodbc.connect(
 #   "Driver={ODBC Driver 17 for SQL Server};"
  #  f"Server=tcp:tomwinserver.database.windows.net;"
  #  f"Database=TomDB;"
  #  f"Uid=therbert;Pwd=Pebbles11;"
#)

#connect to tomdb azure

server = 'tcp:tomwinserver.database.windows.net'
database = 'TomDB'
username = 'therbert'
password = 'Pebbles11.'
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor=conn.cursor()
print("Connection Established")



def load_data():
    cursor.execute("SELECT * FROM Customers ORDER BY LastName")
    data = cursor.fetchall()
    #return pd.DataFrame(data, columns=['ID','Last Name','First Name','Email'])
    return pd.DataFrame(data, columns=['ID','Last Name','First Name','Email'], dtype=object)


def update_record(df):
    for index, row in df.iterrows():
        sql = f"""
            UPDATE Customers 
            SET LastName=?, FirstName=?, Email=? 
            WHERE ID=?
        """
        values = (row['Last Name'], row['First Name'], row['Email'], row['ID'])
        cursor.execute(sql, values)
    conn.commit()
        
def main():
    
    # Load data into DataFrame
    df = load_data()
    
    # Show data in Streamlit
    df_edit = st.dataframe(df)
    
    # Update database
    update_record(df_edit.dataframe)
    

if __name__ == '__main__':
    main()