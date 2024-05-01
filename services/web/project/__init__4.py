import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    make_response,
    redirect,
    render_template
)
from werkzeug.utils import secure_filename
import sqlalchemy

app = Flask(__name__)

engine = sqlalchemy.create_engine("postgresql://postgres:pass@postgres:5432", connect_args={
    'application_name': '__init__.py',
    })
connection = engine.connect()

def print_debug_info():
    # requests (PLURAL) library for downloading
    # now we need request (SINGULAR)

    # GET method
    print("request.args.get('username')=",request.args.get('username'))
    print("request.args.get('password')=",request.args.get('password'))

    # POST method
    print("request.form.get('username')=",request.form.get('username'))
    print("request.form.get('password')=",request.form.get('password'))

    # cookies
    print("request.cookies.get('username')=",request.cookies.get('username'))
    print("request.cookies.get('password')=",request.cookies.get('password'))



def are_credentials_good(username, password):

    sql = sqlalchemy.sql.text('''
        SELECT id FROM users
        WHERE username = :username
        AND password = :password
        ;
        ''')

    res = connection.execute(sql, {
        'username': username,
        'password': password
        })

    for row in res.fetchall():
        if res[0]:
            return True
        else:
            return False

def retrieve_messages(a):

    messages = []
    sql = sqlalchemy.sql.text("""
    SELECT sender_id,message,created_at,id
    FROM messages
    ORDER BY created_at DESC LIMIT 50 OFFSET :offset;
    """)

    res = connection.execute(sql, {
        'offset': a
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
        html_message = markdown_compiler2.compile_lines(cleaned_message)
        linked_message = bleach.linkify(html_message)

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



@app.route('/')
def root():
    
    print_debug_info()

    username=request.cookies.get('username')
    password=request.cookies.get('password')
    # good_credentials=are_credentials_good(username, password)
    good_credentials = True
    if good_credentials:
        logged_in=True
    else:
        logged_in=False
    print('logged-in=',logged_in)

    try:
        page_number=int(request.cookies.get('page_number'))
    except TypeError:
        page_number=1
    
    '''
    messages = [{
            'id': 1,
            'message': 1,
            'username': 1,
            'age': 1,
            'created_at': 1,
            'image_url': 1
        }]
    '''

    messages=retrieve_messages(page_number)

    # render the jinja2 template and pass the result to firefox
    
    return render_template('root.html', messages=messages, logged_in=logged_in, username=username, page_number=page_number)

    # render_template does preprocessing of input html file
    # technically, the input to the render_template function is in a language called Jinja2
    # the output of render_template is html


