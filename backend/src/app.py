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

# ✅ 新增计算器接口
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        num1 = int(data.get('num1', 0))
        num2 = int(data.get('num2', 0))
        result = num1 + num2  # 修复了错误，原来是乘法 *
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
