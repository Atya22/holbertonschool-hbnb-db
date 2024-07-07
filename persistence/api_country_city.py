#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.city import City
from model.country import Country
import pycountry
from persistence.data_manager import DataManager
from persistence.database import db

app = Flask(__name__)
data_manager = DataManager()

def find_country_by_code(country_code):
    return pycountry.countries.get(alpha_2=country_code.upper())
