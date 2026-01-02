# 📊 Technical Opinions Calculator (Sanitized Demo)

⚠️ **Confidentiality Note:** This is a sanitized version of a tool developed for a government environmental regulatory body. Real coefficients, oil field names, and sensitive business logic have been replaced with dummy data to protect the original employer's intellectual property and data security.

## 🎯 Project Purpose
A specialized Desktop Application designed to automate the settlement of technical fees for hydrocarbon projects.

The primary objective was to **eliminate human error** and remove hardcoded pricing by implementing a system based on **Fixed Units (UF)** and dynamic configurations. This allows for mass price updates without modifying the source code, ensuring system longevity and reliability.

## 🛠️ Tech Stack & Design Decisions
* **Language:** Python 3.13+.
* **GUI:** `ttkbootstrap` (Modern Tkinter enhancement for professional UI).
Data Reporting: openpyxl (Automated generation of professionally formatted .xlsx Excel reports with styling, formulas, and auto-adjusted columns for executive review).
## ⚙️ Engineering Key Points
* **Financial Precision (Decimal vs. Float):** Implemented the `decimal.Decimal` module with **banker's rounding** (`ROUND_HALF_UP`). This avoids floating-point errors common in float types, which is critical for monetary and regulatory calculations.
* **Decoupled Architecture (Separation of Concerns):**
    * `calculations.py`: Pure business logic, highly testable independent of the UI.
    * `ui.py`: Event handling and visual presentation using `CalculatorApp` class.
    * `config.py`: Data layer acting as the **Single Source of Truth** for pricing using `MOE_ITEMS`.
* **Reactivity:** Implemented observers (`trace_add`) on input variables to trigger real-time recalculations (reactive style), improving UX and ensuring data consistency.

## 📂 Project Structure
```plaintext
technical-opinions-calculator/
├── main.py           # Entry point (Dependency injection)
├── ui.py             # Presentation Layer (English GUI)
├── calculations.py   # Business Logic Layer (Pure logic and validations)
├── config.py         # Data Layer (Sanitized configuration)
└── README.md         # Documentation
