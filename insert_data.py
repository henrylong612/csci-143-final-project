import argparse
import sqlalchemy
from tqdm import tqdm
import random
import string
import time

parser = argparse.ArgumentParser()
parser.add_argument('--db', required=True) 
parser.add_argument('--user_rows', default=100)
args = parser.parse_args()

engine = sqlalchemy.create_engine(args.db, connect_args={
    'application_name': 'insert_data.py',
    })
connection = engine.connect()

# Read words from the dictionary file
with open('dictionary.txt', 'r') as file:
    word_list = file.read().split('\n')

for i, word in enumerate(word_list):
    sql = sqlalchemy.sql.text("""
    INSERT INTO fts_word (word) VALUES (:w);
    """)

    try:
        res = connection.execute(sql, {
            'w': word
        })
        if i % 1000 == 0:
            print('word', i)
    except sqlalchemy.exc.IntegrityError as e:
        pass

def generate_words(num_words):
    random_words = random.sample(word_list, num_words)
    return random_words

# Function to generate random users
def generate_users(num_users):
    for i in tqdm(range(num_users), desc="Generating Users"):
        username = '_'.join(generate_words(3))  # Adjust length as needed
        password = '_'.join(generate_words(3))  # Adjust length as needed
        age = random.randint(18, 80)
        sql = sqlalchemy.sql.text("""
        INSERT INTO users (username, password, age) VALUES (:u, :p, :a);
        """)
        try:
            res = connection.execute(sql, {
                'u': username,
                'p': password,
                'a': age
                })
        except sqlalchemy.exc.IntegrityError as e:
            print("user",i,"FAIL",e)

# Function to generate random URLs
def generate_urls(num_urls):
    for i in tqdm(range(num_urls), desc="Generating URLs"):
        url = '_'.join(generate_words(3))  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
        INSERT INTO urls (url) VALUES (:url);
        """)
        try:
            res = connection.execute(sql, {
                'url': url
                })
        except sqlalchemy.exc.IntegrityError as e:
            print("url",i,"FAIL",e)

# Function to generate random messages
def generate_messages(num_messages):
    sql = sqlalchemy.sql.text("""
    SELECT id FROM users;
    """)
    res = connection.execute(sql)
    sender_ids = [tup[0] for tup in res.fetchall()]
    print(sender_ids)
    for i in tqdm(range(num_messages), desc="Generating Messages"):
        sender_id = random.choice(sender_ids)
        message = ' '.join(generate_words(10))  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
        INSERT INTO messages (sender_id, message) VALUES (:si, :m);
        """)
        try:
            res = connection.execute(sql, {
                'si': sender_id,
                'm': message
                })
        except sqlalchemy.exc.IntegrityError as e:
            print("message",i,"FAIL",e)


start_time = time.time()

# Call functions to generate data
generate_users(int(args.user_rows))
generate_urls(int(args.user_rows))
generate_messages(10 * int(args.user_rows))

end_time = time.time()

runtime = end_time - start_time

print('runtime =', runtime)

# Close the connection
connection.close()
