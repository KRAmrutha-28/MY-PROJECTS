from config.config import get_db_connect 

def user_contact(name,email,message):
    connection = get_db_connect()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO contact (name,email,message)
        VALUES (%s, %s, %s)
    """, (name,email,message))
    
    connection.commit()
    cursor.close()
    connection.close()

        
    