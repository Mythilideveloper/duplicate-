from flask import Flask, render_template, request, send_file
import os

from detector import detect_duplicates

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():

    if "file" not in request.files:
        return "No File Uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "Choose a CSV File"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    duplicates, stats = detect_duplicates(filepath)

    return render_template(

        "result.html",

        duplicates=duplicates,

        stats=stats

    )


@app.route("/download")
def download():

    return send_file(
        "duplicate_report.csv",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)