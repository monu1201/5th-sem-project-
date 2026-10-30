import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  FileCode,
  AlertCircle,
  ShieldAlert,
  Flame,
  Award,
  Activity,
  ArrowRight,
  RefreshCw,
  Plus
} from 'lucide-react';
import { getDashboardStats } from '../services/api';
import {
  SeverityDistributionChart,
  RiskDistributionChart,
  QualityTrendChart
} from '../components/Charts';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchStats = () => {
    setIsLoading(true);
    getDashboardStats()
      .then((data) => setStats(data))
      .catch((err) => console.error(err))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center text-slate-400 gap-2">
        <RefreshCw className="h-5 w-5 animate-spin text-indigo-400" />
        <span className="text-sm">Loading dashboard analytics...</span>
      </div>
    );
  }

  const kpis = [
    {
      title: 'Total Scans',
      value: stats?.total_reviews ?? 0,
      icon: FileCode,
      color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20'
    },
    {
      title: 'Issues Detected',
      value: stats?.total_issues ?? 0,
      icon: AlertCircle,
      color: 'text-amber-400 bg-amber-500/10 border-amber-500/20'
    },
    {
      title: 'Critical Flaws',
      value: stats?.critical_issues ?? 0,
      icon: ShieldAlert,
      color: 'text-rose-400 bg-rose-500/10 border-rose-500/20'
    },
    {
      title: 'High-Risk Files',
      value: stats?.high_risk_files ?? 0,
      icon: Flame,
      color: 'text-orange-400 bg-orange-500/10 border-orange-500/20'
    },
    {
      title: 'Avg Quality Score',
      value: `${stats?.avg_quality_score ?? 100}/100`,
      icon: Award,
      color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
    },
    {
      title: 'Avg Defect Prob.',
      value: `${stats?.avg_defect_probability ?? 0}%`,
      icon: Activity,
      color: 'text-purple-400 bg-purple-500/10 border-purple-500/20'
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner & Quick Trigger */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-dark-border pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Code Quality & Defect Intelligence Dashboard
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time aggregate software health telemetry, defect risk distributions, and historical trends.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchStats}
            className="flex items-center gap-1.5 rounded-lg border border-dark-border bg-dark-800 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-dark-700 transition-colors"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh
          </button>
          <Link
            to="/review"
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 shadow-md shadow-indigo-600/30 transition-colors"
          >
            <Plus className="h-3.5 w-3.5" />
            New Review
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div
              key={idx}
              className="rounded-xl border border-dark-border bg-dark-900 p-4 shadow-sm flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                  {kpi.title}
                </span>
                <div className={`rounded p-1.5 border ${kpi.color}`}>
                  <Icon className="h-3.5 w-3.5" />
                </div>
              </div>
              <div className="mt-3 text-xl font-bold text-white tracking-tight">
                {kpi.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <SeverityDistributionChart data={stats?.severity_distribution || {}} />
        <RiskDistributionChart data={stats?.risk_distribution || {}} />
        <QualityTrendChart data={stats?.quality_trend || []} />
      </div>

      {/* Recent Reviews Table */}
      <div className="rounded-xl border border-dark-border bg-dark-900 shadow-xl overflow-hidden">
        <div className="flex items-center justify-between border-b border-dark-border bg-dark-800/80 px-5 py-3.5">
          <h3 className="font-bold text-slate-100 text-sm">Recent Code Reviews</h3>
          <Link
            to="/history"
            className="flex items-center gap-1 text-xs font-medium text-indigo-400 hover:text-indigo-300"
          >
            View all ({stats?.total_reviews ?? 0})
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-dark-800/50 text-slate-400 uppercase font-semibold border-b border-dark-border">
              <tr>
                <th className="px-5 py-3">File / Module</th>
                <th className="px-5 py-3">Language</th>
                <th className="px-5 py-3">Quality</th>
                <th className="px-5 py-3">Defect Prob.</th>
                <th className="px-5 py-3">Risk Level</th>
                <th className="px-5 py-3">Issues</th>
                <th className="px-5 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border/60 font-mono">
              {!stats?.recent_reviews || stats.recent_reviews.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-5 py-8 text-center text-slate-400 font-sans">
                    No code reviews recorded yet. Run your first analysis from the Code Review tab!
                  </td>
                </tr>
              ) : (
                stats.recent_reviews.map((r) => (
                  <tr key={r.id} className="hover:bg-dark-800/40 transition-colors">
                    <td className="px-5 py-3 font-semibold text-slate-200">
                      {r.filename}
                    </td>
                    <td className="px-5 py-3 text-slate-400 uppercase">
                      {r.language}
                    </td>
                    <td className="px-5 py-3">
                      <span
                        className={`font-bold ${
                          r.quality_score >= 80
                            ? 'text-emerald-400'
                            : r.quality_score >= 60
                            ? 'text-amber-400'
                            : 'text-rose-400'
                        }`}
                      >
                        {r.quality_score}
                      </span>
                    </td>
                    <td className="px-5 py-3 text-slate-300">
                      {r.defect_probability}%
                    </td>
                    <td className="px-5 py-3 font-sans">
                      <span
                        className={`rounded border px-2 py-0.5 text-[10px] font-bold uppercase ${
                          r.risk_level === 'High'
                            ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                            : r.risk_level === 'Medium'
                            ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                            : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                        }`}
                      >
                        {r.risk_level}
                      </span>
                    </td>
                    <td className="px-5 py-3 font-sans text-slate-300">
                      {r.total_issues} issues{' '}
                      {r.critical_issues > 0 && (
                        <span className="text-rose-400 font-semibold">({r.critical_issues} crit)</span>
                      )}
                    </td>
                    <td className="px-5 py-3 text-right font-sans">
                      <Link
                        to={`/review/${r.id}`}
                        className="rounded bg-dark-800 px-2.5 py-1 text-[11px] font-medium text-slate-300 hover:bg-dark-700 hover:text-white border border-dark-border"
                      >
                        View Report
                      </Link>
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
