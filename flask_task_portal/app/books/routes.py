from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from app.db import execute, fetch_all, fetch_one

books_bp = Blueprint("books", __name__, template_folder="templates")


@books_bp.get("/")
def list_books():
    books = fetch_all("SELECT id, title, author, published_year FROM books ORDER BY id DESC")
    return render_template("books/list.html", books=books)


@books_bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        published_year = request.form.get("published_year", "").strip()
        if not title or not author or not published_year.isdigit():
            flash("Enter a title, author, and numeric published year.", "danger")
            return render_template("books/form.html")
        execute("INSERT INTO books (title, author, published_year) VALUES (%s, %s, %s)",
                (title, author, int(published_year)))
        flash("Book added successfully.", "success")
        return redirect(url_for("books.list_books"))
    return render_template("books/form.html")


@books_bp.post("/<int:book_id>/delete")
def delete_book(book_id):
    execute("DELETE FROM books WHERE id = %s", (book_id,))
    flash("Book deleted.", "info")
    return redirect(url_for("books.list_books"))


@books_bp.get("/api")
def api_books():
    return jsonify(fetch_all("SELECT id, title, author, published_year FROM books ORDER BY id"))


@books_bp.post("/api")
def api_add_book():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    author = str(data.get("author", "")).strip()
    year = data.get("published_year")
    if not title or not author or not isinstance(year, int):
        return jsonify(error="title, author, and integer published_year are required"), 400
    book_id = execute("INSERT INTO books (title, author, published_year) VALUES (%s, %s, %s)",
                      (title, author, year))
    return jsonify(id=book_id, title=title, author=author, published_year=year), 201


@books_bp.get("/api/<int:book_id>")
def api_get_book(book_id):
    book = fetch_one("SELECT id, title, author, published_year FROM books WHERE id = %s", (book_id,))
    if not book:
        return jsonify(error="book not found"), 404
    return jsonify(book)


@books_bp.put("/api/<int:book_id>")
def api_update_book(book_id):
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    author = str(data.get("author", "")).strip()
    year = data.get("published_year")
    if not title or not author or not isinstance(year, int):
        return jsonify(error="title, author, and integer published_year are required"), 400
    if not fetch_one("SELECT id FROM books WHERE id = %s", (book_id,)):
        return jsonify(error="book not found"), 404
    execute("UPDATE books SET title = %s, author = %s, published_year = %s WHERE id = %s",
            (title, author, year, book_id))
    return jsonify(id=book_id, title=title, author=author, published_year=year)


@books_bp.delete("/api/<int:book_id>")
def api_delete_book(book_id):
    if not fetch_one("SELECT id FROM books WHERE id = %s", (book_id,)):
        return jsonify(error="book not found"), 404
    execute("DELETE FROM books WHERE id = %s", (book_id,))
    return jsonify(message="book deleted")
