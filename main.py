#!/usr/bin/python3
import os
import cmd
import threading
from flask import Flask
from dotenv import load_dotenv
from persistence.database import db
from api import api_controller, api_amenities, api_country_city, api_place, api_review


#Load environment variables from .env
load_dotenv()

# Set up the Flask application
app = Flask(__name__)

# Database configuration
"""db_uri = 'sqlite:///development.db' if os.getenv('FLASK_ENV') == 'development' else os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False"""

config_class = 'config.DevelopmentConfig' if os.getenv('ENV') == 'development' else 'config.ProductionConfig'
app.config.from_object(config_class)

# Initialize the database with the application
db.init_app(app)

# Register all Flask blueprints
app.register_blueprint(api_controller.app)
app.register_blueprint(api_amenities.app)
app.register_blueprint(api_country_city.app)
app.register_blueprint(api_place.app)
app.register_blueprint(api_review.app)

def run_flask_app():
    with app.app_context():
        db.create_all()  #
        app.run(debug=app.config['DEBUG'], use_reloader=False)


# CRUD in the console
class CRUD:
    def __init__(self):
        self.data = []

    def create(self, item):
        self.data.append(item)
        print(f"Item '{item}' created.")

    def read(self):
        if not self.data:
            print("No items found.")
        else:
            for idx, item in enumerate(self.data, 1):
                print(f"{idx}. {item}")

    def update(self, index, new_item):
        if 0 <= index < len(self.data):
            old_item = self.data[index]
            self.data[index] = new_item
            print(f"Item '{old_item}' updated to '{new_item}'.")
        else:
            print("Invalid index.")

    def delete(self, index):
        if 0 <= index < len(self.data):
            removed_item = self.data.pop(index)
            print(f"Item '{removed_item}' deleted.")
        else:
            print("Invalid index.")



class CRUDConsole(cmd.Cmd):
    intro = "Welcome to the CRUD console. Type help or ? to list commands.\n"
    prompt = "(crud) "

    def __init__(self, crud):
        super().__init__()
        self.crud = crud

    def do_create(self, arg):
        "Create a new item: CREATE item"
        self.crud.create(arg)

    def do_read(self, arg):
        "Read all items: READ"
        self.crud.read()

    def do_update(self, arg):
        "Update an item by index: UPDATE index new_item"
        try:
            index, new_item = arg.split(" ", 1)
            self.crud.update(int(index) - 1, new_item)
        except ValueError:
            print("Invalid syntax. Use: UPDATE index new_item")

    def do_delete(self, arg):
        "Delete an item by index: DELETE index"
        try:
            index = int(arg) - 1
            self.crud.delete(index)
        except ValueError:
            print("Invalid syntax. Use: DELETE index")

    def do_exit(self, arg):
        "Exit the console: EXIT"
        print("Goodbye!")
        return True

if __name__ == '__main__':
    #Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    crud = CRUD()
    CRUDConsole(crud).cmdloop()
