import os
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

if os.environ.get('FLASK_ENV') != 'production':
    app.config.from_object('CollegeRanking.settings.DevelopmentConfig')
else:
    app.config.from_object('CollegeRanking.settings.ProductionConfig')

print(app.config)

db = MongoEngine(app)