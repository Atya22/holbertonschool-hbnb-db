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

def validate_city_data(data, is_update=False):
    if 'name' not in data or not data['name'].strip() or 'population' not in data or 'country_code' not in data:
        abort(400, description="Missing required fields: name, population, country_code")
    if not find_country_by_code(data['country_code']):
        abort(404, description=f"Country with code '{data['country_code']}' not found")
    if not is_update:
        existing_city = data_manager.query_all_by_filter(City, City.name == data['name'], City.country_code == data['country_code']).first()
        if existing_city:
            abort(409, description=f"City '{data['name']}' already exists in country '{data['country_code']}'")

