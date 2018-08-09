import os

from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import config


app = Flask(__name__)
# The environment variable below helps to allow firing up a server with
# of a given configuration without having to edit the code itself. Just your
# environment variables. It also has a default 'production' value
# when it's not set in the environment.
environment = os.getenv('FLASK_ENV', 'production')
app.config.from_object(config.configuration[environment])
api = Api(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from app import models, views
