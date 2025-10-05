import Link from 'next/link';

// Reusing simple SVG icons
const QuestIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>;
const ChatIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>;
const JournalIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 3v4M17 3v4"></path></svg>;

export default function BottomNav() {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-[#1F1F3A] p-2 flex justify-around">
      <Link href="/" className="flex flex-col items-center p-2 rounded-md hover:bg-[#9B8BFF] hover:text-white transition-colors">
        <QuestIcon />
        <span className="text-xs">Quest</span>
      </Link>
      <Link href="/chat" className="flex flex-col items-center p-2 rounded-md hover:bg-[#9B8BFF] hover:text-white transition-colors">
        <ChatIcon />
        <span className="text-xs">Chat</span>
      </Link>
      <Link href="/journal" className="flex flex-col items-center p-2 rounded-md hover:bg-[#9B8BFF] hover:text-white transition-colors">
        <JournalIcon />
        <span className="text-xs">Journal</span>
      </Link>
    </nav>
  );
}
