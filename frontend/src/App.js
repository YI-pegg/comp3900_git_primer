import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // 确保有这个文件或删除这行

const api = axios.create({
  baseURL: 'http://localhost:5001',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
});

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    setIsLoading(true);
    try {
      const res = await api.post('/api/message', { message });
      setResponse(res.data.response);
    } catch (err) {
      setResponse(`Error: ${err.message}`);
      console.error('API Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Welcome to COMP3900 and COMP9900</h1> {/* 新增欢迎语 */}
      <h2>React ↔ Flask 通信测试</h2>

      <div className="input-group">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="输入要发送的消息"
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !message.trim()}
        >
          {isLoading ? '发送中...' : '发送到Flask'}
        </button>
      </div>

      <div className="response-box">
        <h3>后端响应:</h3>
        <p>{response || (isLoading ? '等待响应...' : '尚未发送消息')}</p>
      </div>
    </div>
  );
}

export default App;
