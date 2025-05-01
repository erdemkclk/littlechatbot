import { useState } from 'react'
import './index.css'

function App() {
  const [chat, setChat] = useState([]);
  const [message, setMessage] = useState('');

  const sendMessage = async () => {
    if (!message.trim()) return;
    const newChat = [...chat, { role: 'user', content: message }];
    setChat(newChat);
    setMessage('');

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await res.json();
      const reply = data.choices?.[0]?.message?.content || "[No reply]";
      setChat([...newChat, { role: 'assistant', content: reply }]);
    } catch (err) {
      setChat([...newChat, { role: 'assistant', content: "[Error]" }]);
    }
  };

  return (
    <div className="app">
      <h1>GroqBot</h1>
      <div className="chat-box">
        {chat.map((msg, i) => (
          <p key={i} className={msg.role}>
            <strong>{msg.role}:</strong> {msg.content}
          </p>
        ))}
      </div>
      <input
        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
        placeholder="Say something..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
