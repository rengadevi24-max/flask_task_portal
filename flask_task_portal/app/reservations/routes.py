from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from app.db import execute, fetch_all, fetch_one

reservations_bp = Blueprint("reservations", __name__, template_folder="templates")


def choices():
    books = fetch_all("SELECT id, title FROM books ORDER BY title")
    members = fetch_all("SELECT id, name FROM members ORDER BY name")
    return books, members


@reservations_bp.get("/")
def list_reservations():
    reservations = fetch_all(
        """SELECT r.id, r.book_id, r.member_id, r.reservation_date,
                  b.title AS book_title, m.name AS member_name
           FROM reservations r
           JOIN books b ON b.id = r.book_id
           JOIN members m ON m.id = r.member_id
           ORDER BY r.id DESC"""
    )
    return render_template("reservations/list.html", reservations=reservations)


@reservations_bp.route("/add", methods=["GET", "POST"])
def add_reservation():
    books, members = choices()
    if request.method == "POST":
        book_id = request.form.get("book_id", "").strip()
        member_id = request.form.get("member_id", "").strip()
        reservation_date = request.form.get("reservation_date", "").strip()
        if not book_id.isdigit() or not member_id.isdigit() or not reservation_date:
            flash("Choose a book, a member, and a reservation date.", "danger")
            return render_template("reservations/form.html", books=books, members=members)
        execute("INSERT INTO reservations (book_id, member_id, reservation_date) VALUES (%s, %s, %s)",
                (int(book_id), int(member_id), reservation_date))
        flash("Reservation added successfully.", "success")
        return redirect(url_for("reservations.list_reservations"))
    return render_template("reservations/form.html", books=books, members=members)


@reservations_bp.post("/<int:reservation_id>/delete")
def delete_reservation(reservation_id):
    execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    flash("Reservation deleted.", "info")
    return redirect(url_for("reservations.list_reservations"))


@reservations_bp.get("/api")
def api_reservations():
    return jsonify(fetch_all(
        "SELECT id, book_id, member_id, reservation_date FROM reservations ORDER BY id"
    ))


@reservations_bp.post("/api")
def api_add_reservation():
    data = request.get_json(silent=True) or {}
    book_id = data.get("book_id")
    member_id = data.get("member_id")
    reservation_date = str(data.get("reservation_date", "")).strip()
    if not isinstance(book_id, int) or not isinstance(member_id, int) or not reservation_date:
        return jsonify(error="integer book_id, integer member_id, and reservation_date are required"), 400
    if not fetch_one("SELECT id FROM books WHERE id = %s", (book_id,)):
        return jsonify(error="book_id does not exist"), 400
    if not fetch_one("SELECT id FROM members WHERE id = %s", (member_id,)):
        return jsonify(error="member_id does not exist"), 400
    reservation_id = execute(
        "INSERT INTO reservations (book_id, member_id, reservation_date) VALUES (%s, %s, %s)",
        (book_id, member_id, reservation_date),
    )
    return jsonify(id=reservation_id, book_id=book_id, member_id=member_id,
                   reservation_date=reservation_date), 201


@reservations_bp.get("/api/<int:reservation_id>")
def api_get_reservation(reservation_id):
    reservation = fetch_one(
        "SELECT id, book_id, member_id, reservation_date FROM reservations WHERE id = %s",
        (reservation_id,),
    )
    if not reservation:
        return jsonify(error="reservation not found"), 404
    return jsonify(reservation)


@reservations_bp.delete("/api/<int:reservation_id>")
def api_delete_reservation(reservation_id):
    if not fetch_one("SELECT id FROM reservations WHERE id = %s", (reservation_id,)):
        return jsonify(error="reservation not found"), 404
    execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    return jsonify(message="reservation deleted")
