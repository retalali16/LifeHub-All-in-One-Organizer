from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import googleapiclient.discovery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from bson import ObjectId
from forms import TodoForm
from flask_pymongo import PyMongo
from markupsafe import Markup

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['lifehub_db']
users_collection = db['users_sitteings']
activity_collection = db['activity_logs']
events_collection = db['events_calender']

# Flask-PyMongo setup
app.config["SECRET_KEY"] = "f2330203d221db94b14488386f4ba3a5b0ee38c2b966327a"
app.config["MONGO_URI"] = "mongodb://localhost:27017/lifehub_db"
mongodb_client = PyMongo(app)
db = mongodb_client.db

# YouTube API setup
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Email setup
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Scheduler setup
scheduler = BackgroundScheduler()

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search_youtube(query):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part="snippet", type="video", maxResults=5)
    response = request.execute()

    video_links = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_links.append(video_url)

    return video_links

def send_reminder(event_name, event_date, email):
    subject = f"Reminder: Upcoming Event - {event_name}"
    body = f"Hi there,\n\nThis is a reminder for your upcoming event:\n\nEvent: {event_name}\nDate: {event_date}\n\nBest regards, LifeHub."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
    except Exception as e:
        print(f"Error sending reminder: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/view_todos", methods=["GET"])
def get_todos():
    filter_option = request.args.get("filter", "all")
    todos = []

    # Adjusting query to filter todos based on completion status
    if filter_option == "completed":
        query = {"completed": "True"}
    elif filter_option == "not_completed":
        query = {"completed": "False"}
    else:
        query = {}

    # Fetch todos from MongoDB, sorting by date created
    for todo in db.todos_flask.find(query).sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("view_todos.html", todos=todos, filter_option=filter_option)

@app.route("/add_todo", methods=["POST", "GET"])
def add_todo():
    form = TodoForm(request.form)
    if request.method == "POST" and form.validate():
        todo_data = {
            "name": form.name.data,
            "description": form.description.data,
            "completed": form.completed.data,
            "due_date": form.due_date.data.strftime("%Y-%m-%d"),
            "priority": form.priority.data,
            "date_created": datetime.utcnow(),
        }
        db.todos_flask.insert_one(todo_data)
        flash("Todo successfully added", "success")
        return redirect(url_for('get_todos'))

    return render_template("add_todo.html", form=form)

@app.route("/update_todo/<id>", methods=["POST", "GET"])
def update_todo(id):
    form = TodoForm(request.form)
    if request.method == "POST" and form.validate():
        updated_data = {
            "name": form.name.data,
            "description": form.description.data,
            "completed": form.completed.data,
            "due_date": form.due_date.data.strftime("%Y-%m-%d") if form.due_date.data else None,
            "priority": form.priority.data,
        }
        db.todos_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": updated_data})
        flash("Todo successfully updated", "success")
        return redirect(url_for('get_todos'))

    todo = db.todos_flask.find_one({"_id": ObjectId(id)})
    if todo:
        form.name.data = todo.get("name")
        form.description.data = todo.get("description")
        form.completed.data = todo.get("completed")
        form.due_date.data = datetime.strptime(todo.get("due_date"), "%Y-%m-%d") if todo.get("due_date") else None
        form.priority.data = todo.get("priority")

    return render_template("add_todo.html", form=form)

@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todos_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect(url_for('get_todos'))

@app.route("/view_todo/<id>")
def view_todo(id):
    todo = db.todos_flask.find_one({"_id": ObjectId(id)})
    if not todo:
        flash("Todo not found", "danger")
        return redirect(url_for('get_todos'))
    todo["_id"] = str(todo["_id"])
    todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
    return render_template("view_todo.html", todo=todo)




@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = users_collection.find_one()
    if request.method == 'POST':
        username = request.form.get('username')
        address = request.form.get('address')
        phone = request.form.get('phone')
        file = request.files.get('profile_picture')

        if not username:
            flash("Username cannot be empty!", 'error')
            return redirect(url_for('profile'))

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_picture_path = os.path.join('uploads', filename)
        else:
            profile_picture_path = user.get('profile_picture', 'uploads/default.png')

        users_collection.update_one({}, {'$set': {
            'username': username,
            'address': address,
            'phone': phone,
            'profile_picture': profile_picture_path
        }}, upsert=True)

        flash("Profile updated successfully!", 'success')
        return redirect(url_for('profile'))

    if not user:
        user = {'username': 'New User', 'profile_picture': 'uploads/default.png', 'address': '', 'phone': ''}
        users_collection.insert_one(user)

    return render_template('profile.html', user=user)

@app.route('/log_activity', methods=['POST', 'GET'])
def log_activity():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        activity_type = request.form['activity_type']
        duration = float(request.form['duration'])

        # Calculate calories burned
        calories = (10.0 if activity_type == 'running' else 7.5 if activity_type == 'cycling' else 3.8) * weight * duration / 60
        
        activity_collection.insert_one({
            'weight': weight,
            'activity_type': activity_type,
            'duration': duration,
            'calories_burned': round(calories, 2),
            'timestamp': datetime.now()
        })
        
        # Flash a success message to the user
        flash("Activity logged successfully!", "success")
        return redirect(url_for('log_activity'))

    # Fetch all activity logs from the database, sorted by timestamp
    logs = activity_collection.find().sort('timestamp', -1)
    return render_template('log_activity.html', logs=logs)

@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        event_name = request.form['name']
        description = request.form['description']
        event_date = datetime.strptime(request.form['date'], "%Y-%m-%dT%H:%M")
        reminder_time = datetime.strptime(request.form['reminder_time'], "%Y-%m-%dT%H:%M")
        email = request.form['email']

        event = {
            'name': event_name,
            'description': description,
            'date': event_date,
            'reminder_time': reminder_time,
            'email': email
        }
        events_collection.insert_one(event)

        scheduler.add_job(send_reminder, 'date', run_date=reminder_time, args=[event_name, event_date, email])

    events = events_collection.find().sort('date', 1)
    return render_template('events.html', events=events)

@app.route('/search', methods=['GET', 'POST'])
def search():
    movie = None
    video_links = []
    if request.method == 'POST':
        movie = request.form.get('movie')  # Retrieve movie name from the form
        if movie:
            video_links = search_youtube(movie)  # Fetch video links using the YouTube API

    return render_template('search.html', movie=movie, video_links=video_links)

if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=3000)