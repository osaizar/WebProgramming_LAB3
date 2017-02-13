#!/usr/bin/python

from User import User
from Message import Message
from ReturnedData import ReturnedData
import database_helper as db
import server


def test_db():
    print "Creating 3 users"

    user1 = User("oier@mail.com1", "pw", "Oier", "Saizar", "M", "Tolosa", "EH")
    user2 = User("oier@mail.com2", "pw", "Oier", "Saizar", "M", "Tolosa", "EH")
    user3 = User("oier@mail.com3", "pw", "Oier", "Saizar", "M", "Tolosa", "EH")
    db.insert_user(user1)
    db.insert_user(user2)
    db.insert_user(user3)


    print "Inserting 3 messages"

    message1 = Message("oier@mail.com1", "oier@mail.com2", "message1")
    message2 = Message("oier@mail.com2", "oier@mail.com2", "message2")
    message3 = Message("oier@mail.com3", "oier@mail.com2", "message3")

    db.insert_message(message1)
    db.insert_message(message2)
    db.insert_message(message3)


    print "Creating 3 sessions"

    db.insert_token("firstToken", 1)
    db.insert_token("secondToken", 2)
    db.insert_token("thirdToken", 3)

    print "Getting 3 users"

    user1_1 = db.get_user_by_id(1)
    user2_1 = db.get_user_by_id(2)
    user3_1 = db.get_user_by_id(3)

    if user1.email == user1_1.email:
        print "user1 correct"
    else:
        print "user1 incorrect"

    if user2.email == user2_1.email:
        print "user2 correct"
    else:
        print "user2 incorrect"

    if user3.email == user3_1.email:
        print "user3 correct"
    else:
        print "user3 incorrect"

    print "Getting messages of user2"

    messages = db.get_messages_by_user(db.get_userId_by_email("oier@mail.com2"))

    for msg in messages:
        print msg.content+" "+msg.writer+" "+msg.reader


    print "Changing password of user1"

    db.change_user_password(db.get_userId_by_email("oier@mail.com1"), "123456")

    user1_2 = db.get_user_by_id(1)

    if user1_2.password == "123456":
        print "Change successfull"
    else:
        print "Error on change"

def test_server():

    response = server.sign_up("oier@mail.com1", "pw", "Oier", "Saizar", "M", "Tolosa", "EH")
    print response

    message1 = Message("oier@mail.com1", "oier@mail.com1", "message1")
    message2 = Message("oier@mail.com1", "oier@mail.com1", "message2")
    message3 = Message("oier@mail.com1", "oier@mail.com1", "message3")

    db.insert_message(message1)
    db.insert_message(message2)
    db.insert_message(message3)

    response = server.get_user_messages_by_email("token1","oier@mail.com1")
    print response

def test_error():
    user = db.get_user_by_id(200)
    if user:
        print user.email
    else:
        print user

test_error()
