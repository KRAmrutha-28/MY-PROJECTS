from config.config import get_db_connect

def get_user2():
    connection=get_db_connect()
    cursor=connection.cursor()
    cursor.execute("select *from user2")
    users=cursor.fetchall()
    cursor.close()
    connection.close()
    return users