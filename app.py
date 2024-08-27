from flask import Flask, render_template, request, jsonify, session
from Centre_Calculator import Centre_Calculator
from Point import Point
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=6)  # Sessions expire after 30 minutes

calc = Centre_Calculator()

def retrieve_markers():
    """Retrieve markers from the session and convert them to Point objects."""
    if 'markers' not in session:
        session['markers'] = []
    return [{"vertex": Point.from_dict(marker["vertex"]), "id": marker["id"]} for marker in session['markers']]

def save_markers(markers):
    """Convert Point objects to dictionaries and save them in the session."""
    session['markers'] = [{"vertex": marker["vertex"].to_dict(), "id": marker["id"]} for marker in markers]
    session.modified = True

def set_id(current):
    if 'current_id' not in session:
        session['current_id'] = 0
    session['current_id'] = current+1
    session.modified = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-current-id', methods=['GET'])
def get_current_id():
    if 'current_id' not in session:
        session['current_id'] = 0
    return jsonify({'id': session['current_id']}), 200

@app.route('/get-markers', methods=['GET'])
def get_markers():
    if 'markers' not in session:
        session['markers'] = []
        return jsonify([]), 200
    else:
        markers = retrieve_markers()
        return jsonify([{'latitude': point['vertex'].polar[0], 'longitude': point['vertex'].polar[1], 'id': point['id']} for point in markers])

@app.route('/add-marker', methods=['POST'])
def add_marker():
    vertex = request.json
    point = Point.fromPolar([vertex['vertex']['latitude'], vertex['vertex']['longitude']])
    marker_id = vertex['id']
    
    # Retrieve current markers from session
    markers = retrieve_markers()
    markers.append({"vertex": point, "id": marker_id})

    set_id(marker_id)
    
    # Save updated markers back to session
    save_markers(markers)
    # for m in markers:
    #     print(m)
    return jsonify({'status': 'success'}), 200

@app.route('/del-marker', methods=['POST'])
def del_marker():
    vertex = request.json

    markers = retrieve_markers()

    markers = [point for point in markers if not (point['id'] == vertex['id'])]
    save_markers(markers)
    # for m in markers:
    #     print(str(m['vertex']))
    
    return jsonify({'status': 'success'}), 200

@app.route('/update-marker', methods=['POST'])
def update_marker():
    vertex = request.json
    markers = retrieve_markers()

    for point in markers:
        if (point['id'] == vertex['id']):
            point['vertex'] = Point.fromPolar([vertex['vertex']['latitude'], vertex['vertex']['longitude']])
            save_markers(markers)
            # for m in markers:
            #     print(str(m['vertex']))
            return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failed'}), 200

@app.route('/refresh', methods=['POST'])
def refresh():
    # Clear markers from session
    session.pop('markers', None)
    
    # Reset current ID in session
    session['current_id'] = 0
    session.modified = True

    return jsonify({'status': 'success'}), 200


@app.route('/calculate_centre', methods=['POST'])
def submit_coordinates():
    # Retrieve markers from session
    markers = retrieve_markers()
    vertices = [m['vertex'] for m in markers]
    
    # Calculate the center
    centre = calc.centre(vertices)
    arcvariance = calc.arcvariance(centre, vertices)

    arcdistances = [{'distance': calc.arcdistance(centre, m['vertex']), 'id':m['id']} for m in markers]

    print(centre)
    print(arcdistances)
    print(arcvariance)
    
    return jsonify({'vertex': centre.to_dict(), 'arcvariance': arcvariance, 'arcdistances': arcdistances})

if __name__ == '__main__':
    app.run(debug=True)
