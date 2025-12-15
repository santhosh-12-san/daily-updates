from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import mysql.connector
import jwt
import datetime
from functools import wraps
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# --- Database Connection Helper ---
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# --- Authentication Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except:
            return redirect(url_for('login'))
        return f(current_user_id, *args, **kwargs)
    return decorated

# --- Routes ---

@app.route('/')
def index():
    # Get parameters from URL
    category = request.args.get('category')
    search_query = request.args.get('q') 
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Filter Logic
    if search_query:
        query_text = f"%{search_query}%"
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", (query_text,))
    elif category and category != 'Top Deals':
        cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
    else:
        cursor.execute("SELECT * FROM products")
        
    products = cursor.fetchall()
    conn.close()
    
    is_logged_in = 'token' in request.cookies
    return render_template('index.html', products=products, is_logged_in=is_logged_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password, phone, address) VALUES (%s, %s, %s, %s, %s)", 
                           (name, email, password, phone, address))
            conn.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Error: {e}"
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            token = jwt.encode({
                'user_id': user['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('token', token)
            return resp
        else:
            return render_template('login.html', error="Invalid Credentials")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', '', expires=0)
    return resp

@app.route('/search_suggestions')
def search_suggestions():
    query = request.args.get('q')
    if not query:
        return jsonify([])
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM products WHERE name LIKE %s LIMIT 5", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return jsonify([row['name'] for row in results])

# --- IMPROVED ADD TO CART (Prevents Duplicates) ---
@app.route('/add_to_cart/<int:product_id>')
@token_required
def add_to_cart(current_user_id, product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if item is already in cart
    cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (current_user_id, product_id))
    existing_item = cursor.fetchone()
    
    if existing_item:
        # If exists, just increase quantity
        new_qty = existing_item['quantity'] + 1
        cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s", 
                       (new_qty, current_user_id, product_id))
    else:
        # If not, add new row
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)", 
                       (current_user_id, product_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/cart')
@token_required
def cart(current_user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # IMPORTANT: We explicitly select p.id as product_id for the update buttons
    query = """
        SELECT p.id as product_id, p.name, p.price, p.image_url, c.quantity 
        FROM cart c
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = %s
    """
    
    cursor.execute(query, (current_user_id,))
    items = cursor.fetchall()
    
    # Calculate Total
    total = sum(item['price'] * item['quantity'] for item in items)
    
    conn.close()
    return render_template('cart.html', items=items, total=total)

# --- IMPROVED UPDATE CART (Increase/Decrease/Remove) ---
@app.route('/update_cart/<int:product_id>/<string:action>')
@token_required
def update_cart(current_user_id, product_id, action):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s", (current_user_id, product_id))
    item = cursor.fetchone()
    
    if item:
        current_qty = item['quantity']
        
        if action == 'increase':
            cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s", 
                           (current_qty + 1, current_user_id, product_id))
            
        elif action == 'decrease':
            if current_qty > 1:
                cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s", 
                               (current_qty - 1, current_user_id, product_id))
            else:
                cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", 
                               (current_user_id, product_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/profile')
@token_required
def profile(current_user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (current_user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('profile.html', user=user, is_logged_in=True)

if __name__ == '__main__':
    app.run(debug=True)