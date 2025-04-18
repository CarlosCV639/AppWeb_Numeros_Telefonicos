import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

def load_data_from_sqlite(db_name='data/data.db', table_name='telefonos', suministro=None):
    # Get the absolute path of the database file
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)

    # Use parameterized query to protect against SQL injection
    query = f"SELECT * FROM {table_name} WHERE SUMINISTRO = ?"
    
    # Execute the query with the suministro parameter
    df = pd.read_sql(query, conn, params=(suministro,))
    conn.close()
    
    return df

# Function to log each query in the consultas table
def log_query(db_name='data/data.db', table_name = 'consultas', suministro=None, user=None):
    # Get the absolute path of the database file
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Insert the query data (SUMINISTRO, DATETIME, USER)
    query = f'''
    INSERT INTO {table_name} (SUMINISTRO, DATETIME, USER)
    VALUES (?, ?, ?)
    '''
    c.execute(query, (suministro, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user))
    
    conn.commit()
    conn.close()

# Function to count queries made by the user today
def count_queries_today(db_name='data/data.db', table_name = 'consultas', user=None):
    # Get the absolute path of the database file
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get the current date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Count the number of queries made today by the user
    query = f'''
    SELECT COUNT(*) FROM {table_name}
    WHERE USER = ? AND DATETIME LIKE ?
    '''
    c.execute(query, (user, today + '%'))
    
    count = c.fetchone()[0]
    conn.close()
    
    return count

# User credentials (this is just a basic example)
USER_CREDENTIALS = {
    "pordefinir": "pordefinir",
    "prueba": "prueba"
}


# Function to get the current query count from the "consultas" table
def get_query_count(username, db_name='data/data.db'):
    # Get the absolute path of the database file
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get the current date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Count the number of queries made today by the user from the "consultas" table
    query = '''
    SELECT COUNT(*) FROM consultas
    WHERE USER = ? AND DATETIME LIKE ?
    '''
    c.execute(query, (username, today + '%'))
    
    count = c.fetchone()[0]
    conn.close()
    
    return count, today

# Function to update the query count and last query date in the database
def update_query_count(username, query_count, last_query_date, db_name='data/data.db'):
    # Get the absolute path of the database file
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if the user exists in the table
    c.execute('SELECT count FROM consultas WHERE username = ?', (username,))
    result = c.fetchone()
    
    if result:
        # Update the existing record
        c.execute('UPDATE query_count SET count = ?, last_query_date = ? WHERE username = ?',
                  (query_count, last_query_date, username))
    else:
        # Insert a new record
        c.execute('INSERT INTO query_count (username, count, last_query_date) VALUES (?, ?, ?)',
                  (username, query_count, last_query_date))
    
    conn.commit()
    conn.close()

# # Function to reset the query count if it's a new day
# def reset_query_count(username):
#     current_date = str(datetime.now().date())
#     query_count, last_query_date = get_query_count(username)
    
#     if last_query_date != current_date:
#         query_count = 0  # Reset the query count
#         last_query_date = current_date
#         update_query_count(username, query_count, last_query_date)
    
#     return query_count, last_query_date

# Limit the number of queries per day
MAX_QUERIES_PER_DAY = 50

# Function for login process
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.success("Usuario correcto. Click nuevamente en Ingresar")
    else:
        st.error("Usuario o contraseña inválida")

# Function for logout process
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.success("Desconectado")

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Login page
if not st.session_state.authenticated:
    st.title("Ingreso")
    
    # Input for username and password
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    # Login button
    if st.button("Ingresar"):
        login(username, password)
else:
    # Once authenticated, fetch the query count for the user
    query_count, last_query_date = get_query_count(st.session_state.username)
    
    # Check if the user has exceeded their query limit
    if query_count < MAX_QUERIES_PER_DAY:
        st.title("Búsqueda de teléfono")

        # Input box for searching
        suministro = st.text_input("Ingrese suministro:")

        # If input is provided, filter the DataFrame from the SQLite database
        if suministro:
            filtered_df = load_data_from_sqlite(db_name='data/data.db', table_name='telefonos', suministro=suministro)
            filtered_df['TELEFONO'] = filtered_df['TELEFONO'].astype(str)
            
            if not filtered_df.empty:
                st.write("Teléfonos encontrados:")
                st.dataframe(filtered_df[['SUMINISTRO', 'TELEFONO']])
                
                # Log the query in the consultas table
                log_query(suministro=suministro, user=st.session_state.username, db_name='data/data.db')
                
                # Count the number of queries made today
                query_count = count_queries_today(user=st.session_state.username, db_name='data/data.db')
            else:
                st.write("Sin teléfonos asociados.")
            
            st.write(f"Búsquedas hechas hoy: {query_count}/{MAX_QUERIES_PER_DAY}")
        
    else:
        # If query limit is reached, show a different page
        st.title("No se permiten más búsquedas hoy")
        st.write("Ha alcanzado el límite de 40 búsquedas diarias.")

    # Add a logout button
    if st.button("Salir"):
        logout()
