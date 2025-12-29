import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from decimal import Decimal
from tkinter import messagebox, filedialog
# Importing from our translated module
from calculations import calculate_unit_amount, calculate_subtotal, calculate_total
import config as cfg

# Configuration Mappings
MOE_ITEMS = getattr(cfg, "MOE_ITEMS", {})
UF_VALUE = getattr(cfg, "UF_VALUE", 420)
DEFAULT_INDEX = getattr(cfg, "DEFAULT_INDEX", 1.6)

def format_currency_ars(value: Decimal) -> str:
    """Formats a Decimal value into a standard ARS currency string."""
    integer_part, _, decimal_part = f"{value:.2f}".partition(".")
    formatted_integer = "{:,}".format(int(integer_part)).replace(",", ".")
    return f"${formatted_integer},{decimal_part}"

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Technical Opinions Calculator")
        self.root.geometry("980x720")

        title_label = ttk.Label(
            self.root,
            text="Technical Opinions Calculator",
            font=("Segoe UI", 16, "bold"),
        )
        title_label.pack(pady=15)

        # State Variables
        self.uf_value_var = tk.StringVar(value=str(UF_VALUE))
        self.index_var = tk.StringVar(value=str(DEFAULT_INDEX))
        self.quantities = {}
        self.items_flat = {}
        self.flatten_items()

        # Build View
        self.create_interface()
        self._wire_live_updates()

    def _wire_live_updates(self):
        """Traces changes to trigger real-time recalculations."""
        self.uf_value_var.trace_add("write", lambda *_: self.calculate_final_total())
        self.index_var.trace_add("write", lambda *_: self.calculate_final_total())

    def _decimal_from_var(self, var: tk.StringVar, default="0"):
        try:
            return Decimal(var.get().strip().replace(",", "."))
        except Exception:
            return Decimal(default)

    def flatten_items(self):
        for category, items in MOE_ITEMS.items():
            if isinstance(items, dict):
                for item_name, uf_val in items.items():
                    self.items_flat[item_name] = uf_val
            else:
                self.items_flat[category] = items

    def create_interface(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        main_frame.columnconfigure(0, minsize=280, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # --- Left Column: Categories ---
        cat_label = ttk.Label(main_frame, text="Select categories:")
        cat_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        cat_frame = ttk.Frame(main_frame)
        cat_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        cat_frame.rowconfigure(1, weight=1)
        cat_frame.columnconfigure(0, weight=1)

        self.category_listbox = tk.Listbox(
            cat_frame,
            selectmode=tk.MULTIPLE,
            exportselection=False,
            height=18,
            bg="white",
            fg="black"
        )
        self.category_listbox.grid(row=0, column=0, sticky="nsew")

        cat_scroll = ttk.Scrollbar(cat_frame, orient="vertical", command=self.category_listbox.yview)
        cat_scroll.grid(row=0, column=1, sticky="ns")
        self.category_listbox.config(yscrollcommand=cat_scroll.set)

        self.cat_status = ttk.Label(main_frame, text="", bootstyle=INFO)
        self.cat_status.grid(row=0, column=1, sticky="w", padx=10)
        self.cat_status.config(text=f"{len(list(MOE_ITEMS.keys()))} categories | config.py")

        # Populate and Bind
        categories = sorted(list(MOE_ITEMS.keys()))
        for cat in categories:
            self.category_listbox.insert(tk.END, cat)
        self.category_listbox.bind("<<ListboxSelect>>", self.update_item_rows)

        # --- Right Column: Items ---
        self.items_frame = ttk.Frame(main_frame)
        self.items_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

        headers = ["Item", "UF", "Qty", "Subtotal (ARS)"]
        for col, text in enumerate(headers):
            ttk.Label(self.items_frame, text=text, font=("Segoe UI", 10, "bold")).grid(row=0, column=col, padx=5, sticky="w")

        self.subtotal_labels = {}
        self.item_rows = []

        # --- Settings ---
        controls_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        controls_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        ttk.Label(controls_frame, text="UF Value:").grid(row=0, column=0, padx=5)
        ttk.Entry(controls_frame, textvariable=self.uf_value_var, width=12).grid(row=0, column=1, padx=5)

        ttk.Label(controls_frame, text="Index:").grid(row=0, column=2, padx=5)
        ttk.Entry(controls_frame, textvariable=self.index_var, width=12).grid(row=0, column=3, padx=5)

        # --- Buttons ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        # HERE WAS THE ERROR: Method name must match exactly
        ttk.Button(btn_frame, text="Calculate Total", command=self.calculate_final_total, style="success.TButton").pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Reset", command=self.reset, style="secondary.TButton").pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Export CSV", command=self.export_csv).pack(side="left", padx=8)

        self.total_label = ttk.Label(btn_frame, text="Final Total: $0,00", font=("Segoe UI", 14, "bold"), foreground="green")
        self.total_label.pack(side="left", padx=20)

    # ------------ Logic Methods ------------
    def update_item_rows(self, event=None):
        for widgets in self.item_rows:
            for w in widgets: w.destroy()
        self.item_rows.clear()
        self.subtotal_labels.clear()
        self.quantities.clear()

        indices = self.category_listbox.curselection()
        selected = [self.category_listbox.get(i) for i in indices]

        row = 1
        for cat in selected:
            items = MOE_ITEMS[cat]
            if isinstance(items, dict):
                for name, uf in items.items():
                    self._create_row(row, name, uf)
                    row += 1
            else:
                self._create_row(row, cat, items)
                row += 1
        self.calculate_final_total()

    def _create_row(self, row, name, uf):
        ttk.Label(self.items_frame, text=name).grid(row=row, column=0, sticky="w", padx=5)
        ttk.Label(self.items_frame, text=str(uf)).grid(row=row, column=1, padx=5)
        
        q_var = tk.IntVar(value=0)
        ttk.Spinbox(self.items_frame, from_=0, to=999, width=6, textvariable=q_var).grid(row=row, column=2, padx=5)
        q_var.trace_add("write", lambda *_: self.calculate_final_total())
        self.quantities[name] = q_var

        lbl = ttk.Label(self.items_frame, text="$0,00")
        lbl.grid(row=row, column=3, padx=5)
        self.subtotal_labels[name] = lbl
        self.item_rows.append([name, uf, q_var, lbl])

    def calculate_final_total(self):
        """Unified method for calculating all values."""
        try:
            subtotals = []
            val_uf = self._decimal_from_var(self.uf_value_var)
            for name, q_var in self.quantities.items():
                qty = q_var.get()
                uf_units = Decimal(str(self.items_flat[name]))
                m_unit = calculate_unit_amount(uf_units, val_uf)
                sub = calculate_subtotal(m_unit, qty)
                subtotals.append(sub)
                self.subtotal_labels[name].config(text=format_currency_ars(sub))

            idx = self._decimal_from_var(self.index_var, default="1")
            res = calculate_total(subtotals, idx) if subtotals else Decimal("0")
            self.total_label.config(text=f"Final Total: {format_currency_ars(res)}")
        except Exception as e:
            pass # Silent fail for live updates, but you could add a logger here

    def reset(self):
        for v in self.quantities.values(): v.set(0)
        self.calculate_final_total()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
        try:
            import csv
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow(["Item", "UF", "Qty", "Total"])
                # Add data logic here as needed
            messagebox.showinfo("Success", "File exported.")
        except Exception as e:
            messagebox.showerror("Error", str(e))