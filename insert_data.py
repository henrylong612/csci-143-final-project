import argparse
import sqlalchemy
from tqdm import tqdm
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('--db', default="postgresql://postgres:pass@postgres:5432")
args = parser.parse_args()

engine = sqlalchemy.create_engine(args.db, connect_args={
    'application_name': 'insert_data.py',
    })
connection = engine.connect()

# Define characters for alphanumeric string generation
alphanumeric_chars = string.ascii_letters + string.digits

# Function to generate random alphanumeric strings
def generate_random_alphanumeric(length):
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))

# Function to generate random users
def generate_users(num_users):
    for i in tqdm(range(num_users), desc="Generating Users"):
        username = generate_random_alphanumeric(10)  # Adjust length as needed
        password = generate_random_alphanumeric(10)  # Adjust length as needed
        age = random.randint(18, 80)
        sql = sqlalchemy.sql.text("""
        INSERT INTO users (username, password, age) VALUES (:u, :p, :a);
        """)
        res = connection.execute(sql, {
            'u': username,
            'p': password,
            'a': age
            })
        print("user",i)

# Function to generate random URLs
def generate_urls(num_urls):
    for i in tqdm(range(num_urls), desc="Generating URLs"):
        url = generate_random_alphanumeric(10)  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
        INSERT INTO urls (url) VALUES (:url);
        """)
        res = connection.execute(sql, {
            'url': url
            })
        print("url",i)

# Function to generate random messages
def generate_messages(num_messages):
    for i in tqdm(range(num_messages), desc="Generating Messages"):
        sender_id = random.randint(1, 1000000)  # Assuming users have IDs up to 1 million
        message = generate_random_alphanumeric(10)  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
        INSERT INTO messages (sender_id, message) VALUES (:si, :m);
        """)
        res = connection.execute(sql, {
            'si': sender_id,
            'm': message
            })
        print("message",i)

# Call functions to generate data
generate_users(1000000)
generate_urls(1000000)
generate_messages(10000000)

# Close the connection
connection.close()
