"""Simple Tkinter app for estimating income tax and net pay."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

BRACKETS = [
    (11_000, 0.10),
    (44_725, 0.12),
    (95_375, 0.22),
    (182_100, 0.24),
    (231_250, 0.32),
    (578_125, 0.35),
    (float("inf"), 0.37),
]



def estimate_tax(income: float) -> tuple[float, float]:
    """Return estimated federal income tax and effective tax rate.

    Parameters
    ----------
    income:
        Annual taxable income in USD.
    """
    remaining = max(0.0, income)
    tax = 0.0
    lower = 0.0

    for upper, rate in BRACKETS:
        if remaining <= 0:
            break
        taxable = min(upper - lower, remaining)
        tax += taxable * rate
        remaining -= taxable
        lower = upper

    effective_rate = (tax / income * 100.0) if income > 0 else 0.0
    return tax, effective_rate


class TaxingGui(tk.Tk):
    """Desktop GUI for rough tax planning."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Taxing GUI")
        self.resizable(False, False)
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Annual taxable income (USD)").grid(
            row=0, column=0, sticky="w"
        )

        self.income_var = tk.StringVar(value="80000")
        self.result_var = tk.StringVar(value="Enter income and click Calculate.")

        income_entry = ttk.Entry(frame, textvariable=self.income_var, width=20)
        income_entry.grid(row=1, column=0, sticky="ew", pady=(6, 10))
        income_entry.focus()

        ttk.Button(frame, text="Calculate", command=self.calculate).grid(
            row=2, column=0, sticky="ew"
        )

        ttk.Label(
            frame,
            textvariable=self.result_var,
            justify="left",
            wraplength=320,
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))

        frame.columnconfigure(0, weight=1)

    def calculate(self) -> None:
        raw = self.income_var.get().strip().replace(",", "")
        try:
            income = float(raw)
        except ValueError:
            self.result_var.set("Please enter a valid numeric income amount.")
            return

        tax, rate = estimate_tax(income)
        net = max(0.0, income - tax)
        self.result_var.set(
            f"Estimated tax: ${tax:,.2f}\n"
            f"Effective rate: {rate:.2f}%\n"
            f"Estimated net income: ${net:,.2f}"
        )


if __name__ == "__main__":
    app = TaxingGui()
    app.mainloop()
