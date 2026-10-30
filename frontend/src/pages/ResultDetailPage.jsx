import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Download,
  Trash2,
  FileCode,
  Calendar,
  Layers,
  Sparkles,
  RefreshCw,
  Cpu,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { getReviewDetail, deleteReview, getDownloadReportUrl } from '../services/api';
import ScoreCard from '../components/ScoreCard';
import IssuesList from '../components/IssuesList';
import CodeDiffViewer from '../components/CodeDiffViewer';

export default function ResultDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [review, setReview] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setIsLoading(true);
    getReviewDetail(id)
      .then(setReview)
      .catch((err) => {
        console.error(err);
        setError('Unable to load code review details.');
      })
      .finally(() => setIsLoading(false));
  }, [id]);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this code review record?')) {
      try {
        await deleteReview(id);
        navigate('/history');
      } catch (err) {
        alert('Failed to delete review');
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center text-slate-400 gap-2">
        <RefreshCw className="h-5 w-5 animate-spin text-indigo-400" />
        <span className="text-sm">Loading review findings...</span>
      </div>
    );
  }

  if (error || !review) {
    return (
      <div className="p-8 text-center space-y-4">
        <AlertCircle className="h-10 w-10 text-rose-400 mx-auto" />
        <h2 className="text-lg font-bold text-white">Review Not Found</h2>
        <p className="text-xs text-slate-400">{error || 'The requested analysis record does not exist.'}</p>
        <Link
          to="/history"
          className="inline-flex items-center gap-1.5 rounded-lg bg-dark-800 px-4 py-2 text-xs text-slate-200 border border-dark-border"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> Back to History
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Actions Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-dark-border pb-5">
        <div className="flex items-center gap-3">
          <Link
            to="/history"
            className="rounded-lg border border-dark-border bg-dark-800 p-2 text-slate-400 hover:text-white transition-colors"
            title="Back to Review History"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white font-mono">
                {review.filename}
              </h1>
              <span className="rounded bg-dark-800 px-2 py-0.5 text-[11px] font-semibold text-slate-300 border border-dark-border uppercase font-mono">
                {review.language}
              </span>
            </div>
            <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
              <span className="flex items-center gap-1">
                <Calendar className="h-3.5 w-3.5" />
                {new Date(review.created_at).toLocaleString()}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Cpu className="h-3.5 w-3.5 text-indigo-400" />
                {review.ai_model_used}
              </span>
            </div>
          </div>
        </div>

        {/* Export & Delete Actions */}
        <div className="flex items-center gap-2">
          {/* Download Report Dropdown */}
          <div className="relative group">
            <button className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 transition-colors shadow-md shadow-indigo-600/30">
              <Download className="h-3.5 w-3.5" />
              Download Report
            </button>
            <div className="absolute right-0 top-full mt-1.5 hidden group-hover:block z-30 w-44 rounded-lg border border-dark-border bg-dark-800 p-1 shadow-xl">
              <a
                href={getDownloadReportUrl(review.id, 'markdown')}
                download
                className="block w-full text-left rounded px-3 py-1.5 text-xs text-slate-300 hover:bg-dark-700 hover:text-white"
              >
                Markdown (.md)
              </a>
              <a
                href={getDownloadReportUrl(review.id, 'html')}
                target="_blank"
                rel="noreferrer"
                className="block w-full text-left rounded px-3 py-1.5 text-xs text-slate-300 hover:bg-dark-700 hover:text-white"
              >
                Printable HTML / PDF
              </a>
              <a
                href={getDownloadReportUrl(review.id, 'json')}
                target="_blank"
                rel="noreferrer"
                className="block w-full text-left rounded px-3 py-1.5 text-xs text-slate-300 hover:bg-dark-700 hover:text-white"
              >
                Structured JSON
              </a>
            </div>
          </div>

          <button
            onClick={handleDelete}
            className="rounded-lg border border-dark-border bg-dark-800 p-2 text-slate-400 hover:text-rose-400 hover:border-rose-500/30 transition-colors"
            title="Delete this review"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Review Summary Alert */}
      {review.review_summary && (
        <div className="rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-4 text-xs text-slate-200 flex items-start gap-3">
          <Sparkles className="h-4 w-4 text-indigo-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-indigo-300 block mb-0.5">Audit Summary:</span>
            <p className="leading-relaxed text-slate-300">{review.review_summary}</p>
          </div>
        </div>
      )}

      {/* Primary Score Cards */}
      <ScoreCard
        qualityScore={review.quality_score}
        riskLevel={review.risk_level}
        defectProbability={review.defect_probability}
        metrics={review.metrics || {}}
      />

      {/* Detected Issues Section */}
      <IssuesList issues={review.issues || []} />

      {/* Code Comparison / Suggested Fix */}
      <CodeDiffViewer
        originalCode={review.source_code}
        suggestedCode={review.suggested_code}
        language={review.language}
      />

      {/* Architectural Recommendations */}
      {review.recommendations && review.recommendations.length > 0 && (
        <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-xl">
          <h3 className="text-sm font-bold text-slate-100 mb-4 flex items-center gap-2">
            <Layers className="h-4 w-4 text-indigo-400" />
            Actionable Strategic Recommendations
          </h3>
          <div className="space-y-3">
            {review.recommendations.map((rec, idx) => (
              <div
                key={idx}
                className="rounded-lg border border-dark-border/80 bg-dark-800/50 p-3.5 text-xs text-slate-300 flex items-start gap-3"
              >
                <span
                  className={`rounded border px-2 py-0.5 text-[10px] font-bold uppercase shrink-0 mt-0.5 ${
                    rec.priority === 'Critical'
                      ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                      : rec.priority === 'High'
                      ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                      : 'bg-indigo-500/10 border-indigo-500/30 text-indigo-400'
                  }`}
                >
                  {rec.priority || 'Medium'}
                </span>
                <div>
                  <h4 className="font-semibold text-slate-100">{rec.title}</h4>
                  <p className="mt-1 text-slate-400 leading-relaxed">{rec.action_plan}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
