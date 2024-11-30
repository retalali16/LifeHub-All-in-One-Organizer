from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "db24c608640f5034b30b8e1e1eb5618ed0ffdbf5"
# app.config["MONGO_URI"] = "mongodb+srv://smostafaahmed:MW70J69NbYYr8800@cluster0.84fy8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db
print("Database initialized:", db)


from application import routes