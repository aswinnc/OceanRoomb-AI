from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from keras.models import load_model
import smtplib
import matplotlib.pyplot as plt
import subprocess
from flask import Flask, jsonify, render_template
from bot_location_map import get_bot_location  # Import the bot location logics
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI environments
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template
from io import BytesIO
import base64
from depth import get_depth_data


from email.mime.text import MIMEText

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Global variable to store battery percentage
battery_percentage = 100

# Load AI model for plastic detection (Ensure the model path is correct)
model = load_model('plastic_detector_model.h5')


def preprocess_image(image):
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def send_email():
    # Set your SMTP server details
    smtp_server = "smtp.gmail.com"  # Example: Gmail SMTP server
    smtp_port = 587  # For starttls
    sender_email = "gandhirajng@gmail.com"  # Your email
    sender_password = "gandhiraj@21"  # Your email password
    recipient_email = "gandhirajranjig@gmail.com"  # Recipient email

    subject = "Operation Started"
    body = "The operation has started after login."

    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connect to the server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Log in to your email account
        server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
        server.quit()  # Close the connection
    except Exception as e:
        print(f"An error occurred while sending email: {e}")


# Routes
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    id_number = request.form['id-number']
    password = request.form['password']

    if username and id_number and password:
        send_email()  # Send email when login is successful
        return redirect(url_for('about'))
    else:
        return "Invalid credentials, please try again."


@app.route('/about')
def about():
    return render_template('about.html')


# Guide page with videos and instructions
@app.route('/guidance')
def guide():
    return render_template('guide.html')


@app.route('/start')
def start_operation():
    return render_template('start_operation.html')


# Battery status route
@app.route('/battery')
def battery_status():
    global battery_percentage
    battery_percentage -= 10
    if battery_percentage < 0:
        battery_percentage = 100

    used_percentage = 100 - battery_percentage
    remaining_percentage = battery_percentage
    hours_left = remaining_percentage // 10

    return render_template(
        'battery_status.html',
        used_percentage=used_percentage,
        remaining_percentage=remaining_percentage,
        hours_left=hours_left
    )


# Route to serve the HTML page
@app.route('/marine_map')
def marine_map():
    return render_template('marine_map.html')  # Render the map page

# API route to get the bot's current location
@app.route('/get_location')
def get_location():
    location = get_bot_location()  # Get the current location
    return jsonify(location)  # Return it as JSON


@app.route('/depth_data')
def depth_analysis():
    # Get the current depth data
    depth_data = get_depth_data()
    depth_values = depth_data['depth_readings']

    # Generate the plot for depth analysis
    plt.figure(figsize=(8, 5))
    plt.plot(depth_values, marker='o', color='blue', label='Depth (m)')
    plt.title('Real-Time Depth Analysis')
    plt.xlabel('Time (s)')
    plt.ylabel('Depth (m)')
    plt.grid(True)
    plt.legend()

    # Save the plot as a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # Render the template and pass the depth data
    return render_template('depth_analysis.html',
                           depth=depth_data['current_depth'],
                           max_depth=depth_data['max_depth'],
                           avg_depth=depth_data['avg_depth'],
                           graph_image=image_base64)


@app.route('/get_depth_data')
def get_depth_data_route():
    # Get the depth data from the backend logic
    depth_data = get_depth_data()

    # Return the data as JSON for dynamic updates
    return jsonify({
        'current_depth': depth_data['current_depth'],
        'max_depth': depth_data['max_depth'],
        'avg_depth': depth_data['avg_depth'],
        'latest_readings': depth_data['depth_readings'][-5:]
    })
# Previous data route
@app.route('/previous_data')
def previous_data():
    data = {
        'Operation': ['Operation 1', 'Operation 2', 'Operation 3'],
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Depth (m)': [10, 20, 15],
        'Plastic Collected (kg)': [5, 3, 8]
    }

    zipped_data = zip(data['Operation'], data['Date'], data['Depth (m)'], data['Plastic Collected (kg)'])

    return render_template('previous_data.html', zipped_data=zipped_data)

# Plastic detection page route
@app.route('/plastic_detection')
def plastic_detection_page():
    return render_template('plastic_detection.html')


# Start collection process route
@app.route('/start-collection')
def start_collection():
    return render_template('plastic_detection.html')


# Define a route to trigger the plastic detection process
@app.route('/start-plastic-collection', methods=['POST'])
def start_plastic_collection():
    try:
        # Call the detect_plastic.py script (or the function inside that file)
        # You can run the script using subprocess, or import the function and call it directly

        # Using subprocess to run the Python script
        subprocess.run(['python',r'C:\Users\Gandhiraj\PycharmProjects\Ocean-RoobAi\backend\detect_plastic.py'], check=True)

        # If successful, send back a success message
        return jsonify({"message": "Plastic collection started successfully!"})
    except Exception as e:
        # Handle errors
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Route for the Collection Process page
@app.route('/collection')
def collection_process():
    return render_template('collection_process.html')
# next
@app.route('/start-metal-collection', methods=['GET'])  # Renamed route to avoid conflict
def start_metal_collection():  # Renamed function to avoid conflict
    try:
        # Run your Python script (metal_detection_Webcame.py)
        subprocess.Popen(['python', 'metal_detection_Webcam.py'])
        return jsonify({"status": "success", "message": "Metal detection started!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
