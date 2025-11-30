#GUI
from tkinter import *
from tkinter import messagebox
import random

class BSTVisualizer:
    def __init__(self, root):

        #button style constants
        BUTTON_WIDTH = 10
        BUTTON_HEIGHT = 1
        BUTTON_FONT = ("Arial", 12, "bold")
        BUTTON_BG = "black"
        BUTTON_FG = "#F0F8FF"
        BUTTON_BD = 8
        BUTTON_RELIEF = RAISED

        self.window = root
        self.window.title("Binary Search Tree Visualizer")
        self.window.geometry("1350x720")
        self.window.config(bg="light blue")

        #Frame for canvas and scrollbars
        #Main frame
        self.frame = Frame(self.window, bd=4, relief=RAISED)
        self.frame.place(x=0, y=0, width=1160, height=520)

        #Interior frame to hold canvas and scrollbars
        inner = Frame(self.frame)
        inner.pack(fill=BOTH, expand=True)

        #Canvas
        self.canvas = Canvas(inner, bg="mint cream")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        #Scrollbars
        self.v_scroll = Scrollbar(inner, orient=VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=RIGHT, fill=Y)

        self.h_scroll = Scrollbar(self.frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=BOTTOM, fill=X)

        #Bind scrollbars to canvas
        self.canvas.configure(yscrollcommand=self.v_scroll.set,
                            xscrollcommand=self.h_scroll.set)

        #Auto update scrollregion after drawing
        def update_scrollregion(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        #Result canvas
        self.result_canvas = Canvas(self.window, width=1340, height=168,
                                    bg="#2F4156", bd=4, relief=RAISED)
        self.result_canvas.place(x=0, y=540)

        self.status_label = Label(self.result_canvas, bg="#2F4156", fg="black",
                                  text="BST Algorithm",
                                  font=("Times New Roman", 20, "bold", "italic"))
        self.status_label.place(x=530, y=130)

        self.traversal_label = Label(self.result_canvas, bg="#2F4156", fg="black",
                                     text="Traversal Result",
                                     font=("Times New Roman", 15, "bold", "italic"))
        self.traversal_label.place(x=530, y=10)

        #Traversal output labels
        self.value_show = []
        pos = 8
        for i in range(15):
            lbl = Label(self.result_canvas, bg="white", fg="black",
                        text=" ", width=4, height=1,
                        font=("Arial", 15, "bold", "italic"),
                        relief=SUNKEN, bd=5)
            lbl.place(x=pos, y=50)
            self.value_show.append(lbl)
            pos += 91

        #Root of BST
        self.root_node = None

        #Node input
        self.input_entry = Entry(self.window, fg="black", bg="white", width=5,
                                 font=("Arial", 12, "bold"))
        self.input_entry.place(x=1210, y=60)

        #Buttons
        self.insert_btn = Button(self.window, text="Insert",
                         font=BUTTON_FONT, bg=BUTTON_BG,
                         fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
                         width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                         command=self.insert_node)
        self.insert_btn.place(x=1180, y=90)

        self.delete_btn = Button(self.window, text="Delete Node",
                                font=BUTTON_FONT, bg=BUTTON_BG,
                                fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
                                width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                command=self.delete_node)
        self.delete_btn.place(x=1180, y=470)

        Button(self.window, text="Pre-Order", font=BUTTON_FONT, bg=BUTTON_BG,
            fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=lambda: self.traverse("pre")).place(x=1180, y=170)

        Button(self.window, text="In-Order", font=BUTTON_FONT, bg=BUTTON_BG,
            fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=lambda: self.traverse("in")).place(x=1180, y=220)

        Button(self.window, text="Post-Order", font=BUTTON_FONT, bg=BUTTON_BG,
            fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=lambda: self.traverse("post")).place(x=1180, y=270)

        Button(self.window, text="Level-Order", font=BUTTON_FONT, bg=BUTTON_BG,
            fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=lambda: self.traverse("level")).place(x=1180, y=320)
        
        self.random_btn = Button(self.window, text="Random Tree",
                         font=BUTTON_FONT, bg=BUTTON_BG,
                         fg=BUTTON_FG, bd=BUTTON_BD, relief=BUTTON_RELIEF,
                         width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                         command=self.create_random_tree)
        self.random_btn.place(x=1180, y=415) 


        #layout
        self._inorder_counter = 0
        self.h_gap = 120      
        self.v_gap = 120       
        self.canvas_center_x = 580  

    #Node structure
    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
            self.oval = None
            self.text = None
            self.x = 0
            self.y = 0

    #tree height
    def get_height(self, node):
        if not node:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    #insertion
    def insert_node(self):
        val = self.input_entry.get()
        if not val.isdigit():
            messagebox.showerror("Input Error!", "Please enter an integer!")
            return

        val = int(val)
        self.input_entry.delete(0, END)

        if self.root_node is None:
            self.root_node = self.Node(val)
        else:
            self._insert(self.root_node, val)

        #Compute positions and redraw tree
        self.layout_and_draw()

    def _insert(self, node, val):
        if val == node.value:
            messagebox.showerror("Duplicate!", "Duplicated values is not allowed!")
            return

        if val < node.value:
            if node.left is None:
                node.left = self.Node(val)
            else:
                self._insert(node.left, val)
        else:
            if node.right is None:
                node.right = self.Node(val)
            else:
                self._insert(node.right, val)

    #In-order layout
    def layout_and_draw(self):
        #Clear canvas items
        self.canvas.delete("all")
        #Reset inorder counter
        self._inorder_counter = 0

        #Assigns x positions (in-order) and y positions by depth
        self._assign_positions(self.root_node, depth=1)

        #Center the layout around desired center x
        if self.root_node:
            #Finds min and max x
            xs = []
            def collect_x(n):
                if not n: return
                xs.append(n.x)
                collect_x(n.left)
                collect_x(n.right)
            collect_x(self.root_node)
            if xs:
                min_x, max_x = min(xs), max(xs)
                current_center = (min_x + max_x) / 2
                shift = self.canvas_center_x - current_center
                if abs(shift) > 0.1:
                    self._shift_tree(self.root_node, shift)

        #Draw nodes and lines
        self._draw_all(self.root_node)

        #Update scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _assign_positions(self, node, depth):
        #docstring 
        """In-order traversal that assigns x positions based on inorder index
           and y positions based on depth. This keeps the tree compact and
           preserves BST ordering horizontally."""
        if not node:
            return
        #left
        self._assign_positions(node.left, depth + 1)

        #Assign x based on inorder counter
        x = (self._inorder_counter + 1) * self.h_gap
        y = 50 + (depth - 1) * self.v_gap
        node.x = x
        node.y = y
        self._inorder_counter += 1

        #Right
        self._assign_positions(node.right, depth + 1)

    def _shift_tree(self, node, shift):
        if not node:
            return
        node.x += shift
        self._shift_tree(node.left, shift)
        self._shift_tree(node.right, shift)

    #Tree drawing
    def _draw_all(self, node):
        if not node:
            return
        #Draw left subtree first
        if node.left:
            self._draw_all(node.left)
            self.draw_line(node, node.left)
        if node.right:
            self._draw_all(node.right)
            self.draw_line(node, node.right)
        #Draw node itself
        self.draw_node(node)

    def draw_node(self, node):
        r = 25
        node.oval = self.canvas.create_oval(node.x - r, node.y - r,
                                            node.x + r, node.y + r,
                                            fill="green", outline="yellow", width=2)
        node.text = self.canvas.create_text(node.x, node.y,
                                            text=str(node.value),
                                            fill="yellow",
                                            font=("Arial", 12, "bold"))

    def draw_line(self, parent, child):
        #Draws line from parent to child
        self.canvas.create_line(parent.x, parent.y + 25,
                                child.x, child.y - 25,
                                width=3, fill="red4")

    #Transversals
    def traverse(self, order):
        for lbl in self.value_show:
            lbl.config(text=" ")

        self._counter = 0

        if not self.root_node:
            messagebox.showinfo("Empty Tree!", "BST is empty!")
            return

        if order == "pre":
            self._pre_order(self.root_node)
        elif order == "in":
            self._in_order(self.root_node)
        elif order == "post":
            self._post_order(self.root_node)
        elif order == "level":
            self._level_order()

    def _pre_order(self, node):
        if node:
            self.value_show[self._counter].config(text=node.value)
            self._counter += 1
            self._pre_order(node.left)
            self._pre_order(node.right)

    def _in_order(self, node):
        if node:
            self._in_order(node.left)
            self.value_show[self._counter].config(text=node.value)
            self._counter += 1
            self._in_order(node.right)

    def _post_order(self, node):
        if node:
            self._post_order(node.left)
            self._post_order(node.right)
            self.value_show[self._counter].config(text=node.value)
            self._counter += 1

    def _level_order(self):
        queue = [self.root_node]
        while queue:
            node = queue.pop(0)
            self.value_show[self._counter].config(text=node.value)
            self._counter += 1
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    #Delete and redraw
    def delete_node(self):
        val = self.input_entry.get()
        if not val.isdigit():
            messagebox.showerror("Input Error", "Enter integer")
            return

        val = int(val)
        self.input_entry.delete(0, END)

        self.root_node = self._delete(self.root_node, val)
        #Recomputes positions and redraw
        self.layout_and_draw()

    def _delete(self, node, val):
        if node is None:
            messagebox.showinfo("Not Found", f"{val} not found")
            return None

        if val < node.value:
            node.left = self._delete(node.left, val)
        elif val > node.value:
            node.right = self._delete(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = self._min_value_node(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        return node

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node
    
    def create_random_tree(self):
        #Clear existing tree
        self.root_node = None

        #Generate a list of random integers
        values = random.sample(range(1, 101), 10)  #Avoids duplicates automatically

        #Insert all values into the BST
        for val in values:
            self._insert_random(self.root_node, val) if self.root_node else self._set_root(val)

        #Redraw the tree
        self.layout_and_draw()

    #Sets root if tree is empty
    def _set_root(self, val):
        self.root_node = self.Node(val)

    #Recursive insert method that avoids duplicate messages
    def _insert_random(self, node, val):
        if val == node.value:
            return
        if val < node.value:
            if node.left is None:
                node.left = self.Node(val)
            else:
                self._insert_random(node.left, val)
        else:
            if node.right is None:
                node.right = self.Node(val)
            else:
                self._insert_random(node.right, val)

if __name__ == "__main__":
    window = Tk()
    bst_app = BSTVisualizer(window)
    window.mainloop()
