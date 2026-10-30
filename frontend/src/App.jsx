import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';
import CodeReviewPage from './pages/CodeReviewPage';
import ResultDetailPage from './pages/ResultDetailPage';
import HistoryPage from './pages/HistoryPage';
import ProjectsPage from './pages/ProjectsPage';
import ReportsPage from './pages/ReportsPage';
import SettingsPage from './pages/SettingsPage';

function DashboardLayout({ children }) {
  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="flex-1 p-6 md:p-8 max-w-7xl mx-auto overflow-y-auto">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#0b0f17] text-slate-100 flex flex-col">
        <Navbar />
        <Routes>
          {/* Landing page */}
          <Route path="/" element={<LandingPage />} />

          {/* App Dashboard views */}
          <Route
            path="/dashboard"
            element={
              <DashboardLayout>
                <DashboardPage />
              </DashboardLayout>
            }
          />
          <Route
            path="/review"
            element={
              <DashboardLayout>
                <CodeReviewPage />
              </DashboardLayout>
            }
          />
          <Route
            path="/review/:id"
            element={
              <DashboardLayout>
                <ResultDetailPage />
              </DashboardLayout>
            }
          />
          <Route
            path="/history"
            element={
              <DashboardLayout>
                <HistoryPage />
              </DashboardLayout>
            }
          />
          <Route
            path="/projects"
            element={
              <DashboardLayout>
                <ProjectsPage />
              </DashboardLayout>
            }
          />
          <Route
            path="/reports"
            element={
              <DashboardLayout>
                <ReportsPage />
              </DashboardLayout>
            }
          />
          <Route
            path="/settings"
            element={
              <DashboardLayout>
                <SettingsPage />
              </DashboardLayout>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}
