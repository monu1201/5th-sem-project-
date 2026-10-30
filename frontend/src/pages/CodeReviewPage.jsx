import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, AlertTriangle, ShieldCheck, Zap } from 'lucide-react';
import CodeEditor from '../components/CodeEditor';
import { analyzeCode } from '../services/api';

const DEFAULT_CODE = `import sqlite3

def get_user_profile(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Potential security flaw: SQL injection via string concatenation
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)
    user = cursor.fetchone()

    try:
        conn.close()
    except:
        # Bare except hides critical process crashes
        pass

    return user
`;

export default function CodeReviewPage() {
  const navigate = useNavigate();
  const [code, setCode] = useState(DEFAULT_CODE);
  const [language, setLanguage] = useState('python');
  const [filename, setFilename] = useState('auth_service.py');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleAnalyze = async () => {
    if (!code.trim()) return;

    setIsLoading(true);
    setErrorMessage('');

    try {
      const result = await analyzeCode({
        code,
        language,
        filename,
        project_name: 'Default Workspace',
      });

      // Navigate to detailed results page with newly created review ID
      navigate(`/review/${result.id}`);
    } catch (err) {
      console.error(err);
      const detail = err.response?.data?.detail || 'Failed to analyze code. Please check server connection.';
      setErrorMessage(detail);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-dark-border pb-5">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
          <Sparkles className="h-3.5 w-3.5" />
          Interactive Code Inspection
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">
          AI Code Review & Defect Prediction
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Submit source code in Python, C++, or Java to execute the pipeline: Multi-Language Static Analysis &rarr; ChatGPT AI Code Review &rarr; Section-Wise Defect Analysis & ML Scoring.
        </p>
      </div>

      {/* Error Alert if any */}
      {errorMessage && (
        <div className="flex items-start gap-3 rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-xs text-rose-300">
          <AlertTriangle className="h-4 w-4 shrink-0 text-rose-400 mt-0.5" />
          <div>
            <span className="font-semibold block mb-0.5">Submission Error:</span>
            {errorMessage}
          </div>
        </div>
      )}

      {/* Code Editor Component */}
      <CodeEditor
        code={code}
        setCode={setCode}
        language={language}
        setLanguage={setLanguage}
        filename={filename}
        setFilename={setFilename}
        onAnalyze={handleAnalyze}
        isLoading={isLoading}
      />

      {/* Analysis Pipeline Info Badges */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-xl border border-dark-border bg-dark-900/60 p-4 text-xs">
          <div className="flex items-center gap-2 font-semibold text-slate-200 mb-1">
            <ShieldCheck className="h-4 w-4 text-indigo-400" />
            C++, Java & Python Static Analysis
          </div>
          <p className="text-slate-400 leading-relaxed text-[11px]">
            Deeply audits memory safety, buffer overruns, resource leaks, SQL injections, and control flow complexity across C++, Java, and Python.
          </p>
        </div>

        <div className="rounded-xl border border-dark-border bg-dark-900/60 p-4 text-xs">
          <div className="flex items-center gap-2 font-semibold text-slate-200 mb-1">
            <Zap className="h-4 w-4 text-violet-400" />
            ChatGPT AI Review & Refactoring
          </div>
          <p className="text-slate-400 leading-relaxed text-[11px]">
            Delivers section-wise multi-line analysis: Software Defects, Issue Details, Bug Fixes, and Future Defensive Guidelines.
          </p>
        </div>

        <div className="rounded-xl border border-dark-border bg-dark-900/60 p-4 text-xs">
          <div className="flex items-center gap-2 font-semibold text-slate-200 mb-1">
            <Sparkles className="h-4 w-4 text-amber-400" />
            Random Forest Defect ML
          </div>
          <p className="text-slate-400 leading-relaxed text-[11px]">
            Extracts McCabe cyclomatic complexity, Halstead metrics, and nesting vectors to compute defect probability.
          </p>
        </div>
      </div>
    </div>
  );
}
