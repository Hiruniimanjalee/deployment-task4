from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return """
    <h1>Deployment Task 4 - Credit</h1>
    <p>My Python Flask application is running inside a Docker container.</p>
    <p>Student: Hiruni Imanjalee</p>
    """

@app.get("/health")
def health():
    return {"status": "ok"}
