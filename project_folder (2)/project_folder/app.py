from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
users_collection = db['users']

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    user = users_collection.find_one()
    if not user:
        user = {
            'username': 'New User', 
            'profile_picture': 'uploads/default.png', 
            'address': '', 
            'phone': ''
        }
        users_collection.insert_one(user)
        
    if not user.get('profile_picture'):
        user['profile_picture'] = 'uploads/default.png'
    return render_template('profile.html', user=user)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = request.form.get('username')
    address = request.form.get('address')
    phone = request.form.get('phone')
    file = request.files['profile_picture']

    if not username:
        flash("Username cannot be empty!", 'error')
        return redirect(url_for('index'))

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        profile_picture_path = filename  
    else:
        profile_picture_path = request.form.get('current_profile_picture')

    users_collection.update_one({}, {'$set': {
        'username': username,
        'address': address,
        'phone': phone,
        'profile_picture': profile_picture_path
    }})

    flash("Profile updated successfully!", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
