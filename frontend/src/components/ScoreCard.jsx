import React from 'react';
import { ShieldAlert, CheckCircle, AlertTriangle, Bug, Activity, Gauge } from 'lucide-react';

export default function ScoreCard({
  qualityScore = 100,
  riskLevel = 'Low',
  defectProbability = 0,
  metrics = {}
}) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (score >= 60) return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
  };

  const getRiskBadge = (risk) => {
    switch (risk.toLowerCase()) {
      case 'high':
        return {
          bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400',
          icon: ShieldAlert,
          label: 'High Defect Risk'
        };
      case 'medium':
        return {
          bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
          icon: AlertTriangle,
          label: 'Medium Defect Risk'
        };
      default:
        return {
          bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
          icon: CheckCircle,
          label: 'Low Defect Risk'
        };
    }
  };

  const riskBadge = getRiskBadge(riskLevel);
  const RiskIcon = riskBadge.icon;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* 1. Overall Code Quality Score */}
      <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col justify-between">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="font-semibold uppercase tracking-wider">Overall Quality Score</span>
          <Gauge className="h-4 w-4 text-indigo-400" />
        </div>
        
        <div className="my-4 flex items-baseline gap-2">
          <span className={`text-4xl font-extrabold tracking-tight ${getScoreColor(qualityScore).split(' ')[0]}`}>
            {qualityScore}
          </span>
          <span className="text-sm font-semibold text-slate-400">/ 100</span>
        </div>

        <div className="w-full bg-dark-800 rounded-full h-2 overflow-hidden border border-dark-border">
          <div
            className={`h-full transition-all duration-500 ${
              qualityScore >= 80 ? 'bg-emerald-500' : qualityScore >= 60 ? 'bg-amber-500' : 'bg-rose-500'
            }`}
            style={{ width: `${Math.min(100, Math.max(0, qualityScore))}%` }}
          />
        </div>
      </div>

      {/* 2. Defect Risk Level */}
      <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col justify-between">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="font-semibold uppercase tracking-wider">Defect Risk Level</span>
          <RiskIcon className="h-4 w-4 text-slate-400" />
        </div>

        <div className="my-4">
          <div className={`inline-flex items-center gap-2 rounded-lg border px-3.5 py-1.5 text-sm font-bold ${riskBadge.bg}`}>
            <RiskIcon className="h-4 w-4" />
            <span>{riskLevel.toUpperCase()} RISK</span>
          </div>
        </div>

        <p className="text-xs text-slate-400">
          {riskLevel === 'High'
            ? 'Critical vulnerabilities or high cyclomatic branching require remediation.'
            : riskLevel === 'Medium'
            ? 'Moderate defect liability. Refactor identified code smells.'
            : 'Healthy codebase adhering to structural & security standards.'}
        </p>
      </div>

      {/* 3. ML Defect Probability */}
      <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col justify-between">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="font-semibold uppercase tracking-wider">ML Defect Probability</span>
          <Activity className="h-4 w-4 text-violet-400" />
        </div>

        <div className="my-4 flex items-baseline gap-2">
          <span className="text-4xl font-extrabold tracking-tight text-white font-mono">
            {defectProbability}%
          </span>
          <span className="text-xs font-medium text-slate-400">
            {defectProbability > 60 ? 'High Propensity' : defectProbability > 30 ? 'Moderate' : 'Negligible'}
          </span>
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
          <span>LOC: {metrics.loc || 0}</span>
          <span>Complexity: {metrics.cyclomatic_complexity || 1.0}</span>
          <span>Depth: {metrics.max_nesting_depth || 0}</span>
        </div>
      </div>
    </div>
  );
}
