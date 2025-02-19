import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Helper functions 
from helpers import apology, usd, surface

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["surface"] = surface

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database helper
def get_db_connection():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(r"C:\Users\estag\Desktop\final proyect\Local DB\model_quant.db")
    conn.row_factory = sqlite3.Row  # Allow to access as dict
    return conn


# Custom login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Middleware para agregar automáticamente '.js' a las rutas faltantes
@app.before_request
def fix_js_imports():
    # Si ya tiene extensión, no hacemos nada
    if request.path.endswith('.js') or '.' in request.path:
        return

    # Si el archivo está en /static/ y falta la extensión
    if '/static/' in request.path:
        corrected_path = request.path.replace('/static/', '')

        # Verificar si la ruta está dentro de 'node_modules'
        if corrected_path.startswith('node_modules/'):
            # Reemplazar 'node_modules' por la carpeta correcta dentro de 'static'
            return send_from_directory('static', corrected_path)

        # Revisar si es un archivo dentro de 'components' dentro de 'web-ifc-viewer'
        elif corrected_path.startswith('components/'):
            # Enviar el archivo desde la carpeta correcta dentro de 'static'
            return send_from_directory('static/node_modules/web-ifc-viewer/dist', corrected_path)

        # Caso general: Si no es un componente o archivo dentro de node_modules, intenta agregar '.js'
        return send_from_directory('static', corrected_path + '.js')


@app.route("/")
@login_required
def index():
    """Show project"""
    # Check if session has required keys
    
    if "user_id" not in session or "username" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    username = session["username"]

    # Fetch user and project data

    conn = get_db_connection()
    users_data_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    price_rows = conn.execute("SELECT * FROM single_prices").fetchall()
    Prices = {row[0]: row[1] for row in price_rows}
    
    model_data_rows = conn.execute(
        "SELECT * FROM const_elements WHERE Proyect = ?", (username,)
    ).fetchall()

    total_sum = 0.00

    if model_data_rows:
        for row in model_data_rows:
            total_sum = total_sum + row["Quantity"] * Prices[row["Element"]]
        time = model_data_rows[0][4]
    
    

    # Render the appropriate template
    if not model_data_rows:
        return render_template("home_blank.html")
    return render_template("index.html", Project_Data=model_data_rows, Prices=Prices, total_sum=total_sum, time=time)

    conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Clear session
    session.clear()

    # Handle POST request
    if request.method == "POST":
        # Ensure username and password are provided
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 403)
        if not password:
            return apology("must provide password", 403)

        # Query database for username
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        # Check username and password
        if not user or not check_password_hash(user["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember logged-in user
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        # Redirect to homepage
        return redirect("/")

    # Render login page for GET request
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Clear session
    session.clear()

    # Handle POST request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate form inputs
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must confirm password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Check if username is taken
        conn = get_db_connection()
        existing_user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing_user:
            conn.close()
            return apology("username is already taken", 400)

        # Insert new user into database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
        conn.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()

        # Retrieve the new user's ID and log them in
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        # Redirect to homepage
        return redirect("/")

    # Render registration page for GET request
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)

