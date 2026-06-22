from __future__ import annotations

from qgear_core.enums import DecisionState, DrawdownMode
from qgear_core.models import PortfolioContext, PositionSizeRecommendation, StrategySettings


def classify_drawdown_mode(drawdown_pct: float) -> DrawdownMode:
    if drawdown_pct >= 35:
        return DrawdownMode.HARD_AUDIT
    if drawdown_pct >= 30:
        return DrawdownMode.DEFENSIVE
    if drawdown_pct >= 25:
        return DrawdownMode.RISK_CONTROL
    if drawdown_pct >= 20:
        return DrawdownMode.FREEZE_WEAK_THESIS_ADDITIONS
    if drawdown_pct >= 15:
        return DrawdownMode.REDUCE_AGGRESSIVE_NEW_BUYS
    if drawdown_pct >= 10:
        return DrawdownMode.CAUTION_REVIEW
    return DrawdownMode.NORMAL


def recommend_position_size(
    state: DecisionState,
    score_total: float,
    portfolio: PortfolioContext,
    settings: StrategySettings | None = None,
) -> PositionSizeRecommendation:
    settings = settings or StrategySettings()
    drawdown_mode = classify_drawdown_mode(portfolio.portfolio_drawdown_pct)
    reasons: list[str] = []

    if state not in {DecisionState.STARTER_ALLOWED, DecisionState.ADD_ALLOWED}:
        return PositionSizeRecommendation(
            state=state,
            target_weight_pct=0,
            max_new_money=0,
            range_label="Research only: 0%",
            reasons=("No buy/add action is allowed for the current state.",),
            drawdown_mode=drawdown_mode,
        )

    if drawdown_mode == DrawdownMode.HARD_AUDIT:
        return PositionSizeRecommendation(
            state=DecisionState.BLOCKED_BY_RISK,
            target_weight_pct=0,
            max_new_money=0,
            range_label="Hard audit: 0%",
            reasons=("Portfolio drawdown is at or above the hard limit; normal risk-taking is blocked.",),
            drawdown_mode=drawdown_mode,
        )

    if state == DecisionState.STARTER_ALLOWED:
        if score_total >= 85:
            target_weight = 5
            label = "Starter: 2.5-5%"
        else:
            target_weight = 2.5
            label = "Starter: 2.5-5%"
    else:
        if score_total >= 92:
            target_weight = 12
            label = "High conviction: 8-12%"
        elif score_total >= 84:
            target_weight = 8
            label = "Normal: 5-8%"
        else:
            target_weight = 5
            label = "Normal: 5-8%"

    if drawdown_mode in {
        DrawdownMode.REDUCE_AGGRESSIVE_NEW_BUYS,
        DrawdownMode.FREEZE_WEAK_THESIS_ADDITIONS,
    }:
        target_weight = min(target_weight, 5)
        reasons.append("Drawdown mode reduces aggressive new buys.")
    elif drawdown_mode in {DrawdownMode.RISK_CONTROL, DrawdownMode.DEFENSIVE}:
        target_weight = min(target_weight, 2.5)
        reasons.append("Risk-control drawdown mode limits position sizing.")

    target_weight = min(target_weight, settings.max_single_stock_pct)
    remaining_cap_pct = max(0, settings.max_single_stock_pct - portfolio.current_position_weight_pct)
    new_money_pct = max(0, min(target_weight - portfolio.current_position_weight_pct, remaining_cap_pct))

    if portfolio.cash_pct <= settings.cash_buffer_pct:
        reasons.append("Cash is at or below the desired buffer.")
        new_money_pct = 0

    max_new_money = round(portfolio.total_equity * new_money_pct / 100, 2)
    if max_new_money <= 0:
        reasons.append("Current position or cash buffer leaves no room for new money.")
    else:
        reasons.append(f"New money is capped by the {settings.max_single_stock_pct:.1f}% single-stock limit.")

    return PositionSizeRecommendation(
        state=state,
        target_weight_pct=round(target_weight, 2),
        max_new_money=max_new_money,
        range_label=label,
        reasons=tuple(reasons),
        drawdown_mode=drawdown_mode,
    )
