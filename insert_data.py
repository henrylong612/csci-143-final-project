import argparse
import sqlalchemy
from sqlalchemy import create_engine
from tqdm import tqdm
import random
import string

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--print_every', type=int, default=1000)
args = parser.parse_args()

# Create database connection
engine = create_engine('postgresql://postgres:pass@postgres:5432', connect_args={'application_name': 'insert_data.py'})
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
        password = generate_random_alphanumeric(12)  # Adjust length as needed
        age = random.randint(18, 80)
        connection.execute("INSERT INTO users (username, password, age) VALUES (%s, %s, %s)", (username, password, age))
        print("user",i)

# Function to generate random URLs
def generate_urls(num_urls):
    for i in tqdm(range(num_urls), desc="Generating URLs"):
        url = generate_random_alphanumeric(20)  # Adjust length as needed
        connection.execute("INSERT INTO urls (url) VALUES (%s)", (url,))
        print("url",i)

# Function to generate random messages
def generate_messages(num_messages):
    for i in tqdm(range(num_messages), desc="Generating Messages"):
        sender_id = random.randint(1, 100)  # Assuming users have IDs up to 1 million
        message = generate_random_alphanumeric(100)  # Adjust length as needed
        connection.execute("INSERT INTO messages (sender_id, message) VALUES (%s, %s)", (sender_id, message))
        print("message",i)

# Call functions to generate data
generate_users(100)
generate_urls(100)
generate_messages(1000)

# Close the connection
connection.close()
