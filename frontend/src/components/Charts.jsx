import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  CartesianGrid,
  Legend
} from 'recharts';

const SEVERITY_COLORS = {
  Critical: '#dc2626',
  High: '#ea580c',
  Medium: '#d97706',
  Low: '#16a34a'
};

const RISK_COLORS = {
  Low: '#10b981',
  Medium: '#f59e0b',
  High: '#ef4444'
};

export function SeverityDistributionChart({ data = {} }) {
  const chartData = [
    { name: 'Critical', count: data.Critical || 0, fill: SEVERITY_COLORS.Critical },
    { name: 'High', count: data.High || 0, fill: SEVERITY_COLORS.High },
    { name: 'Medium', count: data.Medium || 0, fill: SEVERITY_COLORS.Medium },
    { name: 'Low', count: data.Low || 0, fill: SEVERITY_COLORS.Low },
  ];

  return (
    <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col h-80">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-4">
        Defect Severity Distribution
      </h4>
      <div className="flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
            <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={11} allowDecimals={false} tickLine={false} />
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '8px' }}
              itemStyle={{ color: '#f8fafc', fontSize: '12px' }}
            />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export function RiskDistributionChart({ data = {} }) {
  const chartData = [
    { name: 'Low', value: data.Low || 0, color: RISK_COLORS.Low },
    { name: 'Medium', value: data.Medium || 0, color: RISK_COLORS.Medium },
    { name: 'High', value: data.High || 0, color: RISK_COLORS.High },
  ].filter(d => d.value > 0);

  const displayData = chartData.length > 0 ? chartData : [{ name: 'None', value: 1, color: '#374151' }];

  return (
    <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col h-80">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-4">
        File Risk Classification
      </h4>
      <div className="flex-1 flex items-center justify-center">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '8px' }}
              itemStyle={{ color: '#f8fafc', fontSize: '12px' }}
            />
            <Pie
              data={displayData}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={80}
              paddingAngle={4}
              dataKey="value"
            >
              {displayData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Legend verticalAlign="bottom" height={36} iconType="circle" />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export function QualityTrendChart({ data = [] }) {
  return (
    <div className="rounded-xl border border-dark-border bg-dark-900 p-5 shadow-lg flex flex-col h-80">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-4">
        Code Quality & Defect Probability History
      </h4>
      <div className="flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
            <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} tickLine={false} />
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '8px' }}
              itemStyle={{ color: '#f8fafc', fontSize: '12px' }}
            />
            <Legend verticalAlign="top" height={30} iconType="plainline" />
            <Line
              type="monotone"
              dataKey="quality"
              name="Quality Score"
              stroke="#6366f1"
              strokeWidth={2.5}
              dot={{ fill: '#6366f1', r: 3 }}
            />
            <Line
              type="monotone"
              dataKey="defect_probability"
              name="Defect Probability (%)"
              stroke="#f43f5e"
              strokeWidth={2}
              strokeDasharray="4 4"
              dot={{ fill: '#f43f5e', r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
