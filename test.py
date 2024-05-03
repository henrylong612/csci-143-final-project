import sqlalchemy
import bleach

engine = sqlalchemy.create_engine("postgresql://postgres:pass@postgres:5432", connect_args={
    'application_name': '__init__.py',
    })
connection = engine.connect()

import bleach

def query_messages(query, a):
    messages = []
    sql = sqlalchemy.sql.text("""
    SELECT sender_id,message,created_at
    FROM messages
    WHERE to_tsvector(message) @@ to_tsquery(:query)
    ORDER BY created_at DESC LIMIT 50 OFFSET :offset;
    """)
    res = connection.execute(sql, {
       'offset': a,
       'query': query
        })
    for row_messages in res.fetchall():
        # convert sender_id into a username
        sql = sqlalchemy.sql.text("""
        SELECT id,username,password,age
        FROM users
        WHERE id=:id;
        """)
        user_res = connection.execute(sql, {'id': row_messages[0]})
        row_users = user_res.fetchone()
        message = row_messages[1]
        cleaned_message = bleach.clean(message)
        linked_message = bleach.linkify(cleaned_message)
        image_url = 'https://robohash.org/' + row_users[1]
        # build the message dictionary
        messages.append({
            'id': row_messages[3],
            'message': linked_message,
            'username': row_users[1],
            'age': row_users[3],
            'created_at': row_messages[2],
            'image_url': image_url
        })
    return messages
