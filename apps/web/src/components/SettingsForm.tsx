"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";

export function SettingsForm() {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      starting_capital: Number(form.get("starting_capital")),
      base_currency: String(form.get("base_currency")),
      country: String(form.get("country")),
      risk_style: String(form.get("risk_style")),
      target_cagr_low_pct: Number(form.get("target_cagr_low_pct")),
      target_cagr_high_pct: Number(form.get("target_cagr_high_pct")),
      hard_drawdown_limit_pct: Number(form.get("hard_drawdown_limit_pct")),
      cash_buffer_pct: Number(form.get("cash_buffer_pct")),
      max_single_stock_pct: Number(form.get("max_single_stock_pct")),
      benchmarks: ["SPY", "QQQ", "XLK", "SMH"],
      broker_mode: String(form.get("broker_mode")),
      margin_enabled: false,
      options_enabled: false,
      auto_trading_enabled: false
    };
    try {
      const response = await fetch(`${API_URL}/settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      setMessage(response.ok ? "Settings saved locally." : "Could not save settings. Check that the API is running.");
    } catch {
      setMessage("API unavailable. Demo settings remain visible, but changes were not saved.");
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="form-grid">
        <div className="field">
          <label htmlFor="starting_capital">Starting capital</label>
          <input id="starting_capital" name="starting_capital" type="number" defaultValue="10000" />
        </div>
        <div className="field">
          <label htmlFor="base_currency">Base currency</label>
          <select id="base_currency" name="base_currency" defaultValue="USD">
            <option>USD</option>
            <option>SGD</option>
            <option>MYR</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="country">Country</label>
          <select id="country" name="country" defaultValue="Singapore">
            <option>Singapore</option>
            <option>Malaysia</option>
            <option>Other</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="risk_style">Risk style</label>
          <select id="risk_style" name="risk_style" defaultValue="BALANCED">
            <option value="CONSERVATIVE">Conservative</option>
            <option value="BALANCED">Balanced</option>
            <option value="AGGRESSIVE">Aggressive</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="target_cagr_low_pct">Target CAGR low</label>
          <input id="target_cagr_low_pct" name="target_cagr_low_pct" type="number" defaultValue="18" />
        </div>
        <div className="field">
          <label htmlFor="target_cagr_high_pct">Target CAGR high</label>
          <input id="target_cagr_high_pct" name="target_cagr_high_pct" type="number" defaultValue="22" />
        </div>
        <div className="field">
          <label htmlFor="hard_drawdown_limit_pct">Hard drawdown limit</label>
          <input id="hard_drawdown_limit_pct" name="hard_drawdown_limit_pct" type="number" defaultValue="35" />
        </div>
        <div className="field">
          <label htmlFor="cash_buffer_pct">Cash buffer</label>
          <input id="cash_buffer_pct" name="cash_buffer_pct" type="number" defaultValue="15" />
        </div>
        <div className="field">
          <label htmlFor="max_single_stock_pct">Max single stock</label>
          <input id="max_single_stock_pct" name="max_single_stock_pct" type="number" defaultValue="15" />
        </div>
        <div className="field">
          <label htmlFor="broker_mode">Portfolio mode</label>
          <select id="broker_mode" name="broker_mode" defaultValue="manual">
            <option value="manual">Manual portfolio</option>
          </select>
        </div>
      </div>
      <div className="button-row">
        <button className="button" type="submit">
          Save settings
        </button>
        <span className="badge">Margin disabled</span>
        <span className="badge">Options disabled</span>
        <span className="badge">Auto-trading disabled</span>
        {message ? <span className="muted">{message}</span> : null}
      </div>
    </form>
  );
}
