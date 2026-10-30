import React from 'react';
import { Link } from 'react-router-dom';
import {
  Shield,
  Sparkles,
  Cpu,
  Binary,
  Layers,
  CheckCircle2,
  ArrowRight,
  Code2,
  FileSearch,
  Database,
  Terminal,
  Activity
} from 'lucide-react';

export default function LandingPage() {
  const steps = [
    { num: '01', title: 'Source Code Input', desc: 'Paste raw code or upload scripts across Python, JavaScript, Java, and C++.' },
    { num: '02', title: 'AST Preprocessing', desc: 'Parses syntax trees, extracts McCabe complexity, nesting depth, and Halstead metrics safely.' },
    { num: '03', title: 'AI Code Review', desc: 'Context-aware LLM or local deterministic engine identifies bugs, smells, and security risks.' },
    { num: '04', title: 'ML Defect Prediction', desc: 'Random Forest and Logistic models compute defect risk probability (0-100%) and proneness.' },
    { num: '05', title: 'Result Analysis', desc: 'Aggregates multi-dimensional signals into overall quality score and risk classification.' },
    { num: '06', title: 'Developer Feedback', desc: 'Actionable recommendations, side-by-side diff fix code, and downloadable audit reports.' },
  ];

  const features = [
    {
      icon: Shield,
      title: 'Security Vulnerability Detection',
      desc: 'Pinpoints SQL injections, arbitrary eval execution, hardcoded tokens, buffer overflows, and unsafe inputs with exact line numbers.'
    },
    {
      icon: Binary,
      title: 'Machine Learning Defect Prediction',
      desc: 'Predicts module defect liability using real software engineering feature distributions (NASA/PROMISE metrics).'
    },
    {
      icon: Cpu,
      title: 'Multi-Provider AI Abstraction',
      desc: 'Supports Google Gemini, OpenAI, Claude, Ollama, and a zero-config local rule engine that works without API keys.'
    },
    {
      icon: Code2,
      title: 'Automated Refactoring & Diffs',
      desc: 'Inspect original source versus refactored, hardened code in a side-by-side comparison with instant copy options.'
    },
    {
      icon: Layers,
      title: 'Intelligent Quality Scoring',
      desc: 'Translates bug counts, architectural smells, and complexity metrics into a normalized 0-100 software health rating.'
    },
    {
      icon: FileSearch,
      title: 'Comprehensive Audit Reports',
      desc: 'Download audit findings as formatted Markdown, structured JSON, or printable HTML compliance summaries.'
    }
  ];

  return (
    <div className="min-h-screen bg-[#0b0f17] text-slate-100 flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-28 px-4 sm:px-6 lg:px-8 border-b border-dark-border">
        {/* Subtle background glow */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[350px] bg-indigo-600/15 blur-[120px] rounded-full pointer-events-none" />

        <div className="mx-auto max-w-5xl text-center relative z-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3.5 py-1 text-xs font-semibold text-indigo-300 mb-6">
            <Sparkles className="h-3.5 w-3.5" />
            Next-Generation Software Intelligence & Quality Assurance
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
            AI-Powered Intelligent Code Review & <span className="bg-gradient-to-r from-indigo-400 via-violet-400 to-purple-400 bg-clip-text text-transparent">Software Defect Prediction</span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-base sm:text-lg text-slate-400 leading-relaxed">
            Eliminate software bugs, patch critical security vulnerabilities, and anticipate defect-prone modules using a hybrid pipeline of AST static analysis, machine learning scoring, and multi-model AI code review.
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Link
              to="/review"
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 hover:from-indigo-500 hover:to-violet-500 transition-all"
            >
              Analyze Source Code
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              to="/dashboard"
              className="flex items-center gap-2 rounded-xl border border-dark-border bg-dark-800/80 px-6 py-3 text-sm font-semibold text-slate-200 hover:bg-dark-700 hover:text-white transition-all"
            >
              <Activity className="h-4 w-4 text-indigo-400" />
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 border-b border-dark-border bg-dark-900/40">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
              System Architecture
            </span>
            <h2 className="mt-2 text-2xl sm:text-3xl font-bold tracking-tight text-white">
              End-to-End Analysis Pipeline
            </h2>
            <p className="mt-2 text-sm text-slate-400 max-w-xl mx-auto">
              How submitted source code transforms into high-fidelity diagnostic intelligence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {steps.map((step) => (
              <div
                key={step.num}
                className="relative rounded-xl border border-dark-border bg-dark-800/50 p-6 shadow-sm hover:border-indigo-500/40 transition-colors"
              >
                <span className="font-mono text-xs font-extrabold text-indigo-400">
                  {step.num}
                </span>
                <h3 className="mt-2 text-base font-bold text-white">
                  {step.title}
                </h3>
                <p className="mt-2 text-xs text-slate-400 leading-relaxed">
                  {step.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Key Features Grid */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 border-b border-dark-border">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
              Core Capabilities
            </span>
            <h2 className="mt-2 text-2xl sm:text-3xl font-bold tracking-tight text-white">
              Designed for High-Reliability Engineering
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feat, idx) => {
              const Icon = feat.icon;
              return (
                <div
                  key={idx}
                  className="rounded-xl border border-dark-border bg-dark-800/40 p-6 shadow-sm hover:bg-dark-800/70 transition-colors"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 mb-4">
                    <Icon className="h-5 w-5" />
                  </div>
                  <h3 className="text-base font-bold text-white">{feat.title}</h3>
                  <p className="mt-2 text-xs text-slate-400 leading-relaxed">
                    {feat.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Stack & Benefits */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-900/40 border-b border-dark-border">
        <div className="mx-auto max-w-5xl text-center">
          <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
            Technology Foundation
          </span>
          <h2 className="mt-2 text-2xl sm:text-3xl font-bold tracking-tight text-white">
            Built on Battle-Tested Open Standards
          </h2>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-4 text-xs font-mono text-slate-300">
            <span className="rounded-lg border border-dark-border bg-dark-800 px-3.5 py-2">FastAPI & Python 3.13</span>
            <span className="rounded-lg border border-dark-border bg-dark-800 px-3.5 py-2">Scikit-Learn (Random Forest)</span>
            <span className="rounded-lg border border-dark-border bg-dark-800 px-3.5 py-2">AST & Radon Complexity</span>
            <span className="rounded-lg border border-dark-border bg-dark-800 px-3.5 py-2">MySQL 8.0 & SQLAlchemy</span>
            <span className="rounded-lg border border-dark-border bg-dark-800 px-3.5 py-2">React 18 & Vite</span>
            <span className="rounded-lg border border-dark-border bg-dark-800 px-3.5 py-2">Tailwind CSS & Recharts</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto py-8 px-4 sm:px-6 border-t border-dark-border text-center text-xs text-slate-500">
        <p>AI-Powered Intelligent Code Review and Software Defect Prediction System &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}
