import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  History,
  Search,
  Filter,
  Trash2,
  ExternalLink,
  Download,
  Calendar,
  FileCode,
  RefreshCw
} from 'lucide-react';
import { getReviews, deleteReview, getDownloadReportUrl } from '../services/api';

export default function HistoryPage() {
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [langFilter, setLangFilter] = useState('');

  const fetchReviews = () => {
    setIsLoading(true);
    getReviews({
      search: searchTerm || undefined,
      risk_level: riskFilter || undefined,
      language: langFilter || undefined,
    })
      .then(setReviews)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchReviews();
  }, [searchTerm, riskFilter, langFilter]);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (window.confirm('Delete this code review record?')) {
      try {
        await deleteReview(id);
        setReviews((prev) => prev.filter((r) => r.id !== id));
      } catch (err) {
        alert('Failed to delete review');
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-dark-border pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <History className="h-6 w-6 text-indigo-400" />
            Review History & Audit Trail
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Browse, search, and export past code inspections, vulnerability profiles, and defect risk predictions.
          </p>
        </div>

        <button
          onClick={fetchReviews}
          className="flex items-center gap-1.5 rounded-lg border border-dark-border bg-dark-800 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-dark-700 transition-colors"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Refresh
        </button>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-wrap items-center gap-3 rounded-xl border border-dark-border bg-dark-900 p-3 shadow-md">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by file name..."
            className="w-full rounded-lg bg-dark-800 border border-dark-border pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <select
          value={riskFilter}
          onChange={(e) => setRiskFilter(e.target.value)}
          className="rounded-lg bg-dark-800 border border-dark-border px-3 py-1.5 text-xs text-slate-300 font-medium focus:border-indigo-500 focus:outline-none"
        >
          <option value="">All Risk Levels</option>
          <option value="High">High Risk</option>
          <option value="Medium">Medium Risk</option>
          <option value="Low">Low Risk</option>
        </select>

        <select
          value={langFilter}
          onChange={(e) => setLangFilter(e.target.value)}
          className="rounded-lg bg-dark-800 border border-dark-border px-3 py-1.5 text-xs text-slate-300 font-medium focus:border-indigo-500 focus:outline-none"
        >
          <option value="">All Languages</option>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      {/* History Table */}
      <div className="rounded-xl border border-dark-border bg-dark-900 shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-dark-800/80 text-slate-400 uppercase font-semibold border-b border-dark-border">
              <tr>
                <th className="px-5 py-3">File / Module</th>
                <th className="px-5 py-3">Language</th>
                <th className="px-5 py-3">Audit Date</th>
                <th className="px-5 py-3">Quality Score</th>
                <th className="px-5 py-3">Defect Prob.</th>
                <th className="px-5 py-3">Risk Level</th>
                <th className="px-5 py-3">Total Issues</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border/60">
              {isLoading ? (
                <tr>
                  <td colSpan={8} className="px-5 py-8 text-center text-slate-400">
                    <RefreshCw className="h-5 w-5 animate-spin mx-auto text-indigo-400 mb-2" />
                    Loading records...
                  </td>
                </tr>
              ) : reviews.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-5 py-8 text-center text-slate-400">
                    No matching review records found.
                  </td>
                </tr>
              ) : (
                reviews.map((rev) => (
                  <tr key={rev.id} className="hover:bg-dark-800/40 transition-colors">
                    <td className="px-5 py-3.5 font-mono font-semibold text-slate-200">
                      <div className="flex items-center gap-2">
                        <FileCode className="h-4 w-4 text-indigo-400 shrink-0" />
                        <span>{rev.filename}</span>
                      </div>
                    </td>
                    <td className="px-5 py-3.5 uppercase font-mono text-slate-400">
                      {rev.language}
                    </td>
                    <td className="px-5 py-3.5 text-slate-400">
                      {new Date(rev.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3.5 font-mono">
                      <span
                        className={`font-bold ${
                          rev.quality_score >= 80
                            ? 'text-emerald-400'
                            : rev.quality_score >= 60
                            ? 'text-amber-400'
                            : 'text-rose-400'
                        }`}
                      >
                        {rev.quality_score}/100
                      </span>
                    </td>
                    <td className="px-5 py-3.5 font-mono text-slate-300">
                      {rev.defect_probability}%
                    </td>
                    <td className="px-5 py-3.5">
                      <span
                        className={`rounded border px-2 py-0.5 text-[10px] font-bold uppercase ${
                          rev.risk_level === 'High'
                            ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                            : rev.risk_level === 'Medium'
                            ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                            : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                        }`}
                      >
                        {rev.risk_level}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-slate-300 font-mono">
                      {rev.total_issues}{' '}
                      {rev.critical_issues > 0 && (
                        <span className="text-rose-400 text-[11px]">({rev.critical_issues} crit)</span>
                      )}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          to={`/review/${rev.id}`}
                          className="flex items-center gap-1 rounded bg-dark-800 px-2.5 py-1 text-[11px] font-medium text-slate-300 hover:bg-dark-700 hover:text-white border border-dark-border transition-colors"
                        >
                          View Report
                          <ExternalLink className="h-3 w-3" />
                        </Link>
                        <a
                          href={getDownloadReportUrl(rev.id, 'markdown')}
                          download
                          title="Download Markdown Report"
                          className="rounded bg-dark-800 p-1 text-slate-400 hover:text-white border border-dark-border"
                        >
                          <Download className="h-3.5 w-3.5" />
                        </a>
                        <button
                          onClick={(e) => handleDelete(rev.id, e)}
                          title="Delete review"
                          className="rounded bg-dark-800 p-1 text-slate-400 hover:text-rose-400 border border-dark-border"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
