import type { ReactNode } from "react";
import { TopNav } from "./TopNav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">QG</span>
          <span>
            <strong>Q-GEAR</strong>
            <span>AI Growth OS</span>
          </span>
        </div>
        <TopNav />
        <div className="sidebar-footer">
          <span className="eyebrow">Guardrails</span>
          <strong>No auto-trading</strong>
          <small>Manual research, journal, and risk review only.</small>
        </div>
      </aside>
      <main className="main" id="main-content">
        <div className="topbar">
          <small>Local personal research OS. Educational use only.</small>
          <div className="topbar-status" aria-label="System guardrails">
            <span>Auto-trading off</span>
            <span>Margin off</span>
            <span>Benchmarks: SPY · QQQ · XLK · SMH</span>
          </div>
        </div>
        {children}
      </main>
    </div>
  );
}
