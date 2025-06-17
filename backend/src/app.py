from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# 动态CORS配置
CORS(app, 
     resources={
         r"/api/*": {
             "origins": ["http://localhost:3000", "http://localhost:3001", "http://192.168.50.214:3000"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type"],
             "supports_credentials": False,
             "max_age": 600
         }
     })

@app.after_request
def after_request(response):
    # 动态设置允许的源
    origin = request.headers.get('Origin')
    if origin and origin in ['http://localhost:3000', 'http://localhost:3001', 'http://192.168.50.214:3000']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/api/message', methods=['POST', 'OPTIONS'])
def handle_message():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    message = data.get('message', '')
    return jsonify({
        "response": f"Flask received: {message}",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
