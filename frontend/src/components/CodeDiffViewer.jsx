import React, { useState } from 'react';
import { Columns, AlignJustify, Copy, Check, Sparkles } from 'lucide-react';

export default function CodeDiffViewer({ originalCode = '', suggestedCode = '', language = 'python' }) {
  const [viewMode, setViewMode] = useState('split'); // 'split' | 'unified'
  const [copied, setCopied] = useState(false);

  const origLines = (originalCode || '').split('\n');
  const suggLines = (suggestedCode || '').split('\n');

  const copySuggested = () => {
    navigator.clipboard.writeText(suggestedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-dark-border bg-dark-900 shadow-xl overflow-hidden">
      {/* Diff Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-dark-border bg-dark-800/80 px-5 py-3">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-violet-400" />
          <h3 className="font-bold text-slate-100 text-sm md:text-base">
            Code Comparison & Suggested Fix
          </h3>
        </div>

        <div className="flex items-center gap-2">
          {/* View Mode Toggle */}
          <div className="flex items-center rounded-lg border border-dark-border bg-dark-900 p-0.5 text-xs">
            <button
              onClick={() => setViewMode('split')}
              className={`flex items-center gap-1 rounded px-2.5 py-1 font-medium transition-colors ${
                viewMode === 'split' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Columns className="h-3.5 w-3.5" />
              Side-by-Side
            </button>
            <button
              onClick={() => setViewMode('unified')}
              className={`flex items-center gap-1 rounded px-2.5 py-1 font-medium transition-colors ${
                viewMode === 'unified' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <AlignJustify className="h-3.5 w-3.5" />
              Suggested Only
            </button>
          </div>

          <button
            onClick={copySuggested}
            className="flex items-center gap-1.5 rounded-lg border border-dark-border bg-dark-700/60 px-3 py-1 text-xs font-medium text-slate-300 hover:bg-dark-700 hover:text-white transition-colors"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            Copy Fix
          </button>
        </div>
      </div>

      {/* Diff Content View */}
      {viewMode === 'split' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-dark-border text-xs font-mono">
          {/* Original Code Column */}
          <div className="flex flex-col bg-[#0b0e14]">
            <div className="border-b border-dark-border bg-rose-500/10 px-4 py-2 text-[11px] font-semibold uppercase tracking-wider text-rose-400">
              Original Code (Vulnerabilities Detected)
            </div>
            <div className="p-3 overflow-x-auto max-h-[500px] overflow-y-auto space-y-0.5">
              {origLines.map((line, idx) => (
                <div key={idx} className="flex leading-5 hover:bg-white/[0.02]">
                  <span className="w-8 select-none text-right text-slate-400 pr-3 shrink-0">
                    {idx + 1}
                  </span>
                  <span className="text-slate-300 whitespace-pre">{line || ' '}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Suggested Code Column */}
          <div className="flex flex-col bg-[#0b0e14]">
            <div className="border-b border-dark-border bg-emerald-500/10 px-4 py-2 text-[11px] font-semibold uppercase tracking-wider text-emerald-400">
              Suggested Fix (Refactored & Hardened)
            </div>
            <div className="p-3 overflow-x-auto max-h-[500px] overflow-y-auto space-y-0.5">
              {suggLines.map((line, idx) => (
                <div key={idx} className="flex leading-5 hover:bg-emerald-500/5">
                  <span className="w-8 select-none text-right text-emerald-400/80 pr-3 shrink-0">
                    {idx + 1}
                  </span>
                  <span className="text-emerald-300/90 whitespace-pre">{line || ' '}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* Unified View */
        <div className="bg-[#0b0e14] p-4 text-xs font-mono max-h-[500px] overflow-y-auto overflow-x-auto">
          {suggLines.map((line, idx) => (
            <div key={idx} className="flex leading-5 hover:bg-emerald-500/5">
              <span className="w-8 select-none text-right text-slate-400 pr-3 shrink-0">
                {idx + 1}
              </span>
              <span className="text-slate-200 whitespace-pre">{line || ' '}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
