"""
Main entry point for the Technical Opinions Calculator.
This module orchestrates the initialization of the UI and the application lifecycle.
"""

import sys
import ttkbootstrap as ttk
from ui import CalculatorApp  # Core interface logic

def main():
    """Initializes the main window and application controller."""
    try:
        # Initialize the root window with a professional modern theme
        # 'flatly' provides a clean, corporate aesthetic suitable for industrial auditing tools
        app_root = ttk.Window(themename="flatly")
        app_root.title("Technical Opinions Calculator - Sanitized Demo")

        # Instantiate the application controller
        # We pass the root window to the CalculatorApp class for UI management
        app = CalculatorApp(app_root) 
        
        # Execute the application main loop
        app_root.mainloop()

    except ImportError as e:
        print(f"Error: Missing dependencies. Please run 'pip install ttkbootstrap'. Detail: {e}")
    except Exception as e:
        print(f"A critical error occurred during application startup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()