from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "db24c608640f5034b30b8e1e1eb5618ed0ffdbf5"
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db
print("Database initialized:", db)


from application import routes