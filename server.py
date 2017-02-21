#!/usr/bin/python

from flask import Flask, request, render_template, abort
import database_helper as db
import checker
import string
import random
import json
import re

from User import User
from Message import Message, MessageList
from ReturnedData import ReturnedData


app = Flask(__name__)

# START route declarations

@app.route("/client.js")
def clientjs():
    return app.send_static_file("client.js")

@app.route("/client.css")
def clientcss():
    return app.send_static_file("client.css")

@app.route("/serverstub.js")
def serverstubjs():
    return app.send_static_file("serverstub.js")

@app.route("/wimage.png")
def wimage():
    return app.send_static_file("wimage.png")

@app.route('/')
def index():
    return render_template('client.html')

# END route declarations


def token_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route("/sign_in", methods=["POST"])
def sign_in():
    data = request.get_json(silent = True) # get data
    valid, response = checker.check_sign_in_data(data)
    if not valid:
        return response
    try:
        userId = db.get_userId_by_email(data["email"])
        if userId == None:
            return ReturnedData(False, "Email not found").createJSON()
        elif db.get_user_by_id(userId).password != data["password"]:
            return ReturnedData(False, "The password is not correct").createJSON()
        else:
            token = token_generator()
            jToken = {}
            jToken["token"] = token
            jToken = json.dumps(jToken)
            db.insert_token(token, userId)
            return ReturnedData(True, "User signed in", jToken).createJSON()
    except:
        abort(500)


@app.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json(silent = True) # get data
    valid, response = checker.check_sign_up_data(data)
    if not valid:
        return response
    try:
        if db.get_userId_by_email(data["email"]) != None:  # no success
            return ReturnedData(False, "Email already exists").createJSON()
        else:
            user = User(data["email"], data["password"], data["firstname"],
                        data["familyname"], data["gender"], data["city"], data["country"])
            db.insert_user(user)
            return ReturnedData(True, "User successfully created").createJSON()
    except:
        abort(500)

@app.route("/sign_out", methods=["POST"])
def sign_out():
    data = request.get_json(silent = True)
    valid, response = checker.check_token(data)
    if not valid:
        return response
    try:
        if db.delete_token(data["token"]):
            return ReturnedData(True, "Signed out").createJSON()
        else:
            return ReturnedData(False, "You are not logged in (Invalid token)").createJSON()
    except:
        alert(500)


@app.route("/change_password", methods=["POST"])
def change_password():
    data = request.get_json(silent = True)
    valid, response = checker.check_change_password_data(data)
    if not valid:
        return response
    try:
        userId = db.get_userId_by_token(data["token"])
        if userId == None:
            return ReturnedData(False, "The token is not correct").createJSON()
        elif db.get_user_by_id(userId).password != data["old_password"]:
            return ReturnedData(False, "The password is not correct").createJSON()
        else:
            db.change_user_password(userId, data["new_password"])
            return ReturnedData(True, "Password changed").createJSON()
    except:
        abort(500)

@app.route("/get_user_data_by_token", methods=["POST"])
def get_user_data_by_token():
    data = request.get_json(silent = True)
    valid, response = checker.check_token(data)
    if not valid:
        return response
    try:
        userId = db.get_userId_by_token(data["token"])
        if userId == None:
            return ReturnedData(False, "You are not logged in (Invalid token)").createJSON()
        else:
            user = db.get_user_by_id(userId)
            return ReturnedData(True, "User found", user.createJSON()).createJSON()
    except:
        abort(500)


@app.route("/get_user_data_by_email", methods=["POST"]) #TODO: Name changed, remember to change it on lab3
def get_user_data_by_email():
    data = request.get_json(silent = True)
    valid, response = checker.check_token_and_email(data)
    if not valid:
        return response
    try:
        myUserId = db.get_userId_by_token(data["token"])
        if myUserId  == None:
            return ReturnedData(False, "You are not logged in (Invalid token)").createJSON()
        else:
            userId = db.get_userId_by_email(data["email"])
            if userId == None:
                return ReturnedData(False, "Invalid email").createJSON()
            else:
                user = db.get_user_by_id(userId)
                return ReturnedData(True, "User found", user.createJSON()).createJSON()
    except:
        abort(500)

@app.route("/get_user_messages_by_token", methods=["POST"])
def get_user_messages_by_token():
    data = request.get_json(silent = True)
    valid, response = checker.check_token(data)
    if not valid:
        return response
    try:
        userId = db.get_userId_by_token(data["token"])

        if userId == None:
            return ReturnedData(False, "You are not logged in (Invalid token)").createJSON()
        else:
            messages = db.get_messages_by_user(userId)
            return ReturnedData(True, "Messages found", messages.createJSON()).createJSON()
    except:
        abort(500)


@app.route("/get_user_messages_by_email", methods=["POST"])
def get_user_messages_by_email():
    data = request.get_json(silent = True)
    valid, response = checker.check_token_and_email(data)
    if not valid:
        return response
    try:
        if db.get_userId_by_token(data["token"]) == None:
            return ReturnedData(False, "You are not logged in (Invalid token)").createJSON()
        else:
            userId = db.get_userId_by_email(data["email"])
            if userId == None:
                return ReturnedData(False, "Invalid email").createJSON()
            else:
                messages = db.get_messages_by_user(userId)
                return ReturnedData(True, "Messages found", messages.createJSON()).createJSON()
    except:
        abort(500)

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json(silent = True)
    valid, response = checker.check_send_message_data(data)
    if not valid:
        return response
    try:
        writerId = db.get_userId_by_token(data["token"])
        if writerId == None:
            return ReturnedData(False, "You are not logged in (You are not logged in (Invalid token))").createJSON()

        writer = db.get_user_by_id(writerId)

        msg = Message(writer.email, data["reader"], data["msg"])
        toId = db.get_userId_by_email(msg.reader)
        if toId == None:
            return ReturnedData(False, "Invalid reader").createJSON()

        fromId = db.get_userId_by_email(msg.writer)
        if fromId == None:
            return ReturnedData(False, "Invalid writer").createJSON()
        else:
            db.insert_message(msg)
            return ReturnedData(True, "Message sent").createJSON()
    except:
        abort(500)

if __name__ == "__main__":
    app.run()
