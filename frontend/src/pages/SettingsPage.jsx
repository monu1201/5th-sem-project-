import React, { useState, useEffect } from 'react';
import { Settings, Cpu, ShieldCheck, Database, CheckCircle, Save } from 'lucide-react';
import { getHealth } from '../services/api';

export default function SettingsPage() {
  const [provider, setProvider] = useState('openai');
  const [apiKey, setApiKey] = useState('');
  const [health, setHealth] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getHealth().then(setHealth).catch(console.error);
    const storedProvider = localStorage.getItem('DEFECTGUARD_AI_PROVIDER');
    const storedKey = localStorage.getItem('DEFECTGUARD_AI_KEY');
    if (storedProvider) setProvider(storedProvider);
    if (storedKey) setApiKey(storedKey);
  }, []);

  const handleSave = (e) => {
    e.preventDefault();
    localStorage.setItem('DEFECTGUARD_AI_PROVIDER', provider);
    if (apiKey) {
      localStorage.setItem('DEFECTGUARD_AI_KEY', apiKey);
    }
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="max-w-3xl space-y-6">
      <div className="border-b border-dark-border pb-5">
        <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
          <Settings className="h-6 w-6 text-indigo-400" />
          System Settings & AI Configuration
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Configure AI review provider credentials (OpenAI ChatGPT), observe ML model health, and verify database connectivity.
        </p>
      </div>

      {saved && (
        <div className="flex items-center gap-2 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3.5 text-xs text-emerald-300">
          <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0" />
          <span>Configuration preferences saved successfully.</span>
        </div>
      )}

      {/* AI Provider Config */}
      <form onSubmit={handleSave} className="rounded-xl border border-dark-border bg-dark-900 p-6 shadow-xl space-y-5">
        <div className="flex items-center gap-2 font-bold text-slate-100 text-sm">
          <Cpu className="h-4 w-4 text-indigo-400" />
          AI Review Provider Settings
        </div>

        <div className="space-y-4 text-xs">
          <div>
            <label className="font-semibold text-slate-300 block mb-1.5">
              Active Review Engine
            </label>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="w-full rounded-lg bg-dark-800 border border-dark-border px-3 py-2 text-slate-200 focus:border-indigo-500 focus:outline-none"
            >
              <option value="openai">OpenAI ChatGPT (GPT-4o / GPT-4o-mini - Primary)</option>
              <option value="none">Deterministic Local Engine (C++, Java, Python Offline / Zero-Config)</option>
              <option value="anthropic">Anthropic Claude (Claude 3.5 Sonnet)</option>
              <option value="gemini">Google Gemini (Gemini 1.5 Flash)</option>
              <option value="ollama">Ollama (Local Llama 3)</option>
            </select>
            <p className="text-[11px] text-slate-500 mt-1">
              Select "OpenAI ChatGPT" and paste your OpenAI API key below, or use the built-in offline engine with full C++, Java, and Python support.
            </p>
          </div>

          <div>
            <label className="font-semibold text-slate-300 block mb-1.5">
              API Key (Optional / Overrides Server .env)
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Paste API Key here (or leave blank to use backend .env)"
              className="w-full rounded-lg bg-dark-800 border border-dark-border px-3 py-2 text-slate-200 placeholder-slate-600 focus:border-indigo-500 focus:outline-none font-mono"
            />
          </div>

          <button
            type="submit"
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 transition-colors shadow-md shadow-indigo-600/30"
          >
            <Save className="h-3.5 w-3.5" />
            Save Preferences
          </button>
        </div>
      </form>

      {/* Backend & Model Health Telemetry */}
      <div className="rounded-xl border border-dark-border bg-dark-900 p-6 shadow-xl space-y-4">
        <div className="flex items-center gap-2 font-bold text-slate-100 text-sm">
          <ShieldCheck className="h-4 w-4 text-emerald-400" />
          Runtime Environment & Health
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div className="rounded-lg border border-dark-border bg-dark-800/60 p-3">
            <span className="text-slate-400 block text-[11px] uppercase">Active Database</span>
            <span className="font-mono font-bold text-slate-200 mt-0.5 block">
              {health?.active_db || 'Detecting...'}
            </span>
          </div>

          <div className="rounded-lg border border-dark-border bg-dark-800/60 p-3">
            <span className="text-slate-400 block text-[11px] uppercase">ML Defect Model</span>
            <span className="font-mono font-bold text-emerald-400 mt-0.5 block">
              {health?.ml_model === 'loaded' ? 'Random Forest (Trained & Active)' : 'Standby'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
