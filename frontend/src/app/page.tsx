'use client';

import { useState, useEffect } from 'react';

// SVG Illustration: A person watering a plant, symbolizing growth and self-care.
const WelcomeIllustration = () => (
  <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" className="w-64 h-64 mx-auto mb-8">
    <path fill="#1F1F3A" d="M45.8,-73.8C58.9,-65.2,68.9,-52,75.9,-37.3C82.9,-22.6,86.9,-6.4,83.7,8.6C80.5,23.6,70.1,37.4,58.3,48.9C46.5,60.4,33.3,69.6,18.8,74.8C4.3,80,-11.5,81.2,-26.8,76.9C-42.1,72.6,-56.9,62.8,-67.5,49.6C-78.1,36.4,-84.5,19.8,-85.1,2.8C-85.7,-14.2,-80.5,-31.6,-70,-44.9C-59.5,-58.2,-43.7,-67.4,-28.3,-73.1C-12.9,-78.8,-2.9,-81,8.1,-82.1C19.1,-83.2,32.7,-82.4,45.8,-73.8Z" transform="translate(100 100)" />
    <text x="50%" y="50%" textAnchor="middle" dy=".3em" fill="#9B8BFF" fontSize="60" fontFamily="Poppins">🌱</text>
  </svg>
);

export default function DashboardPage() {
  const [quest, setQuest] = useState('Loading your quest...');
  const [error, setError] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    async function fetchQuest() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;
        const response = await fetch(`${apiUrl}/api/quest/today`);
        if (!response.ok) throw new Error('Failed to fetch quest.');
        const data = await response.json();
        setQuest(data.text);
      } catch (err: any) {
        setError(err.message);
        setQuest('Could not load quest.');
      }
    }
    fetchQuest();
  }, []);

  const handleComplete = () => {
    setIsCompleted(true);
  };

  return (
    <div className="text-center">
      <h1 className="font-poppins text-4xl md:text-5xl font-bold mb-4">Welcome to Kelvin</h1>
      <p className="text-lg text-gray-400 mb-12">Your space to reflect, grow, and be heard.</p>
      <WelcomeIllustration />
      <div className="max-w-md mx-auto bg-dark-card p-6 rounded-2xl shadow-lg ring-1 ring-white/10">
        <h2 className="font-poppins text-xl font-bold mb-4">Today's Quest</h2>
        {error ? (
          <p className="text-xl font-semibold text-red-400">{error}</p>
        ) : (
          <p className={`text-xl font-semibold text-gray-200 ${isCompleted ? 'line-through text-gray-500' : ''}`}>
            {quest}
          </p>
        )}
        <button 
          onClick={handleComplete}
          disabled={isCompleted}
          className="mt-6 w-full font-poppins font-bold py-3 px-4 rounded-lg transition-all duration-300 disabled:cursor-not-allowed bg-gradient-to-r from-brand-primary to-brand-secondary text-white hover:shadow-lg hover:shadow-brand-primary/40 disabled:from-gray-600 disabled:to-gray-700 disabled:shadow-none"
        >
          {isCompleted ? 'Quest Completed!' : 'Mark as Complete'}
        </button>
      </div>
    </div>
  );
}
