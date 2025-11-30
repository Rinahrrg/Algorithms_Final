# rbt_visualizer.py  –  Tkinter GUI that imports rbt_logic

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import os
import asyncio
from typing import Optional, List, Tuple, Dict

# import the separated logic
from rbt_logic import RedBlackTree, RedBlackTreeNode


class RedBlackTreeVisualizer:
    def __init__(self, master: tk.Tk) -> None:
        self.master: tk.Tk = master
        self.master.title("Red-Black Tree Visualizer")

        self.color_only_mode: tk.BooleanVar = tk.BooleanVar(value=False)
        self.tree: RedBlackTree = RedBlackTree(color_only=self.color_only_mode.get())

        self.search_path_edges: List[Tuple[RedBlackTreeNode, RedBlackTreeNode]] = []
        self.node_positions: Dict[RedBlackTreeNode, Tuple[int, int, int, int]] = {}
        self.tooltip_label: Optional[tk.Label] = None

        self.hide_nil_var: tk.BooleanVar = tk.BooleanVar(value=False)
        self.zoom_var: tk.DoubleVar = tk.DoubleVar(value=1.0)
        self.theme_var: tk.StringVar = tk.StringVar(value="Classic")
        self.manual_coloring_var: tk.BooleanVar = tk.BooleanVar(value=False)

        self.themes: Dict[str, Dict[str, str]] = {
            "Classic": {"bg": "light blue", "red_node": "red", "black_node": "black", "text_color": "white", "outline": "black", "edge": "black"},
            "Dark": {"bg": "#333333", "red_node": "#cc4444", "black_node": "#555555", "text_color": "white"},
            "High Contrast": {"bg": "white", "red_node": "blue", "black_node": "black", "text_color": "white"},
        }
        self.current_theme: Dict[str, str] = self.themes[self.theme_var.get()]

        # --- Color Palette & Styles ---
        self.ACCENT = "#3b82f6"
        self.ACCENT_H = "#2563eb"
        self.TEXT_ON_ACCENT = "#ffffff"
        self.button_style = {
            "bg": self.ACCENT, "fg": self.TEXT_ON_ACCENT,
            "activebackground": self.ACCENT_H, "activeforeground": self.TEXT_ON_ACCENT,
            "relief": tk.FLAT, "borderwidth": 0, "font": ("Segoe UI", 9, "bold"),
            "padx": 10, "pady": 4
        }

        # -------------------- GUI BUILD --------------------
        # --- Main Actions Frame ---
        main_actions_frame = tk.Frame(master)
        main_actions_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(main_actions_frame, text="Value:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.on_value_change)
        self.value_entry = tk.Entry(main_actions_frame, width=8, textvariable=self.entry_var)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(main_actions_frame, text="Insert", command=self.insert_value, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(main_actions_frame, text="Delete", command=self.delete_value, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(main_actions_frame, text="Search", command=self.search_value, **self.button_style).pack(side=tk.LEFT, padx=3)

        # --- Generation Frame ---
        gen_frame = tk.Frame(master)
        gen_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(gen_frame, text="Random Count:").pack(side=tk.LEFT, padx=(0, 5))
        self.random_count_entry = tk.Entry(gen_frame, width=5)
        self.random_count_entry.insert(0, "10")
        self.random_count_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(gen_frame, text="Generate Random", command=self.generate_random_tree, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(gen_frame, text="Generate Balanced", command=self.on_balanced_click, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(gen_frame, text="Clear Tree", command=self.clear_tree, **self.button_style).pack(side=tk.LEFT, padx=3)

        # --- Rebalance & Traversal Frame ---
        rebalance_trav_frame = tk.Frame(master)
        rebalance_trav_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Button(rebalance_trav_frame, text="Rebalance Step", command=self.rebalance_step, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(rebalance_trav_frame, text="Rebalance All", command=self.rebalance_all, **self.button_style).pack(side=tk.LEFT, padx=3)
        
        separator1 = ttk.Separator(rebalance_trav_frame, orient='vertical')
        separator1.pack(side=tk.LEFT, padx=10, fill='y')

        tk.Button(rebalance_trav_frame, text="Inorder", command=self.show_inorder, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(rebalance_trav_frame, text="Preorder", command=self.show_preorder, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(rebalance_trav_frame, text="Postorder", command=self.show_postorder, **self.button_style).pack(side=tk.LEFT, padx=3)

        # --- Settings & Advanced Frame ---
        settings_frame = tk.Frame(master, bd=2, relief=tk.GROOVE)
        settings_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        tk.Checkbutton(settings_frame, text="Hide NIL Nodes", variable=self.hide_nil_var,
                       command=self.draw_tree).pack(side=tk.LEFT, padx=10)
        tk.Label(settings_frame, text="Zoom:").pack(side=tk.LEFT)
        tk.Scale(settings_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                 variable=self.zoom_var, command=lambda _: self.draw_tree()).pack(side=tk.LEFT, padx=5)
        tk.Label(settings_frame, text="Theme:").pack(side=tk.LEFT)
        self.theme_combo = ttk.Combobox(settings_frame, textvariable=self.theme_var,
                                        values=list(self.themes.keys()), state="readonly")
        self.theme_combo.pack(side=tk.LEFT, padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.on_theme_changed)

        manual_frame = tk.Frame(master, bd=2, relief=tk.GROOVE)
        manual_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Checkbutton(manual_frame, text="Manual Coloring Mode", variable=self.manual_coloring_var,
                       command=self._toggle_manual_coloring).pack(side=tk.LEFT, padx=10)
        tk.Button(manual_frame, text="Check RB Properties", command=self.check_rb_properties).pack(side=tk.LEFT, padx=10)
        tk.Checkbutton(manual_frame, text="Color-Only Mode", variable=self.color_only_mode,
                       command=self.toggle_color_mode).pack(side=tk.LEFT, padx=10)

        separator2 = ttk.Separator(manual_frame, orient='vertical')
        separator2.pack(side=tk.LEFT, padx=10, fill='y')
        tk.Button(manual_frame, text="Save to File", command=self.save_to_file, **self.button_style).pack(side=tk.LEFT, padx=3)
        tk.Button(manual_frame, text="Load from File", command=self.load_from_file, **self.button_style).pack(side=tk.LEFT, padx=3)

        # -------------------- LOG --------------------
        self.log_frame = tk.Frame(master)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        tk.Label(self.log_frame, text="Steps / Log:").pack(side=tk.TOP, anchor=tk.W)
        self.log_text = tk.Text(self.log_frame, height=10, width=80)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scroll = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text['yscrollcommand'] = self.log_scroll.set

        # -------------------- CANVAS --------------------
        self.canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_mouse_click)

        self.draw_tree()
        self._start_async_poll()

    # --------------------------------------------------
    #  ASYNC LOOP POLLING
    # --------------------------------------------------
    def _start_async_poll(self) -> None:
        def poll():
            try:
                loop = asyncio.get_event_loop()
                loop.stop()
                loop.run_forever()
            except RuntimeError:
                pass
            self.master.after(50, poll)
        poll()

    # --------------------------------------------------
    #  COMMANDS
    # --------------------------------------------------
    def toggle_color_mode(self) -> None:
        self.tree.color_only = self.color_only_mode.get()
        self.log(f"Switched to {'COLOR-ONLY' if self.color_only_mode.get() else 'FULL'} rebalancing mode.")

    def insert_value(self) -> None:
        val_str = self.value_entry.get()
        if not val_str.isdigit():
            messagebox.showwarning("Warning", "Please enter a valid integer.")
            return
        val = int(val_str)
        self.tree.insert(val)
        self.update_log_and_tree() # Draw the newly inserted red node
        asyncio.ensure_future(self.animate_rebalance())

    async def animate_rebalance(self) -> None:
        """Automatically performs rebalance steps with a delay for animation."""
        while self.tree.pending_nodes:
            self.tree.rebalance_step()
            self.update_log_and_tree(without_delete=True)
            await asyncio.sleep(0.5) # Animation delay

    def delete_value(self) -> None:
        val_str = self.value_entry.get()
        if not val_str.isdigit():
            messagebox.showwarning("Warning", "Please enter a valid integer.")
            return
        val = int(val_str)
        self.tree.delete(val)
        self.update_log_and_tree()

    def search_value(self) -> None:
        val_str = self.value_entry.get()
        if not val_str.isdigit():
            messagebox.showwarning("Warning", "Please enter a valid integer.")
            return
        val = int(val_str)
        self.search_path_edges.clear()
        node = self.tree.root
        prev: Optional[RedBlackTreeNode] = None
        while node != self.tree.nil:
            if node.value == val:
                if prev is not None:
                    self.search_path_edges.append((prev, node))
                self.log(f"Found node with value {val}, color={node.color}.")
                self.draw_tree(highlight=node)
                return
            else:
                if prev is not None:
                    self.search_path_edges.append((prev, node))
                prev = node
                if val < node.value:  # type: ignore
                    node = node.left
                else:
                    node = node.right
        self.log(f"Value {val} not found in the tree.")
        self.search_path_edges.clear()
        self.draw_tree()

    def rebalance_step(self) -> None:
        self.tree.rebalance_step()
        self.update_log_and_tree()

    def rebalance_all(self) -> None:
        self.tree.rebalance_all()
        self.update_log_and_tree()

    def generate_random_tree(self) -> None:
        count_str = self.random_count_entry.get()
        if not count_str.isdigit():
            messagebox.showwarning("Warning", "Please enter a valid integer for random count.")
            return
        count = int(count_str)
        if count < 1:
            messagebox.showwarning("Warning", "Random count must be >= 1.")
            return
        self.tree = RedBlackTree(color_only=self.color_only_mode.get())
        self.log_text.delete('1.0', tk.END)
        values = random.sample(range(1, 200), count)
        for v in values:
            self.tree.insert(v)
        self.log(f"Generated random tree with {count} nodes: {values}")
        self.update_log_and_tree()

    def on_balanced_click(self) -> None:
        asyncio.ensure_future(self.generate_balanced_tree())

    async def generate_balanced_tree(self) -> None:
        count_str = self.random_count_entry.get()
        if not count_str.isdigit() or int(count_str) < 1:
            messagebox.showwarning("Warning", "Please enter a valid integer >=1 for balanced count.")
            return
        count = int(count_str)
        seed = random.randint(0, 2 ** 31)
        random.seed(seed)
        values = [random.randint(1, 2 ** 10) for _ in range(count)]
        mid = sorted(values)[count // 2]
        new_tree = RedBlackTree(color_only=False)
        new_tree.insert(mid)
        values.remove(mid)
        self.tree = new_tree
        for value in values:
            self.tree.insert(value)
            self.tree.rebalance_all()
            self.update_log_and_tree(without_delete=True)
            await asyncio.sleep(0.1 / count)
        self.log(f"Generated pseudo-balanced BST of size {count} with seed {seed}.")
        self.draw_tree()

    def clear_tree(self) -> None:
        self.tree.clear()
        self.update_log_and_tree()

    def save_to_file(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        traversal = self.tree.inorder()
        values = [str(val) for (val, _) in traversal if val is not None]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(" ".join(values))
            self.log(f"Saved {len(values)} nodes to file: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def load_from_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                messagebox.showwarning("Warning", "File is empty.")
                return
            parts = content.split()
            values: List[int] = []
            for p in parts:
                if p.isdigit():
                    values.append(int(p))
                else:
                    self.log(f"Skipping non-integer token '{p}'.")
            self.tree = RedBlackTree(color_only=self.color_only_mode.get())
            self.log_text.delete('1.0', tk.END)
            for v in values:
                self.tree.insert(v)
            self.log(f"Loaded {len(values)} nodes from file: {os.path.basename(file_path)}")
            self.update_log_and_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file:\n{e}")
        finally:
            self.draw_tree()

    def show_inorder(self) -> None:
        traversal = self.tree.inorder()
        self.log(f"Inorder: {[(val, color) for (val, color) in traversal]}")

    def show_preorder(self) -> None:
        traversal = self.tree.preorder()
        self.log(f"Preorder: {[(val, color) for (val, color) in traversal]}")

    def show_postorder(self) -> None:
        traversal = self.tree.postorder()
        self.log(f"Postorder: {[(val, color) for (val, color) in traversal]}")

    # --------------------------------------------------
    #  DRAWING + THEME
    # --------------------------------------------------
    def on_theme_changed(self, event: Optional[tk.Event] = None) -> None:
        choice = self.theme_var.get()
        if choice in self.themes:
            self.current_theme = self.themes[choice]
        self.draw_tree()

    def update_log_and_tree(self, without_delete: bool = False) -> None:
        if not without_delete:
            self.log_text.delete('1.0', tk.END)
        for step in self.tree.steps:
            self.log_text.insert(tk.END, step + "\n")
        self.draw_tree()
        self.tree.steps.clear()

    def draw_tree(self, highlight: Optional[RedBlackTreeNode] = None) -> None:
        self.canvas.delete("all")
        self.node_positions.clear()
        self.canvas.config(bg=self.current_theme["bg"])
        if self.tree.root == self.tree.nil:
            return

        positions: Dict[RedBlackTreeNode, Tuple[int, int]] = {}
        self._compute_positions(self.tree.root, 0, 0, positions)
        xs = [pos[0] for pos in positions.values()]
        min_x = min(xs) if xs else 0
        max_x = max(xs) if xs else 0
        width_in_order = max_x - min_x if max_x != min_x else 1

        zoom = self.zoom_var.get()
        node_gap_x = int(60 * zoom)
        node_gap_y = int(80 * zoom)
        margin_x = 40
        margin_y = 40
        c_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 50 else 800
        total_tree_width = width_in_order * node_gap_x
        offset_x = (c_width - total_tree_width) // 2

        pixel_coords: Dict[RedBlackTreeNode, Tuple[int, int]] = {}
        for node, (x_index, depth) in positions.items():
            px = offset_x + margin_x + (x_index - min_x) * node_gap_x
            py = margin_y + depth * node_gap_y
            pixel_coords[node] = (px, py)

        def draw_node(node: RedBlackTreeNode, px: int, py: int, current_bh: int) -> None:
            if node == self.tree.nil:
                r = int(15 * zoom)
                self.canvas.create_oval(px - r, py - r, px + r, py + r, fill="black", outline="white", width=2)
                self.canvas.create_text(px, py - r + r * 40 // 15, text=f"BH={current_bh}", fill="black")
                return
            if node.left and node.left in pixel_coords:
                lx, ly = pixel_coords[node.left]
                line_color, line_width = self._edge_color(node, node.left)
                self.canvas.create_line(px, py, lx, ly, width=line_width, fill=line_color)
            if node.right and node.right in pixel_coords:
                rx, ry = pixel_coords[node.right]
                line_color, line_width = self._edge_color(node, node.right)
                self.canvas.create_line(px, py, rx, ry, width=line_width, fill=line_color)

            node_color = self.current_theme["black_node"] if node.color == "black" else self.current_theme["red_node"]
            fill_color = "blue" if node == highlight else node_color
            r = int(15 * zoom)
            self.canvas.create_oval(px - r, py - r, px + r, py + r, fill=fill_color, outline="black", width=2)
            self.canvas.create_text(px, py, text=str(node.value), fill=self.current_theme["text_color"])
            self.node_positions[node] = (px - r, py - r, px + r, py + r)

            new_bh = current_bh + (1 if node.color == "black" else 0)
            if node.left and node.left in pixel_coords:
                draw_node(node.left, pixel_coords[node.left][0], pixel_coords[node.left][1], new_bh)
            else:
                draw_node(self.tree.nil, px - node_gap_x // 2, py + node_gap_y, new_bh)
            if node.right and node.right in pixel_coords:
                draw_node(node.right, pixel_coords[node.right][0], pixel_coords[node.right][1], new_bh)
            else:
                draw_node(self.tree.nil, px + node_gap_x // 2, py + node_gap_y, new_bh)

        root_px, root_py = pixel_coords[self.tree.root]
        initial_bh = 1 if self.tree.root.color == "black" else 0
        draw_node(self.tree.root, root_px, root_py, initial_bh)

    def on_value_change(self, *args) -> None:
        self.search_path_edges.clear()
        self.draw_tree()

    def _edge_color(self, parent: RedBlackTreeNode, child: RedBlackTreeNode) -> Tuple[str, int]:
        for edge in self.search_path_edges:
            if edge == (parent, child):
                return "purple", 5
        return "black", 2

    def _compute_positions(self, node: RedBlackTreeNode, depth: int, x_index: int, positions: dict) -> int:
        if node == self.tree.nil:
            return x_index
        x_index = self._compute_positions(node.left, depth + 1, x_index, positions)
        positions[node] = (x_index, depth)
        x_index += 1
        x_index = self._compute_positions(node.right, depth + 1, x_index, positions)
        return x_index

    # --------------------------------------------------
    #  TOOLTIP
    # --------------------------------------------------
    def on_mouse_move(self, event: tk.Event) -> None:
        found_node: Optional[RedBlackTreeNode] = None
        for node, (left, top, right, bottom) in self.node_positions.items():
            if left <= event.x <= right and top <= event.y <= bottom:
                found_node = node
                break
        if found_node and found_node != self.tree.nil:
            tip = f"Value: {found_node.value}\nColor: {found_node.color}"
            self.show_tooltip(event.x + 10, event.y + 10, tip)
        else:
            self.hide_tooltip()

    def show_tooltip(self, x: int, y: int, text: str) -> None:
        if self.tooltip_label is None:
            self.tooltip_label = tk.Label(self.canvas, text=text, background="lightyellow", borderwidth=1, relief="solid")
            self.tooltip_label.place(x=x, y=y)
        else:
            self.tooltip_label.config(text=text)
            self.tooltip_label.place(x=x, y=y)

    def hide_tooltip(self) -> None:
        if self.tooltip_label:
            self.tooltip_label.destroy()
            self.tooltip_label = None

    # --------------------------------------------------
    #  UTILS
    # --------------------------------------------------
    def log(self, message: str) -> None:
        self.tree.steps.append(message)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def _toggle_manual_coloring(self) -> None:
        self.log("Manual coloring mode " + ("ENABLED" if self.manual_coloring_var.get() else "DISABLED") + ".")

    def on_mouse_click(self, event: tk.Event) -> None:
        if not self.manual_coloring_var.get():
            return
        for node, (left, top, right, bottom) in self.node_positions.items():
            if left <= event.x <= right and top <= event.y <= bottom:
                if node == self.tree.nil:
                    return
                old = node.color
                node.color = "black" if node.color == "red" else "red"
                self.log(f"Toggled node {node.value} from {old} to {node.color}.")
                self.draw_tree()
                return

    # --------------------------------------------------
    #  RB PROPERTY CHECK
    # --------------------------------------------------
    def check_rb_properties(self) -> None:
        errors: List[str] = []

        if self.tree.root != self.tree.nil and self.tree.root.color != "black":
            errors.append(f"Root node {self.tree.root.value} is not black.")
        if self.tree.nil.color != "black":
            errors.append("NIL sentinel is not black.")

        def check_red_children(node: RedBlackTreeNode) -> None:
            if node == self.tree.nil:
                return
            if node.color == "red":
                if node.left.color == "red":
                    errors.append(f"Red node {node.value} has red left child {node.left.value}.")
                if node.right.color == "red":
                    errors.append(f"Red node {node.value} has red right child {node.right.value}.")
            check_red_children(node.left)
            check_red_children(node.right)
        check_red_children(self.tree.root)

        def black_height(n: RedBlackTreeNode) -> int:
            if n == self.tree.nil:
                return 1
            left_bh = black_height(n.left)
            right_bh = black_height(n.right)
            if left_bh != right_bh or left_bh < 0:
                errors.append(f"Black-height mismatch at node {n.value}.")
                return -1
            return left_bh + (1 if n.color == "black" else 0)

        if black_height(self.tree.root) < 0:
            errors.append("Black-height inconsistent across paths.")

        if errors:
            for e in errors:
                self.log("RB Check Failed: " + e)
        else:
            self.log("RB Check Passed: All Red-Black properties satisfied.")