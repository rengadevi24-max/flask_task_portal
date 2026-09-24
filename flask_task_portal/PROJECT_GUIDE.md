# Flask and MySQL from Scratch: Simple Library Project

**Project:** Simple Library Management System  
**Level:** Beginner  
**Modules:** Books, Members, Reservations  
**Database:** MySQL  
**Frontend:** Flask and Jinja templates  
**API testing:** Postman

This guide is written so that a beginner can create and run the project by following the steps in order. The complete working files are included in the project folder and ZIP attachment. The code intentionally uses direct SQL with `mysql-connector-python` instead of an ORM so that the connection between Python, SQL, and Flask is easy to see.

## 1. What you will build

A small library needs three simple areas:

| Module | Exactly three main fields | Purpose |
|---|---|---|
| **Books** | `title`, `author`, `published_year` | Store books in the library |
| **Members** | `name`, `email`, `phone` | Store people who borrow books |
| **Reservations** | `book_id`, `member_id`, `reservation_date` | Connect a member to a book on a date |

The database also creates an automatic `id` column for each table. The `id` is a technical primary key and is not counted as one of the three learner-facing fields.

The browser pages use Flask routes and Jinja templates. The API routes return JSON and can be tested in Postman. Flask maps URLs to Python functions, renders templates, and serves static files such as CSS [1].

> **Simple request flow:** Browser or Postman → Flask route → Python validation → MySQL query → HTML or JSON response.

## 2. Project structure

The project uses three Flask **blueprints**. A blueprint is a small module that groups related routes. This keeps Books, Members, and Reservations separate without making the application complicated.

```text
flask_task_portal/
├── run.py                         # Starts the Flask application
├── config.py                      # MySQL and Flask settings
├── schema.sql                     # Creates the MySQL database and tables
├── requirements.txt               # Python packages
├── postman_collection.json        # Ready-made Postman requests
├── app/
│   ├── __init__.py                # Application factory and blueprint registration
│   ├── db.py                      # Reusable MySQL functions
│   ├── static/
│   │   └── style.css              # CSS file
│   ├── templates/
│   │   ├── base.html               # Shared Jinja layout
│   │   ├── home.html               # Home page
│   │   └── error.html              # Error page
│   ├── books/
│   │   ├── __init__.py
│   │   └── routes.py               # Books HTML and API routes
│   ├── members/
│   │   ├── __init__.py
│   │   └── routes.py               # Members HTML and API routes
│   └── reservations/
│       ├── __init__.py
│       ├── routes.py               # Reservations HTML and API routes
│       └── templates/reservations/
│           ├── list.html
│           └── form.html
└── uploads/                        # Not needed in this simpler project
```

The module templates are included in the project package. The important beginner idea is that every module contains its own route file, while `base.html` is shared.

## 3. Install the required software

You need **Python**, **MySQL Server**, **PyCharm Community or Professional**, and **Postman**. You can use either Conda or Python’s built-in virtual environment. Conda is used below because it matches the supplied reference guide.

### 3.1 Install Anaconda or Miniconda

Install [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/). After installation, open **Anaconda Prompt** on Windows or a terminal on macOS/Linux.

Check the installation:

```bash
conda --version
python --version
```

### 3.2 Create a clean Conda environment

```bash
conda create -n simplelibrary python=3.11 -y
conda activate simplelibrary
```

Keep this terminal open and keep the environment activated whenever you install packages or run the project.

### 3.3 Install MySQL Server

Download MySQL Community Server from the [official MySQL downloads page](https://dev.mysql.com/downloads/mysql/). During installation, remember the root password. Keep the default MySQL port `3306` unless you have a reason to change it.

Check that the MySQL command works:

```bash
mysql --version
```

If Windows says that `mysql` is not recognized, use **MySQL 8.0 Command Line Client** from the Start menu, or add the MySQL `bin` directory to PATH. The usual directory is similar to `C:\Program Files\MySQL\MySQL Server 8.0\bin`.

### 3.4 Install Python packages

After placing this project on your computer, open its terminal and run:

```bash
conda activate simplelibrary
pip install -r requirements.txt
```

The project uses Flask and MySQL Connector/Python. Connector/Python is the official Python driver used to communicate with MySQL [2].

## 4. Open the project in PyCharm

Open PyCharm and choose **File → Open**. Select the `flask_task_portal` folder.

Choose **File → Settings → Project → Python Interpreter** on Windows/Linux, or **PyCharm → Settings → Project → Python Interpreter** on macOS. Select the Conda environment named `simplelibrary`.

If PyCharm cannot find it, choose **Add Interpreter → Add Local Interpreter → Conda Environment → Existing environment**, then select the Python executable inside the environment. You can confirm the interpreter by opening the PyCharm terminal and running:

```bash
python --version
pip show Flask
```

Flask is intentionally lightweight and does not automatically generate a project folder. You create the folders and files yourself. That is useful for learning because you can see what every file does.

## 5. Create the MySQL database from zero

This is the complete database process. Do not skip it.

### 5.1 Open the MySQL client

Use one of these commands:

```bash
mysql -u root -p
```

Enter the root password that you selected while installing MySQL. On Windows, you can also open **MySQL 8.0 Command Line Client** and enter the same password.

### 5.2 Run the database script

The easiest method is to leave the MySQL prompt and run this from the project folder:

```bash
mysql -u root -p < schema.sql
```

Alternatively, open the file `schema.sql`, copy its contents, paste them into the MySQL prompt, and press Enter. The script does four jobs:

1. It creates the `library_db` database.
2. It creates the `flask_user` application user.
3. It grants that user access to `library_db`.
4. It creates the `books`, `members`, and `reservations` tables and inserts one sample book and member.

The database script uses a foreign key from `reservations.book_id` to `books.id` and another from `reservations.member_id` to `members.id`. A reservation cannot refer to a book or member that does not exist.

### 5.3 Check the database manually

```bash
mysql -u root -p
```

Then run:

```sql
SHOW DATABASES;
USE library_db;
SHOW TABLES;
DESCRIBE books;
DESCRIBE members;
DESCRIBE reservations;
SELECT * FROM books;
SELECT * FROM members;
SELECT * FROM reservations;
EXIT;
```

You should see three tables: `books`, `members`, and `reservations`.

### 5.4 Understand the SQL tables

```sql
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    published_year INT NOT NULL
);
```

`id` uniquely identifies a row. `VARCHAR` stores text. `INT` stores whole numbers. `NOT NULL` means a value is required. `AUTO_INCREMENT` generates the next ID automatically.

The application sends Python values through `%s` placeholders. For example:

```python
execute(
    "INSERT INTO books (title, author, published_year) VALUES (%s, %s, %s)",
    (title, author, published_year),
)
```

Do not build SQL by joining user input into a string. Parameterized queries keep SQL instructions separate from data.

## 6. Configure the application

The default values in `config.py` match the values in `schema.sql`, so the application works immediately after the database script succeeds:

```python
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "flask_user"
MYSQL_PASSWORD = "flask_password"
MYSQL_DATABASE = "library_db"
```

For a real application, use environment variables instead of committing passwords to source code. On macOS/Linux:

```bash
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USER=flask_user
export MYSQL_PASSWORD=flask_password
export MYSQL_DATABASE=library_db
```

On Windows PowerShell:

```powershell
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "flask_user"
$env:MYSQL_PASSWORD = "flask_password"
$env:MYSQL_DATABASE = "library_db"
```

## 7. Understand the Flask files

### `run.py`

```python
from app import create_app
app = create_app()
```

This imports the application factory and creates the Flask object. Run this file when you want to start the website.

### `config.py`

This file stores configuration in one place. `current_app.config` makes these settings available to database functions while a request is running.

### `app/__init__.py`

The `create_app()` function creates the Flask object and registers the three blueprints:

```python
app.register_blueprint(books_bp, url_prefix="/books")
app.register_blueprint(members_bp, url_prefix="/members")
app.register_blueprint(reservations_bp, url_prefix="/reservations")
```

This means a route `/` inside the Books blueprint becomes `/books/` in the browser.

### `app/db.py`

This file has three beginner-friendly functions:

| Function | Purpose |
|---|---|
| `get_connection()` | Connect to MySQL |
| `fetch_all()` | Run `SELECT` and return many dictionary rows |
| `fetch_one()` | Run `SELECT` and return one row |
| `execute()` | Run `INSERT`, `UPDATE`, or `DELETE` and commit |

The connection and cursor are closed in `finally` blocks so the application does not leave database resources open.

## 8. Jinja templates from the beginning

Jinja is Flask’s template language. It lets Python send data to HTML. The three most important Jinja forms are:

| Jinja syntax | Meaning | Example |
|---|---|---|
| `{{ ... }}` | Display a value | `{{ book.title }}` |
| `{% ... %}` | Run a control statement | `{% for book in books %}` |
| `{# ... #}` | Add a template comment | `{# This is not displayed #}` |

### 8.1 Template inheritance

`base.html` contains the common HTML structure, navigation, CSS link, and flash-message area. A child template reuses it:

```jinja2
{% extends "base.html" %}
{% block title %}Books{% endblock %}
{% block content %}
<h1>Books</h1>
{% endblock %}
```

This prevents repeating the same `<html>`, `<nav>`, and flash-message code on every page.

### 8.2 Display a variable

The Books route sends a list named `books`:

```python
return render_template("books/list.html", books=books)
```

The template displays a field:

```jinja2
{{ book.title }}
{{ book.author }}
{{ book.published_year }}
```

### 8.3 Loop through records

```jinja2
{% for book in books %}
    <p>{{ book.title }} by {{ book.author }}</p>
{% endfor %}
```

### 8.4 Use a condition

```jinja2
{% if books %}
    <p>Books were found.</p>
{% else %}
    <p>No books yet.</p>
{% endif %}
```

### 8.5 Build URLs with `url_for()`

```jinja2
<a href="{{ url_for('books.add_book') }}">Add book</a>
```

The endpoint is the blueprint name plus the route function name. Using `url_for()` is safer than hard-coding every path because Flask builds the URL from the registered route [1].

### 8.6 Use a variable URL value

```jinja2
<form action="{{ url_for('books.delete_book', book_id=book.id) }}" method="post">
```

The value of `book.id` is inserted into the URL rule `<int:book_id>`.

### 8.7 Flash messages

Python creates a message:

```python
flash("Book added successfully.", "success")
```

`base.html` displays all messages:

```jinja2
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="flash {{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

### 8.8 Jinja safety

Jinja escapes ordinary displayed text by default, which helps prevent user text from being interpreted as HTML [1]. Do not use `|safe` on user input unless you have deliberately cleaned it.

## 9. Run the website

From the project folder:

```bash
conda activate simplelibrary
flask --app run.py run --debug
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). You should see the home page. Visit the three module pages:

```text
/books/
/members/
/reservations/
```

Follow this order in the browser:

1. Open **Books → Add book** and create a book.
2. Open **Members → Add member** and create a member.
3. Open **Reservations → Add reservation**, choose the book and member, and select a date.
4. Delete a record and observe the flash message.
5. Refresh the page and observe that the data remains because it is stored in MySQL.

## 10. How one module works

The Books module demonstrates the complete pattern.

### Route reads records

```python
@books_bp.get("/")
def list_books():
    books = fetch_all(
        "SELECT id, title, author, published_year FROM books ORDER BY id DESC"
    )
    return render_template("books/list.html", books=books)
```

The route calls MySQL, receives dictionaries, and sends them to Jinja.

### Route receives a form

```python
@books_bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        published_year = request.form.get("published_year", "").strip()
        # Validate, insert, flash, and redirect.
    return render_template("books/form.html")
```

`GET` displays the form. `POST` receives the submitted values. This is the basic Flask form pattern.

### Route uses a variable rule

```python
@books_bp.post("/<int:book_id>/delete")
def delete_book(book_id):
    execute("DELETE FROM books WHERE id = %s", (book_id,))
    return redirect(url_for("books.list_books"))
```

The `<int:book_id>` portion is a variable rule. Flask converts the URL part into an integer-like value. Flask supports converters including `int`, `float`, `path`, and `uuid` [1].

## 11. API endpoints for Postman

Each module has JSON API endpoints. The API uses normal HTTP methods: `GET` retrieves data, `POST` creates data, `PUT` updates data, and `DELETE` removes data [3].

| Module | List | Create | Get one | Update | Delete |
|---|---|---|---|---|---|
| Books | `GET /books/api` | `POST /books/api` | `GET /books/api/1` | `PUT /books/api/1` | `DELETE /books/api/1` |
| Members | `GET /members/api` | `POST /members/api` | `GET /members/api/1` | `PUT /members/api/1` | `DELETE /members/api/1` |
| Reservations | `GET /reservations/api` | `POST /reservations/api` | `GET /reservations/api/1` | Not included to keep the beginner project simple | `DELETE /reservations/api/1` |

### 11.1 Start Flask before testing

```bash
flask --app run.py run --debug
```

Keep this terminal running. The base URL is:

```text
http://127.0.0.1:5000
```

### 11.2 Import the ready-made Postman collection

1. Open Postman.
2. Click **Import**.
3. Select `postman_collection.json` from the project folder.
4. Open the collection named **Simple Library Flask API**.
5. Run requests in this order: list books, create book, list members, create member, create reservation, then get/update/delete records.

### 11.3 Manually create a Postman request

For a create request:

1. Choose method `POST`.
2. Enter `http://127.0.0.1:5000/books/api`.
3. Open **Body → raw**.
4. Select **JSON**.
5. Enter:

```json
{
  "title": "Flask for Beginners",
  "author": "Learning Author",
  "published_year": 2026
}
```

6. Click **Send**.

The expected status is `201 Created`. The API response contains the new ID.

### 11.4 Postman request bodies

Create a member:

```json
{
  "name": "Asha Kumar",
  "email": "asha@example.com",
  "phone": "555-0101"
}
```

Create a reservation after a book and member exist:

```json
{
  "book_id": 1,
  "member_id": 1,
  "reservation_date": "2026-08-24"
}
```

Update a book with `PUT /books/api/1`:

```json
{
  "title": "Flask for Complete Beginners",
  "author": "Learning Author",
  "published_year": 2026
}
```

### 11.5 Expected API status codes

| Situation | Status |
|---|---:|
| Successful list or get | `200 OK` |
| Successful create | `201 Created` |
| Missing required JSON field | `400 Bad Request` |
| Requested ID does not exist | `404 Not Found` |
| Successful delete | `200 OK` |

The API reads JSON with `request.get_json(silent=True)` and returns JSON with `jsonify()`. A JavaScript client can call the same endpoint with `fetch()`. The Fetch API needs explicit status checking because an HTTP error response does not necessarily reject the promise [5].

## 12. Test with curl after Postman

Postman is the main testing tool, but curl helps you understand that APIs are ordinary HTTP requests:

```bash
curl http://127.0.0.1:5000/books/api
```

```bash
curl -X POST http://127.0.0.1:5000/members/api \
  -H "Content-Type: application/json" \
  -d '{"name":"Ravi","email":"ravi@example.com","phone":"555-0103"}'
```

## 13. Common beginner errors

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: flask` | Wrong environment or Flask not installed | Run `conda activate simplelibrary` and `pip install -r requirements.txt` |
| `Unknown database 'library_db'` | `schema.sql` was not run | Run `mysql -u root -p < schema.sql` |
| `Access denied for user flask_user` | Password differs from `schema.sql` | Update `config.py` or recreate the user password |
| `Can't connect to MySQL server` | MySQL service is stopped | Start the MySQL service and retry |
| `TemplateNotFound` | Wrong folder or filename | Check the `app/templates` and module template folders |
| Reservation insert fails | Book or member ID does not exist | Create a book and member first |
| Postman connection refused | Flask is not running | Run `flask --app run.py run --debug` |
| Port 5000 is busy | Another program uses port 5000 | Run `flask --app run.py run --port 5001` and change the Postman base URL |

## 14. What to modify after the first successful run

Do not add advanced features until the basic project works. Make one small change at a time.

### Add an address to Members

This changes the module from three fields to four, so it is useful as a modification exercise:

```sql
ALTER TABLE members ADD COLUMN address VARCHAR(200);
```

Then add an address input to the Jinja form, read it with `request.form.get("address")`, update the `INSERT`, update the `SELECT`, and display `member.address` in the table.

### Add an availability field to Books

Add a Boolean-like column such as `available TINYINT(1) NOT NULL DEFAULT 1`. Display “Available” when the value is `1` and “Not available” otherwise:

```jinja2
{% if book.available %}Available{% else %}Not available{% endif %}
```

### Add a reservation update API

Follow the same pattern as the Books `PUT` route: read JSON, validate the ID, run an `UPDATE`, and return the changed row. Keep the first version simple and add this only after the list, create, get, and delete APIs work.

## 15. Final completion checklist

The project is complete when all of these statements are true:

- Conda environment `simplelibrary` exists and is activated.
- Flask and MySQL Connector/Python are installed.
- MySQL is running.
- `schema.sql` completed without an error.
- `library_db` contains `books`, `members`, and `reservations`.
- `flask --app run.py run --debug` starts the server.
- The home page opens in the browser.
- You can create a book, a member, and a reservation from HTML forms.
- The records remain after a page refresh.
- The Postman collection imports successfully.
- Books and Members create/list/get/update/delete requests work.
- Reservations list/create/get/delete requests work.
- Invalid JSON produces a readable error response.

## References

[1]: https://flask.palletsprojects.com/en/stable/quickstart/ "Flask Quickstart"

[2]: https://dev.mysql.com/doc/connector-python/en/ "MySQL Connector/Python Developer Guide"

[3]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods "MDN HTTP request methods"

[5]: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch "MDN Using the Fetch API"
