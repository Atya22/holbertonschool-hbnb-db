#!/usr/bin/python3
from flask import Flask, jsonify, request
from model.users import User
from persistence.data_manager import DataManager
from persistence.database import db
import re
from uuid import UUID

app = Flask(__name__)
data_manager = DataManager()


def validate_email(email):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email)
