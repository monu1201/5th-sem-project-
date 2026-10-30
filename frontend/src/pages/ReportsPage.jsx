import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FileText, Download, ExternalLink, Calendar, RefreshCw } from 'lucide-react';
import { getReviews, getDownloadReportUrl } from '../services/api';

export default function ReportsPage() {
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getReviews()
      .then(setReviews)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="border-b border-dark-border pb-5">
        <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
          <FileText className="h-6 w-6 text-indigo-400" />
          Code Review & Software Defect Audit Reports
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Export formal compliance, security vulnerability, and software defect risk reports.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {isLoading ? (
          <div className="col-span-full p-12 text-center text-slate-400">
            <RefreshCw className="h-6 w-6 animate-spin mx-auto text-indigo-400 mb-2" />
            Loading reports...
          </div>
        ) : reviews.length === 0 ? (
          <div className="col-span-full p-12 text-center rounded-xl border border-dark-border bg-dark-900 text-slate-400">
            <FileText className="h-10 w-10 text-slate-600 mx-auto mb-2" />
            <p className="text-sm font-medium">No reports generated yet.</p>
            <Link to="/review" className="text-xs text-indigo-400 hover:underline mt-1 inline-block">
              Analyze code to generate an audit report &rarr;
            </Link>
          </div>
        ) : (
          reviews.map((rev) => (
            <div
              key={rev.id}
              className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
                  <span className="uppercase">{rev.language}</span>
                  <span className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    {new Date(rev.created_at).toLocaleDateString()}
                  </span>
                </div>

                <h3 className="mt-2 font-mono font-bold text-slate-100 text-sm truncate">
                  {rev.filename}
                </h3>

                <div className="mt-3 flex items-center gap-2">
                  <span
                    className={`rounded border px-2 py-0.5 text-[10px] font-bold uppercase ${
                      rev.risk_level === 'High'
                        ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                        : rev.risk_level === 'Medium'
                        ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                        : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                    }`}
                  >
                    {rev.risk_level} Risk
                  </span>
                  <span className="text-xs font-mono text-slate-300">
                    Score: {rev.quality_score}/100
                  </span>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-dark-border/60 flex items-center justify-between gap-2">
                <Link
                  to={`/review/${rev.id}`}
                  className="flex items-center gap-1 text-xs font-medium text-indigo-400 hover:text-indigo-300"
                >
                  View Details
                  <ExternalLink className="h-3 w-3" />
                </Link>

                <div className="flex items-center gap-1.5">
                  <a
                    href={getDownloadReportUrl(rev.id, 'markdown')}
                    download
                    className="rounded bg-dark-800 px-2.5 py-1 text-[11px] font-medium text-slate-300 hover:bg-dark-700 hover:text-white border border-dark-border flex items-center gap-1"
                    title="Download Markdown Report"
                  >
                    <Download className="h-3 w-3" />
                    .MD
                  </a>
                  <a
                    href={getDownloadReportUrl(rev.id, 'html')}
                    target="_blank"
                    rel="noreferrer"
                    className="rounded bg-dark-800 px-2.5 py-1 text-[11px] font-medium text-slate-300 hover:bg-dark-700 hover:text-white border border-dark-border flex items-center gap-1"
                    title="Print / PDF View"
                  >
                    HTML
                  </a>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
