from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import numpy as np
import os
import csv
from datetime import datetime
import base64
import re

app = Flask(__name__)

# Configure Flask for larger file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['MAX_CONTENT_PATH'] = None

# Load face cascade classifier
haar_file = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

# Check if face recognition module is available
if not hasattr(cv2, 'face'):
    print("WARNING: OpenCV face recognition module not available!")
    print("This will prevent face recognition from working properly.")
    print("Make sure opencv-contrib-python-headless is properly installed.")

# Create dataset directory if it doesn't exist
if not os.path.exists('dataset'):
    os.makedirs('dataset')

def get_attendance_file():
    """Get today's attendance file path"""
    today = datetime.now().strftime('%Y-%m-%d')
    return f'{today}.csv'

def load_trained_model():
    """Load the trained face recognition model"""
    try:
        # Check if face module is available
        if not hasattr(cv2, 'face'):
            print("Warning: OpenCV face module not available")
            return None
        
        model = cv2.face.LBPHFaceRecognizer_create()
        model.read('trained_model.yml')
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_person_names():
    """Get list of person names from dataset directory"""
    names = []
    if os.path.exists('dataset'):
        for folder in os.listdir('dataset'):
            if os.path.isdir(os.path.join('dataset', folder)):
                names.append(folder)
    return names

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new person for face recognition"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            if not name:
                return jsonify({'success': False, 'message': 'Please provide a name'})
            
            # Create directory for the person
            person_dir = os.path.join('dataset', name)
            if not os.path.exists(person_dir):
                os.makedirs(person_dir)
            
            # Get image data from form
            image_data = request.form.get('image')
            if not image_data:
                return jsonify({'success': False, 'message': 'Please capture an image'})
            
            # Extract base64 data
            image_data = re.sub('^data:image/.+;base64,', '', image_data)
            image_bytes = base64.b64decode(image_data)
            
            # Save image
            image_path = os.path.join(person_dir, f'{len(os.listdir(person_dir)) + 1}.png')
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            
            return jsonify({'success': True, 'message': f'Registered {name} successfully!'})
            
        except Exception as e:
            print(f"Registration error: {str(e)}")
            return jsonify({'success': False, 'message': f'Error registering user: {str(e)}'})
    
    return render_template('register.html')

@app.route('/train')
def train_model():
    """Train the face recognition model"""
    try:
        # Get all images from dataset
        images = []
        labels = []
        names = []
        
        for person_name in os.listdir('dataset'):
            person_dir = os.path.join('dataset', person_name)
            if os.path.isdir(person_dir):
                names.append(person_name)
                for image_file in os.listdir(person_dir):
                    if image_file.endswith('.png'):
                        image_path = os.path.join(person_dir, image_file)
                        img = cv2.imread(image_path, 0)
                        if img is not None:
                            images.append(img)
                            labels.append(len(names) - 1)
        
        if len(images) > 0:
            # Train the model
            model = cv2.face.LBPHFaceRecognizer_create()
            model.train(images, np.array(labels))
            model.save('trained_model.yml')
            
            # Save names mapping
            with open('names.txt', 'w') as f:
                for name in names:
                    f.write(name + '\n')
            
            return jsonify({'success': True, 'message': 'Model trained successfully!'})
        else:
            return jsonify({'success': False, 'message': 'No images found in dataset'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error training model: {str(e)}'})

@app.route('/attendance')
def attendance():
    """Take attendance using face recognition"""
    return render_template('attendance.html')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance for detected face"""
    try:
        # Get image data
        image_data = request.form.get('image')
        if not image_data:
            return jsonify({'success': False, 'message': 'No image captured'})
        
        # Extract base64 data
        image_data = re.sub('^data:image/.+;base64,', '', image_data)
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return jsonify({'success': False, 'message': 'No face detected'})
        
        # Load trained model
        model = load_trained_model()
        if model is None:
            return jsonify({'success': False, 'message': 'Model not trained yet'})
        
        # Load names
        names = []
        if os.path.exists('names.txt'):
            with open('names.txt', 'r') as f:
                names = [line.strip() for line in f.readlines()]
        
        # Recognize face
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            label, confidence = model.predict(face_roi)
            
            if confidence < 100 and label < len(names):
                person_name = names[label]
                
                # Mark attendance
                attendance_file = get_attendance_file()
                current_time = datetime.now().strftime('%H-%M-%S')
                
                # Check if already marked attendance
                already_marked = False
                if os.path.exists(attendance_file):
                    with open(attendance_file, 'r') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if row[0] == person_name:
                                already_marked = True
                                break
                
                if not already_marked:
                    with open(attendance_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([person_name, current_time])
                    
                    return jsonify({
                        'success': True, 
                        'message': f'Attendance marked for {person_name} at {current_time}',
                        'person': person_name,
                        'time': current_time
                    })
                else:
                    return jsonify({'success': False, 'message': f'{person_name} already marked attendance today'})
            else:
                return jsonify({'success': False, 'message': 'Face not recognized. Please register first.'})
                
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/view_attendance')
def view_attendance():
    """View today's attendance"""
    attendance_file = get_attendance_file()
    attendance_data = []
    
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    attendance_data.append({'name': row[0], 'time': row[1]})
    
    return render_template('view_attendance.html', attendance=attendance_data)

@app.route('/api/stats')
def get_stats():
    """Get statistics about registered users and images"""
    try:
        users = 0
        images = 0
        
        if os.path.exists('dataset'):
            for person_name in os.listdir('dataset'):
                person_dir = os.path.join('dataset', person_name)
                if os.path.isdir(person_dir):
                    users += 1
                    for image_file in os.listdir(person_dir):
                        if image_file.endswith('.png'):
                            images += 1
        
        return jsonify({
            'users': users,
            'images': images
        })
    except Exception as e:
        return jsonify({'users': 0, 'images': 0})

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    try:
        # Check if OpenCV is working
        cv2_version = cv2.__version__
        face_available = hasattr(cv2, 'face')
        
        return jsonify({
            'status': 'healthy',
            'opencv_version': cv2_version,
            'face_module_available': face_available,
            'dataset_exists': os.path.exists('dataset'),
            'haar_file_exists': os.path.exists(haar_file)
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
