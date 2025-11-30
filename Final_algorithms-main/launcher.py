#  launcher.py  —  pretty & robust
import tkinter as tk
from tkinter import ttk, messagebox, RIDGE
import sys
import traceback
import os

# ---------- import your visualisers ----------
try:
    from bst_visualizer  import BSTVisualizer
    from rbt_visualizer  import RedBlackTreeVisualizer
except ImportError as e:
    print("FATAL SETUP ERROR:", e)
    messagebox.showerror(
        "Missing file",
        "Could not find bst_visualizer.py  or  rbt_visualizer.py\n"
        "Please place them in the same folder as this launcher."
    )
    sys.exit(1)


class VisualizerLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tree-Algorithms ")
        self.resizable(False, False)

        # ---------- colour palette ----------
        self.BG       = "#d7e2f7"
        self.CARD     = "#ffffff"
        self.ACCENT   = "#3b82f6"
        self.ACCENT_H = "#2563eb"
        self.TEXT     = "#1f2937"

        self.configure(bg=self.BG)
        self._center_window(420, 420)

        # ---------- style ----------
        style = ttk.Style(self)
        style.theme_use("clam")

        # frame style
        style.configure("Card.TFrame", background=self.CARD, relief=RIDGE, borderwidth=0)
        # button style
        style.configure("Launch.TButton",
                        foreground=self.CARD,
                        background=self.ACCENT,
                        borderwidth=0,
                        focuscolor="",
                        anchor="center",
                        font=("Segoe UI", 12, "bold"))
        style.map("Launch.TButton",
                  background=[("active", self.ACCENT_H), ("pressed", "#1d4ed8")])

        # ---------- widgets ----------
        card = ttk.Frame(self, style="Card.TFrame", padding=40)
        card.pack(expand=True, padx=30, pady=30)

        ttk.Label(card,
                  text="Tree-Algorithms ",
                  font=("Segoe UI", 20, "bold"),
                  foreground=self.TEXT,
                  background=self.CARD).pack(pady=(0, 25))

        ttk.Button(card,
                   text="Binary-Search Tree",
                   command=self.launch_bst,
                   style="Launch.TButton").pack(fill="x", pady=8)

        ttk.Button(card,
                   text="Red-Black Tree",
                   command=self.launch_rbt,
                   style="Launch.TButton").pack(fill="x", pady=8)

        # subtle footer
        ttk.Label(card,
                  text="github.com/",
                  font=("Segoe UI", 9),
                  foreground="#9ca3af",
                  background=self.CARD).pack(pady=(25, 0))

    # ---------- window helpers ----------
    def _center_window(self, width, height):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ---------- launchers ----------
    def launch_bst(self):
        self._run_visualiser("BST Visualiser", BSTVisualizer)

    def launch_rbt(self):
        self._run_visualiser("Red-Black Visualiser", RedBlackTreeVisualizer)

    def _run_visualiser(self, name, visualiser_class):
        self.withdraw()
        window = tk.Toplevel(self)
        try:
            visualiser_class(window)          # instantiate your class
            window.protocol("WM_DELETE_WINDOW", lambda: self._on_close(window))
            window.focus_force()
        except Exception as e:
            self._handle_crash(e, name)
            self.deiconify()

    # ---------- error / close ----------
    def _handle_crash(self, error, name):
        print("-" * 60)
        print(f"ERROR launching {name}")
        traceback.print_exc()
        print("-" * 60)
        messagebox.showerror("Launch error",
                             f"Could not start {name}.\n"
                             f"See console for detailed traceback.")

    def _on_close(self, window):
        window.destroy()
        self.deiconify()
        self.focus_force()


# ---------- entry ----------
if __name__ == "__main__":
    VisualizerLauncher().mainloop()