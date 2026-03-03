import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { chatbotAPI } from '../services/api';
import axios from 'axios';
import { Send, Sparkles, Bot, User, Zap, BookOpen, Target, Clock, Lightbulb, GraduationCap } from 'lucide-react';
import toast from 'react-hot-toast';
import './ChatbotPage.css';

// Chatbot API endpoint - uses environment variable in production
const CHATBOT_API_URL = process.env.REACT_APP_CHATBOT_URL 
  ? `${process.env.REACT_APP_CHATBOT_URL}/chat`
  : 'http://localhost:5002/chat';

const ChatbotPage = () => {
  const { student } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [typing, setTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Get student_id - use student.id if student role, or default to 1 for testing
  const studentId = student?.id || 1;

  useEffect(() => {
    if (studentId) {
      loadChatHistory();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      setLoading(true);
      const response = await chatbotAPI.getHistory(studentId, 20);
      setMessages(response.data.history.map(msg => ([
        { text: msg.message, sender: 'user', timestamp: msg.created_at },
        { text: msg.response, sender: 'ai', timestamp: msg.created_at }
      ])).flat());
    } catch (error) {
      console.error('Error loading chat history:', error);
    } finally {
      setLoading(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { text: userMessage, sender: 'user', timestamp: new Date().toISOString() }]);
    
    setTyping(true);

    try {
      // Use new Node.js chatbot API
      const response = await axios.post(CHATBOT_API_URL, {
        message: userMessage
      });

      // Add AI response to chat
      setMessages(prev => [...prev, { 
        text: response.data.reply, 
        sender: 'ai',
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message');
      
      // Add error message
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error. Please try again.', 
        sender: 'ai',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setTyping(false);
      inputRef.current?.focus();
    }
  };

  const suggestedPrompts = [
    { icon: BookOpen, text: "Create a study plan for me", color: "purple" },
    { icon: Target, text: "How can I improve my grades?", color: "green" },
    { icon: Clock, text: "Suggest time management tips", color: "amber" },
    { icon: GraduationCap, text: "Help me prepare for exams", color: "blue" },
    { icon: Lightbulb, text: "Motivate me to study", color: "pink" },
    { icon: Zap, text: "Quick revision strategies", color: "cyan" },
  ];

  const handlePromptClick = (prompt) => {
    setInputMessage(prompt);
    inputRef.current?.focus();
  };

  return (
    <div className="chatbot-page">
      {/* Chat Container */}
      <div className="chat-container">
        {/* Sidebar - AI Info */}
        <div className="chat-sidebar">
          <div className="ai-profile">
            <div className="ai-avatar">
              <div className="ai-avatar-ring"></div>
              <Bot size={28} />
            </div>
            <h2 className="ai-name">AI Academic Mentor</h2>
            <p className="ai-description">Your personal AI assistant for academic success</p>
          </div>
          
          <div className="ai-capabilities">
            <h3 className="capabilities-title">I can help you with</h3>
            <ul className="capabilities-list">
              <li><Sparkles size={14} /> Personalized study plans</li>
              <li><Sparkles size={14} /> Exam preparation tips</li>
              <li><Sparkles size={14} /> Time management advice</li>
              <li><Sparkles size={14} /> Career guidance</li>
              <li><Sparkles size={14} /> Learning strategies</li>
            </ul>
          </div>

          <div className="ai-status">
            <div className="status-indicator">
              <span className="status-dot online"></span>
              <span>Online & Ready</span>
            </div>
            <p className="powered-by">Powered by AI</p>
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="chat-main">
          {/* Messages Area */}
          <div className="messages-area">
            {loading ? (
              <div className="chat-loading">
                <div className="loading-animation">
                  <Sparkles className="loading-icon" size={32} />
                </div>
                <p>Loading conversation...</p>
              </div>
            ) : messages.length === 0 ? (
              <div className="welcome-screen">
                <div className="welcome-header">
                  <div className="welcome-icon">
                    <Sparkles size={32} />
                  </div>
                  <h2>Welcome to AI Academic Mentor</h2>
                  <p>I'm here to help you succeed in your academic journey. Ask me anything!</p>
                </div>
                
                <div className="suggested-prompts">
                  <h3>Try asking:</h3>
                  <div className="prompts-grid">
                    {suggestedPrompts.map((prompt, index) => (
                      <button
                        key={index}
                        className={`prompt-card ${prompt.color}`}
                        onClick={() => handlePromptClick(prompt.text)}
                      >
                        <prompt.icon size={20} />
                        <span>{prompt.text}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="messages-list">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`message ${message.sender === 'user' ? 'user' : 'ai'}`}
                  >
                    <div className="message-avatar">
                      {message.sender === 'user' ? (
                        <User size={18} />
                      ) : (
                        <Bot size={18} />
                      )}
                    </div>
                    <div className="message-content">
                      <div className="message-header">
                        <span className="sender-name">
                          {message.sender === 'user' ? 'You' : 'AI Mentor'}
                        </span>
                      </div>
                      <div className="message-bubble">
                        <p>{message.text}</p>
                      </div>
                    </div>
                  </div>
                ))}
                
                {typing && (
                  <div className="message ai">
                    <div className="message-avatar">
                      <Bot size={18} />
                    </div>
                    <div className="message-content">
                      <div className="message-header">
                        <span className="sender-name">AI Mentor</span>
                      </div>
                      <div className="message-bubble typing">
                        <div className="typing-dots">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="input-area">
            <form className="input-form" onSubmit={handleSendMessage}>
              <div className="input-wrapper">
                <input
                  ref={inputRef}
                  type="text"
                  className="chat-input"
                  placeholder="Ask me anything about your studies..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  disabled={typing}
                />
                <button 
                  type="submit" 
                  className="send-btn"
                  disabled={!inputMessage.trim() || typing}
                >
                  <Send size={18} />
                </button>
              </div>
              <p className="input-hint">Press Enter to send your message</p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;
