'use client';

import { useState } from 'react';
import { Search, Loader2, Trophy, Heart, User, ExternalLink, RefreshCw } from 'lucide-react';
import confetti from 'canvas-confetti';

const InstagramIcon = ({ className }) => (
  <svg 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    className={className}
  >
    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
  </svg>
);

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [comments, setComments] = useState([]);
  const [error, setError] = useState('');
  const [winner, setWinner] = useState(null);

  const fetchComments = async () => {
    if (!url) return;
    setLoading(true);
    setError('');
    setComments([]);
    setWinner(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://giveaway-4hq6.onrender.com';
      const response = await fetch(`${apiUrl}/api/fetch-comments/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch comments');
      }

      setComments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const pickWinner = () => {
    if (comments.length === 0) return;
    
    // Confetti effect
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#3b82f6', '#8b5cf6', '#ec4899']
    });

    const randomIndex = Math.floor(Math.random() * comments.length);
    setWinner(comments[randomIndex]);
  };

  return (
    <main className="max-w-4xl mx-auto px-6 py-12 md:py-20 min-h-screen">
      {/* Header */}
      <div className="text-center mb-16 animate-float">
        <div className="inline-flex items-center justify-center p-3 mb-6 rounded-2xl bg-gradient-to-tr from-blue-500/20 to-purple-500/20 border border-white/10">
          <InstagramIcon className="w-10 h-10 text-purple-400" />
        </div>
        <h1 className="text-5xl md:text-7xl font-bold mb-4 tracking-tight">
          Comment<span className="gradient-text">Picker</span>
        </h1>
        <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto">
          The ultimate Instagram giveaway tool. Fetch top comments, boost engagement, and pick winners with absolute transparency.
        </p>
      </div>

      {/* Input Section */}
      <div className="glass-card p-2 mb-12 flex flex-col md:flex-row gap-2">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
            <Search className="w-5 h-5 text-slate-500" />
          </div>
          <input
            type="text"
            placeholder="Paste Instagram Post or Reel URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full bg-transparent border-none focus:ring-0 text-white pl-12 pr-4 py-4 rounded-xl text-lg placeholder:text-slate-600"
          />
        </div>
        <button
          onClick={fetchComments}
          disabled={loading || !url}
          className="gradient-button px-8 py-4 rounded-xl font-semibold flex items-center justify-center gap-2 disabled:opacity-50 disabled:transform-none"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <RefreshCw className="w-5 h-5" />
          )}
          {loading ? 'Fetching...' : 'Fetch Comments'}
        </button>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl mb-8 text-center">
          {error}
        </div>
      )}

      {/* Winner Modal/Banner */}
      {winner && (
        <div className="mb-12 animate-in zoom-in duration-300">
          <div className="bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-pink-600/20 border border-white/20 p-8 rounded-3xl text-center relative overflow-hidden group">
            <div className="absolute -top-12 -right-12 w-32 h-32 bg-purple-500/20 blur-3xl rounded-full group-hover:bg-purple-500/30 transition-all"></div>
            <Trophy className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
            <h2 className="text-3xl font-bold mb-2">And the winner is...</h2>
            <p className="text-4xl font-extrabold text-white mb-4">@{winner.username}</p>
            <p className="text-slate-300 italic mb-6">"{winner.comment}"</p>
            <button 
              onClick={() => setWinner(null)}
              className="text-sm text-slate-500 hover:text-white transition-colors"
            >
              Close Winner
            </button>
          </div>
        </div>
      )}

      {/* Results Header */}
      {comments.length > 0 && !loading && (
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4 px-2">
          <h3 className="text-2xl font-bold flex items-center gap-2">
            Top 10 Comments <span className="text-sm font-normal text-slate-500">(sorted by likes)</span>
          </h3>
          <button
            onClick={pickWinner}
            className="flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all font-medium"
          >
            <Trophy className="w-5 h-5 text-yellow-500" />
            Pick Random Winner
          </button>
        </div>
      )}

      {/* Comments List */}
      <div className="grid gap-4">
        {comments.map((comment, index) => (
          <div 
            key={index}
            className="group glass-card p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:border-white/20 transition-all duration-300"
          >
            <div className="flex items-center gap-4 flex-1">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center shrink-0 border border-white/5">
                <User className="w-6 h-6 text-slate-400" />
              </div>
              <div className="overflow-hidden">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-white">@{comment.username}</span>
                  {index === 0 && <span className="text-[10px] uppercase tracking-widest bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full border border-blue-500/20">Top Comment</span>}
                </div>
                <p className="text-slate-400 text-sm line-clamp-2 md:line-clamp-none">
                  {comment.comment}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-6 self-end md:self-center shrink-0">
              <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-red-500/5 border border-red-500/10">
                <Heart className="w-4 h-4 text-red-500 fill-red-500/20" />
                <span className="text-red-400 font-bold tabular-nums">{comment.likes}</span>
              </div>
              <a 
                href={url} 
                target="_blank" 
                rel="noreferrer"
                className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
                title="View on Instagram"
              >
                <ExternalLink className="w-4 h-4 text-slate-500" />
              </a>
            </div>
          </div>
        ))}
      </div>

      {comments.length === 0 && !loading && !error && (
        <div className="text-center py-20 opacity-20">
          <InstagramIcon className="w-16 h-16 mx-auto mb-4" />
          <p>Results will appear here...</p>
        </div>
      )}

      {/* Footer Branding */}
      <footer className="mt-24 text-center pb-12 border-t border-white/5 pt-12">
        <p className="text-slate-600 text-sm">
          &copy; {new Date().getFullYear()} CommentPicker AI • Crafted for high engagement posts
        </p>
      </footer>
    </main>
  );
}
