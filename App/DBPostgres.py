import psycopg2

hostname = 'dpg-cfc4t15a4998vdd76ugg-a.oregon-postgres.render.com'
database = 'mydb_fpx2'
username = 'mydb_fpx2_user'
pwd = 'jaiibUNVQ0ShPVOGjkbFOdRoAhQMM8eL'
port_id = '5432'
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )
    cur = conn.cursor()

    User_Insert = 'INSERT INTO public.user (id, username, password) VALUES (%s, %s, %s)'
    test_user = (2, 'tim', 'timpass')

    cur.execute(User_Insert, test_user)

    conn.commit()    
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()