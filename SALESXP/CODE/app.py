from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import CORS
import MySQLdb
from MySQLdb import IntegrityError
import logging
from datetime import datetime  # Ensure datetime is imported
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_'  # Replace with a secure key
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'ganesh@sql',  # Replace with your MySQL password
    'db': 'saree_management'
}

# Encryption key (generate once and store securely; here it's hardcoded for simplicity)
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

def get_db_connection():
    try:
        conn = MySQLdb.connect(**db_config)
        logger.info("Database connection established successfully")
        return conn
    except MySQLdb.Error as e:
        logger.error(f"Database connection failed: {str(e)}")
        return None

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info("Serving index page")
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'signin':
            emp_id = request.form.get('emp_id')
            password = request.form.get('password')
            role = request.form.get('role')

            if not emp_id or not password or not role:
                return render_template('index.html', error="Missing sign-in details")

            if role != 'salesperson':
                return render_template('index.html', error="Only Salesperson role requires sign-in")

            conn = get_db_connection()
            if not conn:
                return render_template('index.html', error="Database connection failed")
            try:
                with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT emp_id, password, role FROM users WHERE emp_id = %s", (emp_id,))
                    user = cursor.fetchone()
                    if user and check_password_hash(user['password'], password) and user['role'] == 'salesperson':
                        session['emp_id'] = user['emp_id']
                        session['role'] = user['role']
                        logger.info(f"Sign-in successful for {emp_id} as salesperson")
                        return redirect(url_for('salesperson'))
                    else:
                        logger.warning(f"Invalid sign-in attempt for {emp_id}")
                        return render_template('index.html', error="Invalid Employee ID or Password")
            except MySQLdb.Error as e:
                logger.error(f"Database error during sign-in: {str(e)}")
                return render_template('index.html', error=f"Database error: {str(e)}")
            finally:
                conn.close()

        elif action == 'signup':
            emp_id = request.form.get('emp_id')
            name = request.form.get('name')
            email = request.form.get('email')
            role = request.form.get('role')
            password = request.form.get('password')

            if not all([emp_id, name, email, role, password]):
                return render_template('index.html', error="Missing sign-up details")
            if role != 'salesperson':
                return render_template('index.html', error="Only Salesperson role can sign up")

            conn = get_db_connection()
            if not conn:
                return render_template('index.html', error="Database connection failed")
            try:
                with conn.cursor() as cursor:
                    hashed_password = generate_password_hash(password)
                    cursor.execute('''
                        INSERT INTO users (emp_id, name, email, role, password)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (emp_id, name, email, role, hashed_password))
                    conn.commit()
                    logger.info(f"Salesperson {emp_id} signed up successfully")
                    return render_template('index.html', message="Sign-up successful! Please sign in.")
            except IntegrityError:
                conn.rollback()
                logger.warning(f"Duplicate emp_id or email for {emp_id}")
                return render_template('index.html', error="Employee ID or Email already exists")
            except MySQLdb.Error as e:
                conn.rollback()
                logger.error(f"Database error during sign-up: {str(e)}")
                return render_template('index.html', error=f"Database error: {str(e)}")
            finally:
                conn.close()

    return render_template('index.html')

@app.route('/stock_management')
def stock_management():
    logger.info("Serving stock_management page")
    return render_template('stock_management.html')

@app.route('/billing_desk')
def billing_desk():
    logger.info("Serving billing_desk page")
    return render_template('billing_desk.html')

@app.route('/salesperson')
def salesperson():
    if 'emp_id' not in session or session.get('role') != 'salesperson':
        return redirect(url_for('index'))
    logger.info("Serving salesperson page")
    return render_template('salesperson.html', emp_id=session['emp_id'])

@app.route('/logout')
def logout():
    session.clear()
    logger.info("User logged out")
    return redirect(url_for('index'))

# API Routes
@app.route('/sarees', methods=['GET'])
def get_sarees():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM sarees')
            sarees = cursor.fetchall()
            logger.info(f"Retrieved {len(sarees)} sarees from database")
            return jsonify(sarees)
    except MySQLdb.Error as e:
        logger.error(f"Error fetching sarees: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/sarees', methods=['POST'])
def add_saree():
    data = request.get_json()
    required_fields = ['name', 'fabric', 'color', 'price', 'stock_quantity', 'barcode']
    if not all(field in data for field in required_fields):
        logger.warning("Missing required fields in POST /sarees request")
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['stock_quantity'] < 0:
        logger.warning("Invalid stock quantity: negative value provided")
        return jsonify({'error': 'Stock quantity cannot be negative'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO sarees (name, fabric, color, price, stock_quantity, barcode)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (data['name'], data['fabric'], data['color'], float(data['price']), 
                  int(data['stock_quantity']), data['barcode']))
            conn.commit()
            new_id = cursor.lastrowid
            logger.info(f"Saree added with ID: {new_id}")
            return jsonify({'message': 'Saree added', 'saree_id': new_id}), 201
    except IntegrityError:
        conn.rollback()
        logger.warning("Barcode already exists")
        return jsonify({'error': 'Barcode already exists'}), 409
    except MySQLdb.Error as e:
        conn.rollback()
        logger.error(f"Database error while adding saree: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/sarees/<int:saree_id>', methods=['PUT'])
def update_saree(saree_id):
    data = request.get_json()
    required_fields = ['name', 'fabric', 'color', 'price', 'stock_quantity', 'barcode']
    if not all(field in data for field in required_fields):
        logger.warning(f"Missing required fields in PUT /sarees/{saree_id} request")
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['stock_quantity'] < 0:
        logger.warning("Invalid stock quantity: negative value provided")
        return jsonify({'error': 'Stock quantity cannot be negative'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE sarees 
                SET name=%s, fabric=%s, color=%s, price=%s, stock_quantity=%s, barcode=%s
                WHERE saree_id=%s
            ''', (data['name'], data['fabric'], data['color'], float(data['price']), 
                  int(data['stock_quantity']), data['barcode'], saree_id))
            if cursor.rowcount == 0:
                logger.warning(f"Saree with ID {saree_id} not found")
                return jsonify({'error': 'Saree not found'}), 404
            conn.commit()
            logger.info(f"Saree with ID {saree_id} updated")
            return jsonify({'message': 'Saree updated'}), 200
    except IntegrityError:
        conn.rollback()
        logger.warning("Barcode already exists")
        return jsonify({'error': 'Barcode already exists'}), 409
    except MySQLdb.Error as e:
        conn.rollback()
        logger.error(f"Database error while updating saree: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/sarees/<int:saree_id>', methods=['DELETE'])
def delete_saree(saree_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM sarees WHERE saree_id=%s', (saree_id,))
            if cursor.rowcount == 0:
                logger.warning(f"Saree with ID {saree_id} not found")
                return jsonify({'error': 'Saree not found'}), 404
            conn.commit()
            logger.info(f"Saree with ID {saree_id} deleted")
            return jsonify({'message': 'Saree deleted'}), 200
    except MySQLdb.Error as e:
        conn.rollback()
        logger.error(f"Database error while deleting saree: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/sarees/<int:saree_id>/stock', methods=['PUT'])
def update_stock(saree_id):
    data = request.get_json()
    if 'stock_quantity' not in data:
        logger.warning(f"Missing stock_quantity in PUT /sarees/{saree_id}/stock request")
        return jsonify({'error': 'Missing stock_quantity'}), 400
    
    stock_quantity = int(data['stock_quantity'])
    if stock_quantity < 0:
        logger.warning(f"Invalid stock quantity {stock_quantity} for saree_id {saree_id}")
        return jsonify({'error': 'Stock quantity cannot be negative'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT stock_quantity FROM sarees WHERE saree_id=%s', (saree_id,))
            result = cursor.fetchone()
            if not result:
                logger.warning(f"Saree with ID {saree_id} not found")
                return jsonify({'error': 'Saree not found'}), 404
            
            cursor.execute('UPDATE sarees SET stock_quantity=%s WHERE saree_id=%s', 
                           (stock_quantity, saree_id))
            conn.commit()
            logger.info(f"Stock updated for saree_id {saree_id} to {stock_quantity}")
            return jsonify({'message': 'Stock updated'}), 200
    except MySQLdb.Error as e:
        conn.rollback()
        logger.error(f"Database error while updating stock: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    required_fields = ['customer_name', 'customer_number', 'salesperson_id', 'payment_method', 'items', 'total']
    if not all(field in data for field in required_fields):
        logger.warning("Missing required fields in POST /transactions request")
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor() as cursor:
            # Get current UTC timestamp
            current_time = datetime.utcnow()

            # Insert into transactions table
            cursor.execute('''
                INSERT INTO transactions (customer_name, customer_number, salesperson_id, payment_method, total, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (data['customer_name'], data['customer_number'], data['salesperson_id'], 
                  data['payment_method'], float(data['total']), current_time))
            transaction_id = cursor.lastrowid

            for item in data['items']:
                cursor.execute('''
                    INSERT INTO transaction_items (transaction_id, saree_id, quantity, price, discount, amount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (transaction_id, int(item['saree_id']), int(item['quantity']), float(item['price']), 
                      float(item['discount']), float(item['amount'])))

            # Insert into encrypted tables with encrypted total
            encrypted_total = cipher.encrypt(str(data['total']).encode())
            cursor.execute('''
                INSERT INTO transactions_encrypted (customer_name, customer_number, salesperson_id, payment_method, total_encrypted, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (data['customer_name'], data['customer_number'], data['salesperson_id'], 
                  data['payment_method'], encrypted_total, current_time))
            encrypted_transaction_id = cursor.lastrowid

            for item in data['items']:
                encrypted_amount = cipher.encrypt(str(item['amount']).encode())
                cursor.execute('''
                    INSERT INTO transaction_items_encrypted (transaction_id, saree_id, quantity, price, discount, amount_encrypted)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (encrypted_transaction_id, int(item['saree_id']), int(item['quantity']), float(item['price']), 
                      float(item['discount']), encrypted_amount))

            conn.commit()
            logger.info(f"Transaction added with ID: {transaction_id}, Encrypted ID: {encrypted_transaction_id}")
            return jsonify({'message': 'Transaction recorded', 'transaction_id': transaction_id}), 201
    except MySQLdb.Error as e:
        conn.rollback()
        logger.error(f"Database error while adding transaction: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/salesperson/<emp_id>/sales', methods=['GET'])
def get_salesperson_sales(emp_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT t.transaction_id, t.transaction_date, t.total, ti.saree_id, ti.quantity, ti.amount, s.name as product_name
                FROM transactions t
                JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
                JOIN sarees s ON ti.saree_id = s.saree_id
                WHERE t.salesperson_id = %s
            ''', (emp_id,))
            sales = cursor.fetchall()
            logger.info(f"Retrieved {len(sales)} sales for salesperson {emp_id}")
            return jsonify(sales)
    except MySQLdb.Error as e:
        logger.error(f"Error fetching sales for salesperson {emp_id}: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT u.emp_id, u.name, SUM(t.total) as total_sales
                FROM users u
                LEFT JOIN transactions t ON u.emp_id = t.salesperson_id
                WHERE u.role = 'salesperson'
                GROUP BY u.emp_id, u.name
            ''')
            leaderboard = cursor.fetchall()
            logger.info(f"Retrieved leaderboard with {len(leaderboard)} entries")
            return jsonify(leaderboard)
    except MySQLdb.Error as e:
        logger.error(f"Error fetching leaderboard: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000)