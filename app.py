from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Gemini with the API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Configuration page to set API key
@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        api_key = request.form.get("api_key")
        if api_key:
            # Save the API key to the environment variable
            os.environ["GEMINI_API_KEY"] = api_key
            # Update the Gemini client with the new API key
            genai.configure(api_key=api_key)
            return redirect(url_for("home"))
    return render_template("config.html")

# AI Tutor interaction
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("user_input")
    personality = request.form.get("personality", "friendly")

    if not user_input:
        return "Please enter a question."

    # Set system prompt based on personality
    if personality == "funny":
        system_prompt = "You are a funny Python tutor for children. Use humor to explain concepts and provide examples."
    elif personality == "strict":
        system_prompt = "You are a strict Python tutor for children. Be direct and concise in your explanations."
    else:
        system_prompt = "You are a friendly Python tutor for children. Explain concepts in simple terms and provide examples."

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"{system_prompt} {user_input}"
        )
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Homework generation
@app.route("/generate_homework", methods=["POST"])
def generate_homework():
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            "You are a friendly Python tutor for children. Generate a simple Python coding challenge for a beginner."
        )
        return response.text
    except Exception as e:
        return f"An error occurred while generating homework: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)