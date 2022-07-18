import psycopg2
import pandas as pd

def connect(database="postgres", user='postgres',password='password',host='127.0.0.1',port='5432'):
    conn = psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port
    )
    conn.autocommit = True
    return conn, conn.cursor()

def close_connection(conn, cur):
    cur.close()
    conn.close()

def create_database(cur):
    sql = '''create database ibge_db'''
    cur.execute(sql)
    print("Database created successfully") 

def create_table(cursor, table_name, columns_names, columns_types):
    sql="CREATE TABLE " + table_name + "(\n"
    for i in range(0,len(columns_names)):
        sql+=columns_names[i] + " " + columns_types[i] + ", "
    sql=sql[:-2]+")"
    cursor.execute(sql)

def insert(conn, cur, fields_names,data,table):
    number_fields=len(fields_names)
    sql='INSERT INTO ' + table + '('
    for i in fields_names:
        sql+=str(i)+', '
    sql=sql[:-2]+') VALUES ('
    for i in range(0,number_fields):
        sql+='%s, '
    sql=sql[:-2]+')'
    for d in data:
        cur.execute(sql, d)
    conn.commit()


conn, cur = connect("postgres", 'postgres','password','127.0.0.1','5432')
create_database(cur)
close_connection(conn, cur)
conn, cur = connect("ibge_db", 'root','password','127.0.0.1','5433')

locations_columns = ['id','nome','uf_id','uf_sigla','uf_nome','regiao_id','regiao_nome']
locations_col_types = ['integer', 'text', 'integer', 'text', 'text', 'integer', 'text']
create_table(cur, 'municipios', locations_columns, locations_col_types)
locations_data = pd.read_csv('locations.csv')
locations_data = locations_data.values.tolist()
insert(conn, cur, locations_columns, locations_data, 'municipios')

names_columns = ['nome','local_id','periodo','frequencia']
names_col_types = ['text', 'integer', 'text', 'integer']
create_table(cur, 'nomes', names_columns, names_col_types)
names_data = pd.read_csv('names.csv')
names_data = names_data.values.tolist()
insert(conn, cur, names_columns, names_data, 'nomes')