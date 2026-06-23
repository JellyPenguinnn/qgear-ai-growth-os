import type { ReactNode } from "react";
import { TopNav } from "./TopNav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <strong>Q-GEAR</strong>
          <span>AI Growth OS</span>
        </div>
        <TopNav />
      </aside>
      <main className="main">
        <div className="topbar">
          <small>Local/demo research OS. Personal educational use only.</small>
          <small>Benchmarks: SPY · QQQ · XLK · SMH</small>
        </div>
        {children}
      </main>
    </div>
  );
}
