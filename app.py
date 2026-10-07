from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# The in-memory state store (Python dictionary)
state_store = {}
LIMIT = 3
WINDOW = 60  # 60-second rolling window

@app.before_request
def rate_limiter():
    # Intercept incoming HTTP traffic and get the client IP
    client_ip = request.remote_addr
    current_time = time.time()
    
    # Initialize the IP track record if it is a new visitor
    if client_ip not in state_store:
        state_store[client_ip] = []
        
    # Clean up the track record: remove timestamps older than 60 seconds
    state_store[client_ip] = [t for t in state_store[client_ip] if current_time - t < WINDOW]
    
    # Enforce the strict IP-centric threshold (3 requests per minute)
    if len(state_store[client_ip]) >= LIMIT:
        # Abort processing and return HTTP 429
        return jsonify({"error": "Too Many Requests", "message": "Threshold breached. Max 3 requests per minute."}), 429
        
    # Forward the request and log the new timestamp
    state_store[client_ip].append(current_time)

@app.route('/api/data', methods=['GET'])
def get_synthetic_data():
    # The protected database controller returning a synthetic JSON payload
    return jsonify({
        "status": "success", 
        "data": "Authorized payload execution completed."
    }), 200

if __name__ == '__main__':
    # Run the local REST API
    app.run(port=5000)
