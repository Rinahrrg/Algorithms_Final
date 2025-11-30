# rbt_logic.py  –  pure Red-Black-Tree algorithms (no GUI)

from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class RedBlackTreeNode:
    def __init__(self, value: Optional[int], color: str = "red") -> None:
        self.value: Optional[int] = value
        self.color: str = color
        self.left: Optional[RedBlackTreeNode] = None
        self.right: Optional[RedBlackTreeNode] = None
        self.parent: Optional[RedBlackTreeNode] = None


class RedBlackTree:
    def __init__(self, color_only: bool = False) -> None:
        self.nil = RedBlackTreeNode(None, color="black")
        self.root: RedBlackTreeNode = self.nil
        self.steps: List[str] = []
        self.pending_nodes: List[RedBlackTreeNode] = []
        self.color_only: bool = color_only

    # --------------------------------------------------
    #  INSERTION
    # --------------------------------------------------
    def insert(self, value: int) -> None:
        if self.search_value(value) is not None:
            self.steps.append(f"Value {value} already exists, skipping.")
            return
        new_node = RedBlackTreeNode(value)
        new_node.left = self.nil
        new_node.right = self.nil
        self._bst_insert(new_node)
        self.steps.append(f"Inserted node {value} (red).")
        self.pending_nodes.append(new_node)

    def _bst_insert(self, node: RedBlackTreeNode) -> None:
        parent = None
        curr = self.root
        while curr != self.nil:
            parent = curr
            if node.value < curr.value:  # type: ignore
                curr = curr.left
            else:
                curr = curr.right
        node.parent = parent
        if parent is None:
            self.root = node
            self.root.color = "black"
            return
        if node.value < parent.value:  # type: ignore
            parent.left = node
        else:
            parent.right = node

    def rebalance_step(self) -> None:
        if not self.pending_nodes:
            self.steps.append("No pending nodes to rebalance.")
            return
        node = self.pending_nodes.pop(0)
        if self.color_only:
            self.insert_rebalance_color_only(node)
        else:
            self.insert_rebalance_full(node)

    def rebalance_all(self) -> None:
        while self.pending_nodes:
            self.rebalance_step()

    def insert_rebalance_full(self, node: RedBlackTreeNode) -> None:
        while node.parent is not None and node.parent.color == "red":
            grandparent = node.parent.parent
            if grandparent is None:
                break
            if node.parent == grandparent.left:
                uncle = grandparent.right
                if uncle and uncle.color == "red":
                    self.steps.append("Recoloring parent, uncle, and grandparent.")
                    node.parent.color = "black"
                    uncle.color = "black"
                    grandparent.color = "red"
                    node = grandparent
                else:
                    if node == node.parent.right:
                        self._rotate_left(node.parent)
                        node = node.parent
                    if node.parent:
                        node.parent.color = "black"
                    grandparent.color = "red"
                    self._rotate_right(grandparent)
            else:
                uncle = grandparent.left
                if uncle and uncle.color == "red":
                    self.steps.append("Recoloring parent, uncle, and grandparent.")
                    node.parent.color = "black"
                    uncle.color = "black"
                    grandparent.color = "red"
                    node = grandparent
                else:
                    if node == node.parent.left:
                        self._rotate_right(node.parent)
                        node = node.parent
                    if node.parent:
                        node.parent.color = "black"
                    grandparent.color = "red"
                    self._rotate_left(grandparent)
        if self.root:
            self.root.color = "black"

    def insert_rebalance_color_only(self, node: RedBlackTreeNode) -> None:
        while node != self.root and node.parent is not None and node.parent.color == "red":
            if node.parent.parent is None:
                break
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
            else:
                uncle = node.parent.parent.left
            if uncle.color == "red":
                self.steps.append("Recoloring parent, uncle, and grandparent (color-only).")
                node.parent.color = "black"
                uncle.color = "black"
                node.parent.parent.color = "red"
                node = node.parent.parent
            else:
                self.steps.append("Parent red, uncle black -> skipping rotation (color-only).")
                break
        self.root.color = "black"

    # --------------------------------------------------
    #  ROTATIONS
    # --------------------------------------------------
    def _rotate_left(self, node: RedBlackTreeNode) -> None:
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.nil:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child
        self.steps.append(f"Left rotation at node {node.value}.")

    def _rotate_right(self, node: RedBlackTreeNode) -> None:
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.nil:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child
        self.steps.append(f"Right rotation at node {node.value}.")

    # --------------------------------------------------
    #  DELETION
    # --------------------------------------------------
    def delete(self, value: int) -> None:
        node_to_delete = self.search_value(value)
        if node_to_delete is None:
            self.steps.append(f"Value {value} not found for deletion.")
            return
        self._delete_node(node_to_delete)

    def _delete_node(self, z: RedBlackTreeNode) -> None:
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        self.steps.append(f"Deleted node {z.value}.")
        if y_original_color == "black":
            self._delete_fixup(x)

    def _tree_minimum(self, node: RedBlackTreeNode) -> RedBlackTreeNode:
        while node.left != self.nil:
            node = node.left
        return node

    def _rb_transplant(self, u: RedBlackTreeNode, v: RedBlackTreeNode) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_fixup(self, x: RedBlackTreeNode) -> None:
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == "red":
                    sibling.color = "black"
                    x.parent.color = "red"
                    self._rotate_left(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == "black" and sibling.right.color == "black":
                    sibling.color = "red"
                    x = x.parent
                else:
                    if sibling.right.color == "black":
                        sibling.left.color = "black"
                        sibling.color = "red"
                        self._rotate_right(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = "black"
                    sibling.right.color = "black"
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == "red":
                    sibling.color = "black"
                    x.parent.color = "red"
                    self._rotate_right(x.parent)
                    sibling = x.parent.left
                if sibling.right.color == "black" and sibling.left.color == "black":
                    sibling.color = "red"
                    x = x.parent
                else:
                    if sibling.left.color == "black":
                        sibling.right.color = "black"
                        sibling.color = "red"
                        self._rotate_left(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = "black"
                    sibling.left.color = "black"
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = "black"

    # --------------------------------------------------
    #  SEARCH
    # --------------------------------------------------
    def search_value(self, value: int) -> Optional[RedBlackTreeNode]:
        curr = self.root
        while curr != self.nil:
            if curr.value == value:
                return curr
            elif value < curr.value:  # type: ignore
                curr = curr.left
            else:
                curr = curr.right
        return None

    # --------------------------------------------------
    #  TRAVERSALS
    # --------------------------------------------------
    def inorder(self, node: Optional[RedBlackTreeNode] = None,
                result: Optional[List[Tuple[int, str]]] = None) -> List[Tuple[int, str]]:
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node != self.nil:
            self.inorder(node.left, result)
            if node.value is not None:
                result.append((node.value, node.color))
            self.inorder(node.right, result)
        return result

    def preorder(self, node: Optional[RedBlackTreeNode] = None,
                 result: Optional[List[Tuple[int, str]]] = None) -> List[Tuple[int, str]]:
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node != self.nil:
            if node.value is not None:
                result.append((node.value, node.color))
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result

    def postorder(self, node: Optional[RedBlackTreeNode] = None,
                  result: Optional[List[Tuple[int, str]]] = None) -> List[Tuple[int, str]]:
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node != self.nil:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            if node.value is not None:
                result.append((node.value, node.color))
        return result

    def clear(self) -> None:
        self.root = self.nil
        self.pending_nodes.clear()
        self.steps.append("Cleared the entire tree.")