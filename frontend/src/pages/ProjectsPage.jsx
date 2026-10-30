import React, { useState, useEffect } from 'react';
import { FolderGit2, FileCode, Plus, Layers, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { getReviews } from '../services/api';

export default function ProjectsPage() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    getReviews().then(setReviews).catch(console.error);
  }, []);

  // Group reviews by language or project
  const grouped = reviews.reduce((acc, rev) => {
    const key = rev.language.toUpperCase();
    if (!acc[key]) acc[key] = [];
    acc[key].push(rev);
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-dark-border pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <FolderGit2 className="h-6 w-6 text-indigo-400" />
            Project & Module Management
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Group, organize, and monitor software repositories and source files across languages.
          </p>
        </div>

        <Link
          to="/review"
          className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 shadow-md shadow-indigo-600/30 transition-colors"
        >
          <Plus className="h-3.5 w-3.5" />
          Add File / Scan
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {Object.keys(grouped).length === 0 ? (
          <div className="col-span-full p-12 text-center rounded-xl border border-dark-border bg-dark-900 text-slate-400">
            <FolderGit2 className="h-10 w-10 text-slate-600 mx-auto mb-2" />
            <p className="text-sm font-medium">No project modules analyzed yet.</p>
            <Link to="/review" className="text-xs text-indigo-400 hover:underline mt-1 inline-block">
              Start an analysis to generate project telemetry &rarr;
            </Link>
          </div>
        ) : (
          Object.entries(grouped).map(([lang, items]) => {
            const avgQuality = Math.round(
              items.reduce((s, i) => s + i.quality_score, 0) / items.length
            );
            const highRiskCount = items.filter((i) => i.risk_level === 'High').length;

            return (
              <div
                key={lang}
                className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="rounded bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 text-xs font-bold text-indigo-300 font-mono">
                      {lang} MODULE
                    </span>
                    <span className="text-xs text-slate-400 font-mono">
                      {items.length} file{items.length > 1 ? 's' : ''}
                    </span>
                  </div>

                  <div className="mt-4 space-y-2">
                    <div className="flex justify-between text-xs text-slate-300">
                      <span>Avg Quality Score:</span>
                      <strong
                        className={
                          avgQuality >= 80 ? 'text-emerald-400' : avgQuality >= 60 ? 'text-amber-400' : 'text-rose-400'
                        }
                      >
                        {avgQuality}/100
                      </strong>
                    </div>
                    <div className="flex justify-between text-xs text-slate-300">
                      <span>High Risk Files:</span>
                      <strong className={highRiskCount > 0 ? 'text-rose-400' : 'text-slate-300'}>
                        {highRiskCount}
                      </strong>
                    </div>
                  </div>

                  {/* List of files */}
                  <div className="mt-4 pt-3 border-t border-dark-border/60 space-y-1">
                    {items.slice(0, 3).map((item) => (
                      <Link
                        key={item.id}
                        to={`/review/${item.id}`}
                        className="flex items-center justify-between text-xs text-slate-400 hover:text-slate-200 py-1"
                      >
                        <span className="font-mono truncate max-w-[160px]">{item.filename}</span>
                        <span className="text-[11px] font-mono">{item.defect_probability}% prob</span>
                      </Link>
                    ))}
                  </div>
                </div>

                <Link
                  to="/history"
                  className="mt-5 flex items-center justify-center gap-1.5 rounded-lg border border-dark-border bg-dark-800 py-2 text-xs font-semibold text-slate-300 hover:bg-dark-700 hover:text-white transition-colors"
                >
                  View All {lang} Files
                  <ArrowRight className="h-3 w-3" />
                </Link>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
