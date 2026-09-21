import { FormEvent, useState } from 'react';
import api from '../services/api';

interface ChatEntry {
  role: 'user' | 'assistant';
  text: string;
}

export default function WellnessAssistant() {
  const [messages, setMessages] = useState<ChatEntry[]>([
    { role: 'assistant', text: "Hi, I'm your wellness assistant. Tell me what's on your mind - I can suggest breathing exercises, break ideas, or sleep tips. I can't diagnose anything, and for emergencies please contact a professional." },
  ]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sending, setSending] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: ChatEntry = { role: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setSending(true);

    try {
      const { data } = await api.post('/api/chat', { message: userMsg.text, session_id: sessionId });
      setSessionId(data.session_id);
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Sorry, something went wrong. Please try again.' }]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="chat-page">
      <h1>AI Wellness Assistant</h1>
      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble chat-${m.role}`}>{m.text}</div>
        ))}
      </div>
      <form className="chat-input-row" onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="I am feeling stressed because of my exams..."
        />
        <button type="submit" className="btn btn-primary" disabled={sending}>Send</button>
      </form>
    </div>
  );
}
