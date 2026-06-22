import "./globals.css";
import type { Metadata } from "next";
import type { Route } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Q-GEAR AI Growth OS",
  description: "Local research, scoring, risk, and decision journal for AI-era US equities."
};

const nav: Array<{ href: Route; label: string }> = [
  { href: "/", label: "Dashboard" },
  { href: "/universe", label: "AI Universe" },
  { href: "/earnings", label: "Earnings Lab" },
  { href: "/portfolio", label: "Portfolio Risk" },
  { href: "/journal", label: "Decision Journal" },
  { href: "/reports", label: "Reports" },
  { href: "/settings", label: "Settings" }
];

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <aside className="sidebar">
            <div className="brand">
              <strong>Q-GEAR AI Growth OS</strong>
              <span>Quality, Growth, Earnings Acceleration, AI Relevance, Risk Control</span>
            </div>
            <nav className="nav" aria-label="Primary navigation">
              {nav.map(({ href, label }) => (
                <Link key={href} href={href}>
                  {label}
                </Link>
              ))}
            </nav>
          </aside>
          <main className="main">
            <div className="topbar">
              <small>Demo/local mode. Personal research and educational use only, not licensed financial advice.</small>
              <small>Benchmarks: SPY · QQQ · XLK · SMH</small>
            </div>
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
