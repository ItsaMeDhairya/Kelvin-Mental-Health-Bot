'use client';

import { useState, useEffect } from 'react';

interface JournalEntry {
  date: string;
  title: string;
  mood: 'Happy' | 'Neutral' | 'Sad';
  text: string;
}

export default function JournalPage() {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [newTitle, setNewTitle] = useState('');
  const [newMood, setNewMood] = useState<'Happy' | 'Neutral' | 'Sad'>('Neutral');
  const [newEntry, setNewEntry] = useState('');

  useEffect(() => {
    const savedEntries = localStorage.getItem('journalEntries');
    if (savedEntries) {
      const parsedEntries = JSON.parse(savedEntries);
      // Safely migrate old entries that might be missing fields
      const migratedEntries = parsedEntries.map((entry: any) => ({
        date: entry.date,
        title: entry.title || 'No Title',
        mood: entry.mood || 'Neutral',
        text: entry.text || '',
      }));
      setEntries(migratedEntries);
    }
  }, []);

  const handleSave = () => {
    if (newTitle.trim() === '' || newEntry.trim() === '') return;
    const entry: JournalEntry = { date: new Date().toISOString(), title: newTitle, mood: newMood, text: newEntry };
    const updatedEntries = [entry, ...entries];
    setEntries(updatedEntries);
    localStorage.setItem('journalEntries', JSON.stringify(updatedEntries));
    setNewTitle('');
    setNewMood('Neutral');
    setNewEntry('');
  };

  const MoodDisplay = ({ mood }: { mood: string }) => {
    const moodConfig: { [key: string]: { color: string; emoji: string } } = {
      Happy: { color: 'bg-green-500', emoji: '😊' },
      Neutral: { color: 'bg-yellow-500', emoji: '😐' },
      Sad: { color: 'bg-red-500', emoji: '😔' },
    };
    return <span className={`text-xl mr-2`}>{moodConfig[mood]?.emoji}</span>;
  };

  return (
    <div>
      <h1 className="font-poppins text-3xl font-bold mb-4">Your Private Journal</h1>
      <div className="bg-dark-card p-4 rounded-2xl shadow-lg ring-1 ring-white/10 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <input 
              type="text"
              placeholder="Entry Title"
              className="w-full bg-dark-input rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all duration-300"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
            />
            <select 
              className="w-full bg-dark-input rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all duration-300"
              value={newMood}
              onChange={(e) => setNewMood(e.target.value as any)}
            >
              <option>Happy</option>
              <option>Neutral</option>
              <option>Sad</option>
            </select>
        </div>
        <textarea 
          placeholder="Write your thoughts here..."
          className="w-full h-48 bg-dark-input rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all duration-300"
          value={newEntry}
          onChange={(e) => setNewEntry(e.target.value)}
        ></textarea>
        <button 
          onClick={handleSave}
          className="mt-4 w-full font-poppins font-bold py-3 px-4 rounded-lg transition-all duration-300 bg-gradient-to-r from-brand-primary to-brand-secondary text-white hover:shadow-lg hover:shadow-brand-primary/40 disabled:from-gray-600 disabled:to-gray-700 disabled:shadow-none"
        >
          Save Entry
        </button>
      </div>

      <h2 className="font-poppins text-2xl font-bold mb-4">Past Entries</h2>
      <div className="space-y-4">
        {entries.length > 0 ? (
          entries.map((entry) => (
            <div key={entry.date} className="bg-dark-card p-4 rounded-2xl shadow-lg ring-1 ring-white/10">
              <h3 className="font-poppins text-xl font-bold mb-1 flex items-center">
                <MoodDisplay mood={entry.mood} />
                {entry.title}
              </h3>
              <p className="text-xs text-gray-500 mb-2 ml-8">{new Date(entry.date).toLocaleString()}</p>
              <p className="whitespace-pre-wrap text-gray-300 ml-8">{entry.text}</p>
            </div>
          ))
        ) : (
            <div className="text-center py-12">
                <p className="text-gray-500">You have no journal entries yet.</p>
            </div>
        )}
      </div>
    </div>
  );
}