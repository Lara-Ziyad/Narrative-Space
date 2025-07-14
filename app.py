from flask import Flask
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)


# Basic route to test the API
@app.route('/')
def index():
    return "NarrativeSpace API is running!"

if __name__ == '__main__':
    app.run(debug=True)
