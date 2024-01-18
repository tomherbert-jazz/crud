import streamlit as st
import pyodbc
import uuid
import pandas as pd


#connect to tomdb azure

server = 'tcp:tomwinserver.database.windows.net'
database = 'TomDB'
username = 'therbert'
password = 'Pebbles11.'
driver= '{ODBC Driver 17 for SQL Server}'

mydb = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

mycursor=mydb.cursor()
print("Connection Establisheda")

#Create App

def main():
    #st.title("Customer Contact - AZURE SQL")
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>Customer Contact With AZURE SQL</h1>", unsafe_allow_html=True)
    
    #CRUD Operations
    option=st.sidebar.selectbox("Select Operation",("Create", "Read", "Update", "Delete")) 
    
    #Perform Selected CRUD Operations
    if option == "Create":
     id = str(uuid.uuid4())
     first_name = st.text_input("Enter First Name")
     last_name = st.text_input("Enter Last Name")
     email = st.text_input("Enter Email")   


     if st.button("Create"):
          
          sql = "INSERT INTO Customers (id, FirstName, LastName, Email) VALUES"
          val = f"('{id}','{first_name}', '{last_name}', '{email}')"
          mycursor.execute(sql + val)
          mydb.commit()
          st.success("Record created successfully!!!")

    elif option=="Read":
        st.subheader("Read Records") 
        mycursor.execute('select id, LastName, FirstName, Email from Customers order by LastName')
        result = mycursor.fetchall()
        #for row in result:
            #st.write(row)
        #print(result)
        #result = [tuple(row) for row in result if len(row) == 4]
        result = [list(row) for row in result]     
        df = pd.DataFrame(result, columns=['ID', 'Last Name', 'First Name', 'Email'])
        st.dataframe(df)


    elif option=="Update":
        st.subheader("Update a Record") 
       # id=st.number_input("Enter ID") #,min_value=1)
        id=st.text_input("Enter ID")
        last_name=st.text_input("Enter New Last Name")
        first_name=st.text_input("Enter New First Name")
        email=st.text_input("Enter New Email")
        
        
        if st.button("Update"):
            #sql="update Customers set last_name=%s, first_name=%s,email=%s where id =%s"
            #val=(last_name,first_name,email,id)
            sql = f"UPDATE Customers SET LastName='{last_name}', FirstName='{first_name}', Email='{email}' WHERE id='{id}'"
            mycursor.execute(sql)
           
            #mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Updated Successfully!!!")

    elif option=="Delete":
        st.subheader("Delete a Record")
        #id=st.number_input("Enter ID",min_value=1)
        id=st.text_input("Enter ID")
        if st.button("Delete"):
            sql = f"DELETE FROM Customers WHERE id='{id}'"
            mycursor.execute(sql)
            #sql="delete from Customers where id =%s"
            #val=(id,)
            #mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Deleted Successfully!!!")     




if  __name__ == "__main__":
    main()