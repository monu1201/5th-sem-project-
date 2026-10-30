import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Code2,
  FolderGit2,
  History,
  FileText,
  Settings,
  Sparkles,
  Zap
} from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Code Review', path: '/review', icon: Code2 },
    { name: 'Projects', path: '/projects', icon: FolderGit2 },
    { name: 'Review History', path: '/history', icon: History },
    { name: 'Reports', path: '/reports', icon: FileText },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-dark-border bg-dark-900/60 p-4 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="space-y-1">
        <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20'
                    : 'text-slate-400 hover:bg-dark-800 hover:text-slate-200'
                }`
              }
            >
              <Icon className="h-4 w-4" />
              {item.name}
            </NavLink>
          );
        })}
      </div>

      {/* Pipeline Infobox */}
      <div className="rounded-xl border border-dark-border bg-dark-800/60 p-3.5 text-xs text-slate-400">
        <div className="flex items-center gap-2 font-semibold text-slate-200 mb-2">
          <Zap className="h-4 w-4 text-amber-400" />
          <span>Active Pipeline</span>
        </div>
        <p className="leading-relaxed text-[11px] text-slate-400">
          Source &rarr; AST Preprocessing &rarr; AI Review &rarr; ML Defect Scoring &rarr; Actionable Fixes
        </p>
      </div>
    </aside>
  );
}
