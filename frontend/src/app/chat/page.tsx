'use client';

import { useState, useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'model';
  text: string;
}

const EmptyChatIllustration = () => (
    <div className="text-center my-auto">
        <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" className="w-48 h-48 mx-auto mb-4 text-dark-input">
            <path fill="currentColor" d="M68.7,-23.7C78.3,1.9,67.9,32.2,47.4,49.4C26.9,66.6,-3.7,70.7,-28.8,60.1C-53.9,49.5,-73.5,24.2,-75.2,-2.2C-76.9,-28.6,-60.7,-56.1,-40,-66.5C-19.3,-76.9,6.9,-70.2,30.3,-56.2C53.7,-42.2,79.1,-20.9,68.7,-23.7Z" transform="translate(100 100)" />
        </svg>
        <h3 className="font-poppins font-bold text-xl text-gray-400">It's quiet here...</h3>
        <p className="text-gray-500">Say hello to start a conversation with Kelvin.</p>
    </div>
);

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatContainerRef.current?.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() === '' || isLoading) return;

    const userMessage: Message = { role: 'user', text: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, chat_history: messages.map(m => ({ role: m.role, parts: [m.text] })) }),
      });

      if (!response.ok) throw new Error('Failed to get response from AI.');
      const data = await response.json();
      const aiMessage: Message = { role: 'model', text: data.reply };
      setMessages([...newMessages, aiMessage]);

    } catch (error) {
      console.error(error);
      const errorMessage: Message = { role: 'model', text: 'Sorry, I encountered an error. Please try again.' };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <h1 className="font-poppins text-3xl font-bold mb-4">Chat with Kelvin</h1>
      <div className="bg-dark-card p-4 rounded-2xl shadow-lg ring-1 ring-white/10 flex-grow flex flex-col">
        <div ref={chatContainerRef} className="flex-grow overflow-y-auto mb-4 space-y-6 p-2 pr-4 scrollbar-thin scrollbar-thumb-dark-input scrollbar-track-transparent">
          {messages.length === 0 ? (
             <EmptyChatIllustration />
          ) : (
            messages.map((msg, index) => (
              <div key={index} className={`flex items-end gap-2 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`p-3 rounded-2xl max-w-lg ${msg.role === 'user' ? 'bg-brand-primary text-white rounded-br-none' : 'bg-dark-input rounded-bl-none'}`}>
                  <p className="whitespace-pre-wrap">{msg.text}</p>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex items-end gap-2 justify-start">
                <div className="p-3 rounded-2xl max-w-lg bg-dark-input rounded-bl-none">
                  <p className='animate-pulse'>● ● ●</p>
                </div>
              </div>
          )}
        </div>
        <div className="flex gap-2">
          <input 
            type="text" 
            placeholder="Type your message..." 
            className="flex-grow bg-dark-input rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-brand-primary disabled:opacity-50 transition-all duration-300"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
          />
          <button 
            onClick={handleSend}
            className="font-bold p-3 rounded-lg transition-all duration-300 disabled:cursor-not-allowed bg-gradient-to-r from-brand-primary to-brand-secondary text-white hover:shadow-lg hover:shadow-brand-primary/40 disabled:from-gray-600 disabled:to-gray-700 disabled:shadow-none"
            disabled={isLoading}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
