import React, { useState, useRef, useEffect } from 'react';
import { Upload, FileCode, Play, Sparkles, RefreshCw, Copy, Check } from 'lucide-react';
import { getSamples } from '../services/api';

export default function CodeEditor({
  code,
  setCode,
  language,
  setLanguage,
  filename,
  setFilename,
  onAnalyze,
  isLoading
}) {
  const [samples, setSamples] = useState([]);
  const [copied, setCopied] = useState(false);
  const textareaRef = useRef(null);
  const lineNumbersRef = useRef(null);

  useEffect(() => {
    getSamples().then(setSamples).catch(console.error);
  }, []);

  const lines = code.split('\n');
  const lineCount = lines.length;

  const handleScroll = (e) => {
    if (lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = e.target.scrollTop;
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFilename(file.name);
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext === 'py') setLanguage('python');
    else if (ext === 'js' || ext === 'jsx' || ext === 'ts') setLanguage('javascript');
    else if (ext === 'java') setLanguage('java');
    else if (ext === 'cpp' || ext === 'c' || ext === 'h') setLanguage('cpp');

    const reader = new FileReader();
    reader.onload = (event) => {
      setCode(event.target.result || '');
    };
    reader.readAsText(file);
  };

  const loadSample = (sample) => {
    setCode(sample.code);
    setLanguage(sample.language);
    setFilename(sample.filename);
  };

  const copyCode = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-dark-border bg-dark-900 shadow-xl overflow-hidden flex flex-col">
      {/* Editor Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-dark-border bg-dark-800/90 px-4 py-2.5">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded-full bg-rose-500/80 inline-block" />
            <span className="h-3 w-3 rounded-full bg-amber-500/80 inline-block" />
            <span className="h-3 w-3 rounded-full bg-emerald-500/80 inline-block" />
          </div>

          <div className="flex items-center gap-2 border-l border-dark-border pl-3">
            <FileCode className="h-4 w-4 text-indigo-400" />
            <input
              type="text"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              placeholder="filename.py"
              className="rounded bg-dark-900/80 border border-dark-border px-2.5 py-1 text-xs text-slate-200 font-mono focus:border-indigo-500 focus:outline-none w-36"
            />
          </div>

          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="rounded bg-dark-900/80 border border-dark-border px-2.5 py-1 text-xs text-slate-200 font-medium focus:border-indigo-500 focus:outline-none"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
          </select>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* Sample Code Dropdown */}
          {samples.length > 0 && (
            <div className="relative group">
              <button
                type="button"
                className="flex items-center gap-1.5 rounded-lg border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-300 hover:bg-indigo-500/20 transition-colors"
              >
                <Sparkles className="h-3.5 w-3.5" />
                Try Sample Code
              </button>
              <div className="absolute right-0 top-full mt-1.5 hidden group-hover:block z-30 w-56 rounded-lg border border-dark-border bg-dark-800 p-1.5 shadow-xl">
                <div className="px-2 py-1 text-[11px] font-semibold uppercase text-slate-400">
                  Pre-configured Flaws
                </div>
                {samples.map((s) => (
                  <button
                    key={s.filename}
                    onClick={() => loadSample(s)}
                    className="w-full text-left rounded px-2 py-1.5 text-xs text-slate-300 hover:bg-dark-700 hover:text-white transition-colors flex items-center justify-between"
                  >
                    <span>{s.label}</span>
                    <span className="text-[10px] uppercase font-mono text-slate-400">{s.language}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Upload Button */}
          <label className="cursor-pointer flex items-center gap-1.5 rounded-lg border border-dark-border bg-dark-700/60 px-3 py-1 text-xs font-medium text-slate-300 hover:bg-dark-700 hover:text-white transition-colors">
            <Upload className="h-3.5 w-3.5" />
            Upload File
            <input
              type="file"
              onChange={handleFileUpload}
              className="hidden"
              accept=".py,.js,.jsx,.ts,.tsx,.java,.cpp,.c,.h"
            />
          </label>

          {/* Copy Button */}
          <button
            onClick={copyCode}
            title="Copy Code"
            className="rounded p-1.5 text-slate-400 hover:bg-dark-700 hover:text-white transition-colors"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
          </button>
        </div>
      </div>

      {/* Editor Workspace: Line Numbers + Textarea */}
      <div className="relative flex flex-1 h-[460px] bg-[#0c1017]">
        {/* Line Numbers gutter */}
        <div
          ref={lineNumbersRef}
          className="select-none overflow-hidden border-r border-dark-border/60 bg-dark-900/90 py-4 px-3 text-right font-mono text-xs text-slate-400 min-w-[3.5rem] leading-6"
        >
          {Array.from({ length: Math.max(lineCount, 15) }, (_, i) => (
            <div key={i + 1}>{i + 1}</div>
          ))}
        </div>

        {/* Code Input Area */}
        <textarea
          ref={textareaRef}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          onScroll={handleScroll}
          spellCheck={false}
          placeholder={`// Paste or write ${language.toUpperCase()} source code here...\n// Or click 'Try Sample Code' above to test with intentional bugs & security flaws.`}
          className="flex-1 resize-none bg-transparent py-4 px-4 font-mono text-xs md:text-sm leading-6 text-slate-100 placeholder-slate-600 focus:outline-none selection:bg-indigo-600/30 overflow-auto"
        />
      </div>

      {/* Footer / Analyze Action */}
      <div className="flex items-center justify-between border-t border-dark-border bg-dark-800/80 px-4 py-3">
        <div className="flex items-center gap-4 text-xs text-slate-400 font-mono">
          <span>{lineCount} lines</span>
          <span>•</span>
          <span>{new Blob([code]).size} bytes</span>
          <span>•</span>
          <span className="uppercase">{language}</span>
        </div>

        <button
          onClick={onAnalyze}
          disabled={isLoading || !code.trim()}
          className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 hover:from-indigo-500 hover:to-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? (
            <>
              <RefreshCw className="h-4 w-4 animate-spin" />
              Running Analysis Pipeline...
            </>
          ) : (
            <>
              <Play className="h-4 w-4 fill-white" />
              Analyze Code
            </>
          )}
        </button>
      </div>
    </div>
  );
}
