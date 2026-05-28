"""
Flask Backend for Car Sales Price Prediction System
Handles: Authentication, Predictions, Database Operations, Admin Panel
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import joblib
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this_in_production'

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ben10',
    'database': 'car_sales_db'
}

# Load ML Model and Label Encoders
print("Loading ML model and label encoders...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'label_encoders.pkl')
try:
    model = joblib.load(MODEL_PATH)
    label_encoders = joblib.load(ENCODERS_PATH)
    print("✓ Model loaded successfully from:", MODEL_PATH)
except FileNotFoundError:
    print(f"⚠ Model files not found at {MODEL_PATH}. Please run train_model.py first")
    model = None
    label_encoders = None

# Database Connection Function
def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# ===================== AUTHENTICATION ROUTES =====================

@app.route('/', methods=['GET'])
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not all([username, email, password, confirm_password]):
            return render_template('register.html', error='All fields are required')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        connection = get_db_connection()
        if not connection:
            return render_template('register.html', error='Database connection failed')

        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password))
            connection.commit()
            
            return redirect(url_for('login'))
        except Error as e:
            return render_template('register.html', error=f'Registration failed: {str(e)[:50]}')
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error='Username and password are required')

        connection = get_db_connection()
        if not connection:
            return render_template('login.html', error='Database connection failed')

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id, username, password, is_admin FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = user['is_admin']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password')
        except Error as e:
            return render_template('login.html', error=f'Login failed: {str(e)[:50]}')
        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

# ===================== MAIN APPLICATION ROUTES =====================

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    if not connection:
        return render_template('dashboard.html', error='Database connection failed')

    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get user prediction count
        query = "SELECT COUNT(*) as count FROM predictions WHERE user_id = %s"
        cursor.execute(query, (session['user_id'],))
        prediction_count = cursor.fetchone()['count']

        # Get recent predictions
        query = """
            SELECT * FROM predictions 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 5
        """
        cursor.execute(query, (session['user_id'],))
        recent_predictions = cursor.fetchall()

        return render_template('dashboard.html', 
                             username=session['username'],
                             prediction_count=prediction_count,
                             recent_predictions=recent_predictions)
    except Error as e:
        return render_template('dashboard.html', error=f'Error: {str(e)[:50]}')
    finally:
        cursor.close()
        connection.close()

# ===================== PREDICTION ROUTES =====================

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Car price prediction page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Ensure model and encoders are loaded before attempting prediction
    if model is None or label_encoders is None:
        return render_template('predict.html', error='Model not loaded. Please run train_model.py to train the model')

    if request.method == 'POST':
        try:
            # Get form data
            car_name = request.form.get('car_name')
            year = int(request.form.get('year'))
            present_price = float(request.form.get('present_price'))
            kms_driven = int(request.form.get('kms_driven'))
            fuel_type = request.form.get('fuel_type')
            seller_type = request.form.get('seller_type')
            transmission = request.form.get('transmission')
            owner = int(request.form.get('owner'))

            # Validate inputs
            if not all([car_name, year, present_price, kms_driven, fuel_type, seller_type, transmission, owner]):
                return render_template('predict.html', error='All fields are required')

            # Prepare features for prediction
            features = np.array([[
                label_encoders['Car_Name'].transform([car_name])[0],
                year,
                present_price,
                kms_driven,
                label_encoders['Fuel_Type'].transform([fuel_type])[0],
                label_encoders['Seller_Type'].transform([seller_type])[0],
                label_encoders['Transmission'].transform([transmission])[0],
                owner
            ]])

            # Make prediction
            predicted_price = float(model.predict(features)[0])

            # Save prediction to database
            connection = get_db_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    query = """
                        INSERT INTO predictions 
                        (user_id, car_name, year, present_price, kms_driven, 
                         fuel_type, seller_type, transmission, owner, predicted_price)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        session['user_id'], car_name, year, present_price, kms_driven,
                        fuel_type, seller_type, transmission, owner, predicted_price
                    ))
                    connection.commit()
                except Error as e:
                    print(f"Database error: {e}")
                finally:
                    cursor.close()
                    connection.close()

            return render_template('predict.html', 
                                 prediction_result={
                                     'car_name': car_name,
                                     'present_price': present_price,
                                     'predicted_price': round(predicted_price, 2),
                                     'difference': round(predicted_price - present_price, 2)
                                 })

        except (ValueError, IndexError) as e:
            return render_template('predict.html', error=f'Invalid input: {str(e)[:50]}')

    return render_template('predict.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions (AJAX)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Ensure model and encoders are loaded for API predictions
    if model is None or label_encoders is None:
        return jsonify({'error': 'Model not loaded. Please run train_model.py to train the model'}), 500

    try:
        data = request.get_json()
        
        features = np.array([[
            label_encoders['Car_Name'].transform([data['car_name']])[0],
            int(data['year']),
            float(data['present_price']),
            int(data['kms_driven']),
            label_encoders['Fuel_Type'].transform([data['fuel_type']])[0],
            label_encoders['Seller_Type'].transform([data['seller_type']])[0],
            label_encoders['Transmission'].transform([data['transmission']])[0],
            int(data['owner'])
        ]])

        predicted_price = float(model.predict(features)[0])
        return jsonify({'predicted_price': round(predicted_price, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===================== HISTORY ROUTES =====================

@app.route('/history')
def history():
    """View prediction history"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    if not connection:
        return render_template('history.html', error='Database connection failed')

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM predictions 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """
        cursor.execute(query, (session['user_id'],))
        predictions = cursor.fetchall()

        return render_template('history.html', predictions=predictions)
    except Error as e:
        return render_template('history.html', error=f'Error: {str(e)[:50]}')
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_prediction/<int:prediction_id>', methods=['POST'])
def delete_prediction(prediction_id):
    """Delete a prediction"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        # Verify ownership
        query = "SELECT user_id FROM predictions WHERE id = %s"
        cursor.execute(query, (prediction_id,))
        result = cursor.fetchone()

        if not result or result[0] != session['user_id']:
            return jsonify({'error': 'Unauthorized'}), 403

        # Delete prediction
        query = "DELETE FROM predictions WHERE id = %s"
        cursor.execute(query, (prediction_id,))
        connection.commit()

        return jsonify({'success': True})
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# ===================== ADMIN ROUTES =====================

@app.route('/admin')
def admin():
    """Admin panel"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    connection = get_db_connection()
    if not connection:
        return render_template('admin.html', error='Database connection failed')

    try:
        cursor = connection.cursor(dictionary=True)

        # Get all users
        cursor.execute("SELECT id, username, email, created_at FROM users WHERE is_admin = FALSE")
        users = cursor.fetchall()

        # Get all predictions
        cursor.execute("""
            SELECT p.*, u.username FROM predictions p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        """)
        predictions = cursor.fetchall()

        # Get statistics
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = FALSE")
        user_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM predictions")
        prediction_count = cursor.fetchone()['count']

        cursor.execute("SELECT AVG(predicted_price) as avg_price FROM predictions")
        avg_price = cursor.fetchone()['avg_price']

        return render_template('admin.html',
                             users=users,
                             predictions=predictions,
                             user_count=user_count,
                             prediction_count=prediction_count,
                             avg_price=avg_price or 0)
    except Error as e:
        return render_template('admin.html', error=f'Error: {str(e)[:50]}')
    finally:
        cursor.close()
        connection.close()

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user (admin only)"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s AND is_admin = FALSE"
        cursor.execute(query, (user_id,))
        connection.commit()

        return jsonify({'success': True})
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/admin/delete_prediction/<int:prediction_id>', methods=['POST'])
def admin_delete_prediction(prediction_id):
    """Delete a prediction (admin only)"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM predictions WHERE id = %s"
        cursor.execute(query, (prediction_id,))
        connection.commit()

        return jsonify({'success': True})
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# ===================== ERROR HANDLERS =====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', message='Page not found'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('error.html', message='Server error'), 500

# ===================== RUN APPLICATION =====================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚗 Car Sales Price Prediction System")
    print("="*50)
    print(f"Starting Flask app on http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
