import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, Sparkles, Activity, CheckCircle2, AlertCircle } from 'lucide-react';
import { getHealth } from '../services/api';

export default function Navbar() {
  const [health, setHealth] = useState(null);
  const location = useLocation();

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setHealth({ status: 'offline', active_db: 'disconnected' }));
  }, []);

  return (
    <header className="sticky top-0 z-50 border-b border-dark-border bg-[#0b0f17]/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
            <Shield className="h-5 w-5 text-white" />
          </div>
          <div>
            <span className="text-base font-bold tracking-tight text-white flex items-center gap-2">
              DefectGuard <span className="rounded bg-indigo-500/10 px-1.5 py-0.5 text-xs font-semibold text-indigo-400 border border-indigo-500/20">AI</span>
            </span>
            <span className="text-xs text-slate-400 block -mt-1 font-mono">Intelligent Review & Defect Prediction</span>
          </div>
        </Link>

        {/* Health status badge & Quick CTA */}
        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-2 rounded-full border border-dark-border bg-dark-800/80 px-3 py-1 text-xs">
            <span className={`h-2 w-2 rounded-full ${health?.status === 'healthy' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
            <span className="text-slate-300">
              DB: <strong className="text-white">{health?.active_db || 'Detecting...'}</strong>
            </span>
            <span className="text-slate-500">|</span>
            <span className="text-slate-300">
              ML: <strong className="text-white">{health?.ml_model === 'loaded' ? 'Active' : 'Standby'}</strong>
            </span>
          </div>

          <Link
            to="/review"
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-md shadow-indigo-600/30 hover:bg-indigo-500 transition-colors"
          >
            <Sparkles className="h-4 w-4" />
            Analyze Code
          </Link>
        </div>
      </div>
    </header>
  );
}
