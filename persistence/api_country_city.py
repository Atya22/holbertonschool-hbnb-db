#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.city import City
from model.country import Country
import pycountry
from persistence.data_manager import DataManager
from persistence.database import db
