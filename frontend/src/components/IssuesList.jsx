import React, { useState } from 'react';
import {
  ShieldAlert,
  Bug,
  Flame,
  Wrench,
  AlertCircle,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Filter,
  Compass,
  Code2,
  ShieldCheck,
  Sparkles,
  Terminal
} from 'lucide-react';

export default function IssuesList({ issues = [] }) {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL');
  const [selectedType, setSelectedType] = useState('ALL');
  const [expandedIssues, setExpandedIssues] = useState({});

  const toggleExpand = (index) => {
    setExpandedIssues((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  const getSeverityBadge = (severity) => {
    switch ((severity || '').toLowerCase()) {
      case 'critical':
        return 'bg-rose-500/15 text-rose-400 border-rose-500/30';
      case 'high':
        return 'bg-orange-500/15 text-orange-400 border-orange-500/30';
      case 'medium':
        return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
      default:
        return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
    }
  };

  const getTypeIcon = (type) => {
    switch ((type || '').toLowerCase()) {
      case 'security':
        return <ShieldAlert className="h-4 w-4 text-rose-400" />;
      case 'bug':
        return <Bug className="h-4 w-4 text-orange-400" />;
      case 'code smell':
      case 'codesmell':
        return <Flame className="h-4 w-4 text-amber-400" />;
      default:
        return <Wrench className="h-4 w-4 text-indigo-400" />;
    }
  };

  const filteredIssues = issues.filter((issue) => {
    const matchesSev =
      selectedSeverity === 'ALL' ||
      (issue.severity || '').toUpperCase() === selectedSeverity;
    const matchesType =
      selectedType === 'ALL' ||
      (issue.type || issue.issue_type || '').toUpperCase() === selectedType;
    return matchesSev && matchesType;
  });

  return (
    <div className="rounded-xl border border-dark-border bg-dark-900 shadow-xl overflow-hidden">
      {/* Header & Filters */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-dark-border bg-dark-800/80 px-5 py-3.5">
        <div className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-indigo-400" />
          <h3 className="font-bold text-slate-100 text-sm md:text-base">
            Detected Issues ({filteredIssues.length})
          </h3>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 text-xs text-slate-400">
            <Filter className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Severity:</span>
          </div>
          <select
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="rounded bg-dark-900 border border-dark-border px-2.5 py-1 text-xs text-slate-200 font-medium focus:border-indigo-500 focus:outline-none"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="rounded bg-dark-900 border border-dark-border px-2.5 py-1 text-xs text-slate-200 font-medium focus:border-indigo-500 focus:outline-none"
          >
            <option value="ALL">All Categories</option>
            <option value="SECURITY">Security</option>
            <option value="BUG">Bug</option>
            <option value="CODE SMELL">Code Smell</option>
            <option value="MAINTAINABILITY">Maintainability</option>
          </select>
        </div>
      </div>

      {/* Issues Accordion List */}
      <div className="divide-y divide-dark-border/60">
        {filteredIssues.length === 0 ? (
          <div className="p-8 text-center text-sm text-slate-400 flex flex-col items-center gap-2">
            <CheckCircle2 className="h-8 w-8 text-emerald-400" />
            <span>No issues found matching the selected filter criteria.</span>
          </div>
        ) : (
          filteredIssues.map((issue, idx) => {
            const isExpanded = expandedIssues[idx] !== false; // Default expanded
            const lineNo = issue.line_number ?? issue.line;
            const issueType = issue.type || issue.issue_type || 'General';

            return (
              <div key={idx} className="p-4 hover:bg-dark-800/40 transition-colors">
                {/* Collapsed Header */}
                <div
                  onClick={() => toggleExpand(idx)}
                  className="flex cursor-pointer items-start justify-between gap-3"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5">{getTypeIcon(issueType)}</div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span
                          className={`rounded border px-2 py-0.5 text-[11px] font-bold uppercase tracking-wider ${getSeverityBadge(
                            issue.severity
                          )}`}
                        >
                          {issue.severity || 'Medium'}
                        </span>
                        <span className="rounded bg-dark-800 px-2 py-0.5 text-[11px] font-semibold text-slate-300 border border-dark-border">
                          {issueType}
                        </span>
                        {lineNo && (
                          <span className="font-mono text-xs text-indigo-400">
                            Line {lineNo}
                          </span>
                        )}
                      </div>
                      <h4 className="mt-1 font-semibold text-slate-100 text-sm">
                        {issue.title}
                      </h4>
                    </div>
                  </div>

                  <button className="text-slate-400 hover:text-slate-200">
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                </div>

                {/* Expanded Details - Organized Section-Wise */}
                {isExpanded && (
                  <div className="mt-4 pl-0 sm:pl-7 space-y-3.5 text-xs text-slate-300">
                    {/* Section 1: Software Defect & Root Cause Analysis */}
                    {(issue.software_defect || issue.why_it_matters) && (
                      <div className="rounded-xl border border-rose-500/20 bg-rose-950/15 p-3.5 shadow-sm">
                        <div className="flex items-center gap-2 font-bold text-rose-300 text-[11px] uppercase tracking-wider mb-1.5">
                          <ShieldAlert className="h-3.5 w-3.5 text-rose-400" />
                          Section 1: Software Defect & Root Cause Analysis
                        </div>
                        <div className="whitespace-pre-line leading-relaxed text-slate-300 font-sans text-xs">
                          {issue.software_defect || issue.why_it_matters}
                        </div>
                      </div>
                    )}

                    {/* Section 2: Issue Details & Code Location */}
                    {issue.description && (
                      <div className="rounded-xl border border-dark-border bg-dark-800/60 p-3.5 shadow-sm">
                        <div className="flex items-center gap-2 font-bold text-slate-300 text-[11px] uppercase tracking-wider mb-1.5">
                          <AlertCircle className="h-3.5 w-3.5 text-indigo-400" />
                          Section 2: Issue Details & Findings
                        </div>
                        <div className="whitespace-pre-line leading-relaxed text-slate-200 font-sans text-xs">
                          {issue.description}
                        </div>
                      </div>
                    )}

                    {/* Section 3: Bug Fix & Code Solution */}
                    {(issue.bug_fix || issue.recommendation || issue.suggested_fix) && (
                      <div className="rounded-xl border border-emerald-500/20 bg-emerald-950/15 p-3.5 shadow-sm space-y-2.5">
                        <div className="flex items-center gap-2 font-bold text-emerald-300 text-[11px] uppercase tracking-wider">
                          <Code2 className="h-3.5 w-3.5 text-emerald-400" />
                          Section 3: Bug Fix & Code Solution
                        </div>
                        {(issue.bug_fix || issue.recommendation) && (
                          <div className="whitespace-pre-line leading-relaxed text-slate-200 font-sans text-xs">
                            {issue.bug_fix || issue.recommendation}
                          </div>
                        )}
                        {issue.suggested_fix && (
                          <div>
                            <div className="text-[10px] uppercase font-mono font-semibold text-emerald-400/80 mb-1 flex items-center gap-1">
                              <Terminal className="h-3 w-3" />
                              Remediation Code Replacement:
                            </div>
                            <pre className="rounded-lg border border-dark-border bg-[#0a0e14] p-3 font-mono text-[11px] text-emerald-200 overflow-x-auto">
                              <code>{issue.suggested_fix}</code>
                            </pre>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Section 4: Future Guidelines & Best Practices */}
                    {issue.future_guidelines && (
                      <div className="rounded-xl border border-indigo-500/25 bg-indigo-950/15 p-3.5 shadow-sm">
                        <div className="flex items-center gap-2 font-bold text-indigo-300 text-[11px] uppercase tracking-wider mb-1.5">
                          <Compass className="h-3.5 w-3.5 text-indigo-400" />
                          Section 4: Future Guidelines & Defensive Best Practices
                        </div>
                        <div className="whitespace-pre-line leading-relaxed text-indigo-100 font-sans text-xs">
                          {issue.future_guidelines}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
