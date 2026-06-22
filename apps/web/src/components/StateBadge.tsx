import type { DecisionState } from "@/lib/types";

const dangerStates: DecisionState[] = ["REJECTED", "EXIT_THESIS_BROKEN", "BLOCKED_BY_RISK"];
const warnStates: DecisionState[] = ["WATCHLIST", "TECHNICAL_WAIT", "TRIM_CANDIDATE", "RESEARCH_CANDIDATE"];
const okStates: DecisionState[] = ["STARTER_ALLOWED", "ADD_ALLOWED"];

export function StateBadge({ state }: { state: DecisionState | string }) {
  const normalized = state as DecisionState;
  const tone = dangerStates.includes(normalized)
    ? "danger"
    : warnStates.includes(normalized)
      ? "warn"
      : okStates.includes(normalized)
        ? "ok"
        : "";

  return <span className={`badge ${tone}`}>{state.replaceAll("_", " ")}</span>;
}
