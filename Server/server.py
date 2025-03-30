from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        if request.method == 'POST':  # ✅ Handle POST requests
            data = request.json if request.is_json else request.form
        else:  # ✅ Handle GET requests
            data = request.args

        # ✅ Extract parameters safely
        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

        # ✅ Ensure all required fields are present
        if not location or total_sqft <= 0 or bhk <= 0 or bath <= 0:
            return jsonify({'error': 'Invalid input data'}), 400  # Return Bad Request if data is missing

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # ✅ Handle server errors properly

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)  # ✅ Debug mode for better error messages
