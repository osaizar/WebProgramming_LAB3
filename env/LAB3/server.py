#!/usr/bin/python

import database_helper as db
import string
import random
from User import User
from Message import Message
from ReturnedData import ReturnedData

#app = Flask(__name__)

def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def sign_in(email, password):
    userId = db.get_userId_by_email(email)
    if userId == None:
        return ReturnedData(False, "Email not found", None).createJSON()
    elif db.get_user_by_id(userIds).password != password:
        return ReturnedData(False, "The password is not correct", None).createJSON()
    else:
        token = token_generator()
        if db.insert_token(token, userId):
            return ReturnedData(True, "User signed in", token).createJSON() # TODO: Hay que pasar token a json?
        else:
            return ReturnedData(False, "Database error", None).createJSON()



def sign_up(email, password, firstname, familyname, gender, city, country):
    if db.get_userId_by_email(email) != None:  # no success
        return ReturnedData(False, "Email already exists", None).createJSON()
    else:
        user = User(email, password, firstname,
                    familyname, gender, city, country)
        if db.insert_user(user):
            return ReturnedData(True, "User successfully created", None).createJSON()
        else:
            return ReturnedData(False, "Database error", None).createJSON()


def sign_out(token):
    if db.delete_token(token):
        return ReturnedData(True, "Signed out", None).createJSON()
    else:
        return ReturnedData(False, "Database error", None).createJSON()


def change_password(token, old_password, new_password):
    userId = db.get_userId_by_token(token)
    if userId == None:
        return ReturnedData(False, "The token is not correct", None).createJSON()
    elif db.get_user_by_id(userIds).password != old_password:
        return ReturnedData(False, "The password is not correct", None).createJSON()
    else:
        if db.change_user_password(userId, new_password):
            return ReturnedData(True, "Password changed", None).createJSON()
        else:
            return ReturnedData(False, "Database error", None).createJSON()

# Empieza Isma


def get_user_data_by_token():
    pass


def get_user_data_by_email():
    pass


def get_user_messages_by_token():
    pass


def get_user_messages_by_email(token, email):
    if db.get_userId_by_token(token) == None:
        return ReturnedData(False, "Invalid Token", None).createJSON()
    else:
        userId = db.get_userId_by_email(email)
        if user == None:
            return ReturnedData(False, "Invalid email", None).createJSON()
        else:
            messages = db.get_messages_by_user(userId)
            rData = ReturnedData(True, "Messages found")
            for msg in messages:
                rData.addToData(msg.createJSON())

            return rData.createJSON()  # Funciona?


def post_message():
    pass
