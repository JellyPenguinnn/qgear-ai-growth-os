"use client";

import type { Route } from "next";
import Link from "next/link";
import { usePathname } from "next/navigation";

const nav: Array<{ href: string; label: string; matcher: (pathname: string) => boolean }> = [
  { href: "/", label: "Today", matcher: (pathname) => pathname === "/" },
  { href: "/pipeline", label: "Pipeline", matcher: (pathname) => pathname.startsWith("/pipeline") },
  { href: "/evidence", label: "Evidence", matcher: (pathname) => pathname.startsWith("/evidence") },
  { href: "/universe", label: "Universe", matcher: (pathname) => pathname.startsWith("/universe") },
  { href: "/earnings", label: "Earnings", matcher: (pathname) => pathname.startsWith("/earnings") },
  { href: "/portfolio", label: "Portfolio", matcher: (pathname) => pathname.startsWith("/portfolio") },
  { href: "/journal", label: "Journal", matcher: (pathname) => pathname.startsWith("/journal") },
  { href: "/reports", label: "Reports", matcher: (pathname) => pathname.startsWith("/reports") },
  { href: "/data-health", label: "Data Health", matcher: (pathname) => pathname.startsWith("/data-health") },
  { href: "/settings", label: "Settings", matcher: (pathname) => pathname.startsWith("/settings") }
];

export function TopNav() {
  const pathname = usePathname();

  return (
    <nav className="nav" aria-label="Primary navigation">
      {nav.map(({ href, label, matcher }) => (
        <Link key={href} href={href as Route} className={matcher(pathname) ? "active" : undefined} aria-current={matcher(pathname) ? "page" : undefined}>
          {label}
        </Link>
      ))}
    </nav>
  );
}
