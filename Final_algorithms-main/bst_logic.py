#BINARY SEARCH TREE LOGIC

class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.notation_index = 0


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.nodes = []

    def insert(self, value):
        if self.root is None:
            self.root = BSTNode(value)
            self.root.notation_index = 1
            self.nodes = [self.root]
            return True

        return self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value == node.value:
            return False  #No duplicates

        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
                node.left.notation_index = node.notation_index * 2
                self.nodes.append(node.left)
                return True
            else:
                return self._insert_recursive(node.left, value)

        else:
            if node.right is None:
                node.right = BSTNode(value)
                node.right.notation_index = node.notation_index * 2 + 1
                self.nodes.append(node.right)
                return True
            else:
                return self._insert_recursive(node.right, value)

    def delete(self, value):
        if self.root is None:
            return False

        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted:
            self._update_nodes_list()
        return deleted

    def _delete_recursive(self, node, value):
        if node is None:
            return node, False

        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)

        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)

        else:
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                min_node = self._find_min(node.right)
                node.value = min_node.value
                node.right, _ = self._delete_recursive(node.right, min_node.value)
                return node, True

        return node, False

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _update_nodes_list(self):
        self.nodes = []
        if self.root:
            self._collect_nodes(self.root)

    def _collect_nodes(self, node):
        if node:
            self.nodes.append(node)
            self._collect_nodes(node.left)
            self._collect_nodes(node.right)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def pre_order_traversal(self):
        result = []
        self._pre_order_recursive(self.root, result)
        return result

    def _pre_order_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._pre_order_recursive(node.left, result)
            self._pre_order_recursive(node.right, result)

    def in_order_traversal(self):
        result = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, node, result):
        if node:
            self._in_order_recursive(node.left, result)
            result.append(node.value)
            self._in_order_recursive(node.right, result)

    def post_order_traversal(self):
        result = []
        self._post_order_recursive(self.root, result)
        return result

    def _post_order_recursive(self, node, result):
        if node:
            self._post_order_recursive(node.left, result)
            self._post_order_recursive(node.right, result)
            result.append(node.value)

    def level_order_traversal(self):
        if not self.root:
            return []

        result = []
        queue = [self.root]

        while queue:
            node = queue.pop(0)
            result.append(node.value)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def is_empty(self):
        return self.root is None

    def get_height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return 0

        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)

        return max(left_height, right_height) + 1
