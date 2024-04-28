#!/usr/bin/python3

import datetime
import random
'''
Create a database for the Twitter project.
'''

madlibs = [
    "American [BUSINESSMAN] Andrew Yang, [FLAWS], [REPRESENTS] [ESSENTIAL] [DEPARTURE] from the [NORM]. Yang's rise to [FAME] began in the 2020 Democratic primaries. Yang [PROMOTED] [SEVERAL] [UNORTHODOX] [PROPOSALS] including a universal basic income [UBI] funded by a value-added tax [VAT].",
    "Andrew Yang is a [SPECIAL] politcian. [HIS] 2020 campaign centered around a universal basic income [UBI] proposal in which every [CITIZEN] would receive $1000/month regardless of their income. This [PROPOSAL], though not a panacea, would be a major improvement on our [INEFFICIENT] current welfare [SYSTEM].",
    "Andrew Yang recently [STARTED] the Forward Party. While this party may ultimately be counterproductive and [INEFFECTIVE], it does [PROMOTE] common-sense voting reform, including measures like [PRIMARY]. It also [REPRESENTS] a commitment to moving beyond the [LEFT] [BINARY].",
    "Andrew Yang hosts a podcast called Yang Speaks. On this podcast, Yang [TALKS] with people across the political [AISLE] about pressing [POLITICAL] issues. My personal favorite episode is when he [TALKS] with NYU Professor Jonathan Haidt about the [DETERMINANTS] what makes [SOMEONE] a [LIBERAL].",
    "Andrew Yang [PROMOTES] a lot of [UNORTHODOX] [PROPOSALS]. For example, he [PROMOTES] universal basic income [UBI], [PAYING] [COLLEGE] athletes, and automatic tax filing. Many of these [PROPOSALS] are overlooked simply because [MAINSTREAM].",
    "Andrew Yang [REPRESENTS] a [DEPARTURE] from the [LEFT] [BINARY]. His new party, the Forward Party, [AIMS] to bring [AMERICANS] together under common sense [PROPOSALS]. Hopefully, this kind of thinking will [QUELL] partisan [STRIFE]."
    ]

replacements = {
    'BUSINESSMAN' : ['businessman', 'entrepreneur', 'tycoon'],
    'FLAWS' : ['while he has his flaws', 'although not perfect', 'despite his limitations'],
    'ESSENTIAL' : ['an essential', 'a much-needed', 'an important'],
    'NORM' : ['norm', 'status-quo', 'traditional politician'],
    'FAME' : ['fame', 'stardom', 'prominence'],
    'PROMOTED' : ['promoted', 'advocated for', 'supported'],
    'SEVERAL' : ['several', 'a number of', 'multiple'],
    'UBI' : ['(UBI)', '(also known as UBI)'],
    'VAT' : ['(also known as a VAT)', '(VAT)', '(or VAT)'],
    'SPECIAL' : ['special', 'unique'],
    'HIS' : ['his', 'Yang\'s'],
    'CITIZEN' : ['U.S. citizen', 'American'],
    'PROPOSAL' : ['proposal', 'idea', 'policy'],
    'INEFFICIENT' : ['inefficient', 'bureaucratic', 'red-tape ridden'],
    'SYSTEM' : ['system', 'regime', 'programs'],
    'STARTED' : ['founded', 'created', 'started'],
    'INEFFECTIVE' : ['ineffective', 'unhelpful'],
    'PROMOTE' : ['promote', 'support', 'advocate for'],
    'PRIMARY' : ['ranked-choice voting', 'open primaries'],
    'REPRESENTS' : ['represents', 'symbolizes', 'relfects'],
    'BINARY' : ['binary', 'dichotomy', 'paradigm'],
    'TALKS' : ['talks', 'discusses', 'chats'],
    'AISLE' : ['aisle', 'spectrum'],
    'POLITICAL' : ['political', 'social and economic'],
    'DETERMINANTS' : ['determinants of', 'factors contributing to', 'contributing factors for'],
    'SOMEONE' : ['someone', 'a person'],
    'LIBERAL' : ['liberal or conservative', 'Republican or a Democrat'],
    'UNORTHODOX' : ['unorthodox', 'unconventional', 'out of the ordinary'],
    'PROMOTES' : ['promotes', 'advocates for', 'supports'],
    'PROPOSALS' : ['proposals', 'ideas', 'policies'],
    'PAYING' : ['paying', 'compensating'],
    'COLLEGE' : ['college', 'collegiate', 'NCAA'],
    'MAINSTREAM' : ['they are not mainstream', 'many deem the issues unimportant', 'they are not often discussed on the news'],
    'DEPARTURE' : ['departure', 'break', 'shift'],
    'LEFT' : ['left-right', 'liberal-conservative', 'Republican-Democrat'],
    'AIMS' : ['aims', 'is an attempt'],
    'AMERICANS' : ['Americans', 'people'],
    'QUELL' : ['quell', 'calm'],
    'STRIFE' : ['strife', 'tensions'],
    }


def generate_comment():
    '''
    This function generates random comments according to the patterns specified in the `madlibs` variable.

    To implement this function, you should:
    1. Randomly select a string from the madlibs list.
    2. For each word contained in square brackets `[]`:
        Replace that word with a randomly selected word from the corresponding entry in the `replacements` dictionary.
    3. Return the resulting string.

    For example, if we randomly selected the madlib "I [LOVE] [PYTHON]",
    then the function might return "I like Python" or "I adore Programming".
    Notice that the word "Programming" is incorrectly capitalized in the second sentence.
    You do not have to worry about making the output grammatically correct inside this function.
    Instead, you should ensure that the madlibs that you create will all be grammatically correct when this substitution procedure is followed.
    '''
    madlib=random.choice(madlibs)
    for replacement in replacements.keys():
        madlib=madlib.replace('['+replacement+']',random.choice(replacements[replacement]))
    return madlib

# sqlite3 is built in python3, no need to pip3 install
import sqlite3

# process command line arguments
import argparse
parser = argparse.ArgumentParser(description='Create a database for the twitter project')
parser.add_argument('--db_file', default='twitter_clone.db')
# there is no standard file extension; people use .db .sql .sql3 .database
args = parser.parse_args()

# connect to the database
con = sqlite3.connect(args.db_file)   # con, conn = connection; always exactly 1 of these variables per python project
cur = con.cursor()                    # cur = cursor; for our purposes, exactly 1 of these per python file

# create the users table
sql = '''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER
);
'''
cur.execute(sql)     # cur.execute() actually runs the SQL code
con.commit()         # "commit" means "save" in SQL terminology; not always required, but never wrong

# create the messages table
sql = '''
create table messages (
    id integer primary key,
    sender_id integer not null,
    message text not null,
    created_at timestamp not null default current_timestamp
    );
'''
cur.execute(sql)
con.commit()

for i in range(250):
    username='username'+str(i)
    password='password'+str(i)
    age=i
    sql="""insert into users (username, password, age) values (?, ?, ?);"""
    cur.execute(sql, [username, password, age])
    con.commit()

    for j in range(250):
        print('i=',i,', j=',j)
        sender_id=i
        message=generate_comment()
        created_at=str(datetime.datetime.now()).split('.')[0]
        sql="""
        insert into messages (sender_id,message,created_at) values
        (?, ?, ?);
        """
        cur.execute(sql, [sender_id, message, created_at])
        con.commit()
