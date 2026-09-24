from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from app.db import execute, fetch_all, fetch_one

members_bp = Blueprint("members", __name__, template_folder="templates")


@members_bp.get("/")
def list_members():
    members = fetch_all("SELECT id, name, email, phone FROM members ORDER BY id DESC")
    return render_template("members/list.html", members=members)


@members_bp.route("/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        if not name or not email or not phone:
            flash("Name, email, and phone are required.", "danger")
            return render_template("members/form.html")
        execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)",
                (name, email, phone))
        flash("Member added successfully.", "success")
        return redirect(url_for("members.list_members"))
    return render_template("members/form.html")


@members_bp.post("/<int:member_id>/delete")
def delete_member(member_id):
    execute("DELETE FROM members WHERE id = %s", (member_id,))
    flash("Member deleted.", "info")
    return redirect(url_for("members.list_members"))


@members_bp.get("/api")
def api_members():
    return jsonify(fetch_all("SELECT id, name, email, phone FROM members ORDER BY id"))


@members_bp.post("/api")
def api_add_member():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    if not name or not email or not phone:
        return jsonify(error="name, email, and phone are required"), 400
    member_id = execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)",
                        (name, email, phone))
    return jsonify(id=member_id, name=name, email=email, phone=phone), 201


@members_bp.get("/api/<int:member_id>")
def api_get_member(member_id):
    member = fetch_one("SELECT id, name, email, phone FROM members WHERE id = %s", (member_id,))
    if not member:
        return jsonify(error="member not found"), 404
    return jsonify(member)


@members_bp.put("/api/<int:member_id>")
def api_update_member(member_id):
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    if not name or not email or not phone:
        return jsonify(error="name, email, and phone are required"), 400
    if not fetch_one("SELECT id FROM members WHERE id = %s", (member_id,)):
        return jsonify(error="member not found"), 404
    execute("UPDATE members SET name = %s, email = %s, phone = %s WHERE id = %s",
            (name, email, phone, member_id))
    return jsonify(id=member_id, name=name, email=email, phone=phone)


@members_bp.delete("/api/<int:member_id>")
def api_delete_member(member_id):
    if not fetch_one("SELECT id FROM members WHERE id = %s", (member_id,)):
        return jsonify(error="member not found"), 404
    execute("DELETE FROM members WHERE id = %s", (member_id,))
    return jsonify(message="member deleted")
