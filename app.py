from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1098@localhost/AeroBook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app, resources={r"/search_flights": {"origins": "http://localhost:8080"}})

class AirlineDetails(db.Model):
    __tablename__ = 'airline_details'
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(80), nullable=False)

class FlightDetails(db.Model):
    __tablename__ = 'flight_details'
    flight_id = db.Column(db.Integer, primary_key=True)
    airline_id = db.Column(db.Integer, db.ForeignKey('airline_details.airline_id'))
    origin_airport_id = db.Column(db.Integer)
    destination_airport_id = db.Column(db.Integer)
    departure_time = db.Column(db.TIMESTAMP)
    arrival_time = db.Column(db.TIMESTAMP)
    flight_status = db.Column(db.String(50))

@app.route('/search_flights', methods=['POST', 'OPTIONS'])
def search_flights():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response
    
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    
    try:
        query = query = text("""
    SELECT 
        f.flight_id, 
        a.airline_name, 
        ap2.airport_name AS origin,
        ap.airport_name AS destination, 
        f.departure_time, 
        f.arrival_time,
        f.flight_status
    FROM 
        flight_details f
        JOIN airline_details a ON f.airline_id = a.airline_id
        JOIN airports ap ON f.destination_airport_id = ap.airport_id
        JOIN airports ap2 ON f.origin_airport_id = ap2.airport_id
    WHERE 
        ap2.airport_id = :origin_id AND 
        ap.airport_id = :destination_id
""")
        
        result = db.session.execute(query, {"origin_id": origin, "destination_id": destination})
        
        flights = [{
            'flight_id': row.flight_id,
            'airline_name': row.airline_name,
            'origin': row.origin,
            'destination': row.destination,
            'departure_time': row.departure_time,
            'arrival_time': row.arrival_time,
            'flight_status': row.flight_status
        } for row in result.fetchall()]

        return jsonify(flights)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)