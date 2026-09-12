from config.config import get_db_connect
import hashlib

# Create a new user
def create_user(first_name, last_name, email_id, mobile_no, password, address, usertype):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    connection = get_db_connect()
    cursor = connection.cursor()

    # Check if email or mobile already exists
    cursor.execute("SELECT * FROM users WHERE email_id=%s OR mobile_no=%s", (email_id, mobile_no))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return "exists"

    # Insert user
    cursor.execute("""
        INSERT INTO users (first_name, last_name, email_id, mobile_no, password, address, usertype)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (first_name, last_name, email_id, mobile_no, hashed_password, address, usertype))
    
    connection.commit()

    # Fetch the inserted user (use email or mobile as unique identifier)
    cursor.execute("SELECT * FROM users WHERE email_id=%s", (email_id,))
    new_user = cursor.fetchone()

    cursor.close()
    connection.close()

    return new_user  # this returns a tuple representing the inserted user

# Login user
def login(email_id, password):
    # Get a database connection
    connection = get_db_connect()
    cursor = connection.cursor()

    # Hash the input password before comparing it with the stored password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if there is a user with the provided email and password
    cursor.execute("SELECT * FROM users WHERE email_id=%s AND password=%s", (email_id, hashed_password))
    user = cursor.fetchone()

    # Close the connection and cursor
    cursor.close()
    connection.close()

    # If user found, return the user data; otherwise, return None
    if user:
        return user
    else:
        return None

# Update password (forgot password feature)
def forgotpassword(email_id, new_password):
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    connection = get_db_connect()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE email_id=%s", (hashed_password, email_id))
    connection.commit()
    cursor.close()
    connection.close()
    return "updated"


def get_user_by_id(user_id):
    connection = get_db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userID = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row:
        return {
            'userID': row['userID'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email_id': row['email_id'],
            'mobile_no': row['mobile_no'],
            'password': row['password'],
            'address': row['address'],
            'usertype': row['usertype']
        }
    return None





