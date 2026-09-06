from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import re

from database import (
    initialize_database,
    add_record,
    get_all_records,
    record_exists
)

app = Flask(__name__)
app.secret_key = "codealpha-data-guard-secret-key"


def normalize_data(name, email, phone):
    """Clean and normalize user input."""
    name = " ".join(name.strip().split())
    email = email.strip().lower()
    phone = re.sub(r"\D", "", phone)

    return name, email, phone


def validate_data(name, email, phone):
    """Validate submitted data."""
    errors = []

    if not name or len(name) < 2:
        errors.append("Name must contain at least 2 characters.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors.append("Please enter a valid email address.")

    if not re.fullmatch(r"\d{10}", phone):
        errors.append("Phone number must contain exactly 10 digits.")

    return errors


def generate_data_hash(name, email, phone):
    """Generate a SHA-256 fingerprint for the complete record."""
    raw_data = f"{name.lower()}|{email.lower()}|{phone}"
    return hashlib.sha256(raw_data.encode("utf-8")).hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")

        # Normalize input before checking for duplicates.
        name, email, phone = normalize_data(name, email, phone)

        # Validate the submitted information.
        errors = validate_data(name, email, phone)

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("index"))

        # Create a unique fingerprint for the complete record.
        data_hash = generate_data_hash(name, email, phone)

        # Check existing records before inserting.
        if record_exists(email, data_hash):
            flash(
                "Duplicate data detected. This record was not added.",
                "duplicate"
            )
            return redirect(url_for("index"))

        # Store only unique and validated data.
        if add_record(name, email, phone, data_hash):
            flash(
                "Data verified successfully and added to the database.",
                "success"
            )
        else:
            flash(
                "Duplicate data detected. This record was not added.",
                "duplicate"
            )

        return redirect(url_for("index"))

    records = get_all_records()

    return render_template(
        "index.html",
        records=records,
        total_records=len(records)
    )


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)