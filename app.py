from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# Define the function f(x, y)
def f(x, y):
    return x + y  # Modify this function according to your requirement

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-coordinates', methods=['POST'])
def submit_coordinates():
    data = request.json  # Get the JSON data sent from the client
    print('Received coordinates:', data)
    
    coordinates_sum = {'lat_sum': 0.0, 'lng_sum': 0.0}
    lat_sum = sum(item['latitude'] for item in data)
    lng_sum = sum(item['longitude'] for item in data)
    coordinates_sum['lat_sum'] = lat_sum
    coordinates_sum['lng_sum'] = lng_sum
    
    return jsonify(coordinates_sum)

if __name__ == '__main__':
    app.run(debug=True)