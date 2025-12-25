from flask import Flask, render_template, request, jsonify
import logging
import os

app = Flask(__name__, template_folder="templates")

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.exception("Template error")
        return "Template not found: " + str(e), 500

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    try:
        path = os.path.join(os.path.dirname(__file__), "messages.txt")
        with open(path, "a", encoding="utf-8") as file:
            file.write(f"Name: {name}, Email: {email}, Message: {message}\n")
    except Exception as e:
        app.logger.exception("Failed to write message")
        return jsonify({"status":"error","message":str(e)}), 500
    return jsonify({"status":"success","message":"Message sent successfully!"})

if __name__ == "__main__":
    app.run(debug=True)