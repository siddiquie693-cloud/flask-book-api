from flask import Flask, request, jsonify
from models import db, bcrypt, User, Book
from auth import token_required, admin_required
import jwt, logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db.init_app(app)
bcrypt.init_app(app)

logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")

with app.app_context():
    db.create_all()

#---------------AUTH-----------
@app.route("/register", methods=['POST'])
def register():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username & password required"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password=hashed_pw, role=data.get("role", "user"))
    db.session.add(user)
    db.session.commit()
    logging.info(f"User register: {user.username}")
    return jsonify({"message": "User registered"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not bcrypt.check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    logging.info(f"User login: {user.username}")
    return jsonify({"token": token})

#--------------BOOKS------------- 
@app.route("/books", methods=["GET"])
@token_required(app, db)
def get_books(current_user):
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    query = Book.query
    if search:
        query = query.filter(Book.title.contains(search))
    books = query.paginate(page=page, per_page=limit, error_out=False)
    return jsonify([b.to_dict() for b in books.items])

@app.route("/books", methods=["POST"])
@token_required(app, db)
@admin_required
def add_book(current_user):
    data = request.json
    if not data.get("title") or not data.get("author"):
        return jsonify({"error": "Title & author required"}), 400

    book = Book(title=data["title"], author=data["author"])
    db.session.add(book)
    db.session.commit()
    logging.info(f"Book added: {book.title}")
    return jsonify(book.to_dict()), 201

@app.route("/books/<int:id>", methods=["PUT"])
@token_required(app, db)
@admin_required
def update_book(current_user, id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.json
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    db.session.commit()
    logging.info(f"Book updated: {book.title}")
    return jsonify(book.to_dict())

@app.route("/books/<int:id>", methods=["DELETE"])
@token_required(app, db)
@admin_required
def delete_book(current_user, id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    logging.info(f"Book deleted: {book.title}")
    return jsonify({"message": "Book deleted"})

#-------------RUN------------ 
if __name__ == "__main__":
    app.run(debug=True)    
        