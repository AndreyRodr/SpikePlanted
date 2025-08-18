from flask import Flask, jsonify
from src.api.scrapers.vlr_scrapers import get_match_data

app = Flask(__name__)

# Route to check if the API is running
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the SpikePlanted API!"})

def check_data(data):
    """Checks if the extracted data is valid."""
    return data and data.get('team_1')

# Route to get match data by ID
@app.route('/match-data/<match_id>')
def match_data(match_id):
    # Builds the match URL using the provided ID
    match_url = f"https://www.vlr.gg/{match_id}/"
    
    # Calls your scraping function
    data = get_match_data(match_url)
    
    # If extraction was successful, returns the data as JSON
    if check_data(data):
        return jsonify(f"Match: {data.get('team_1')} {data.get('score_1')} vs {data.get('score_2')} {data.get('team_2')}")
    else:
        # If extraction failed, returns an error message
        return jsonify({"error": "Could not get match data."}), 500

if __name__ == '__main__':
    # Runs the application in debug mode
    app.run(debug=True)