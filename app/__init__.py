import os
from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
api = Api(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from app import models, views