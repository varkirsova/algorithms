class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    # поиск
    def search(self, value):
        node = self.root
        while node:
            if value == node.value:
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return None

    # вставка
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        node = self.root
        parent = None

        while node:
            parent = node
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right
            else:
                return  # уже существующее не добавляем

        if value < parent.value:
            parent.left = Node(value)
        else:
            parent.right = Node(value)

    #удаление
    def delete(self, value):
        node = self.root
        parent = None

        while node and node.value != value:
            parent = node
            if value < node.value:
                node = node.left
            else:
                node = node.right

        if node is None:
            return

        # нет потомков
        if node.left is None and node.right is None:
            if parent is None:
                self.root = None
            elif parent.left == node:
                parent.left = None
            else:
                parent.right = None

        # один потомок
        elif node.left is None or node.right is None:
            if node.left:
                child = node.left
            else:
                child = node.right

            if parent is None:
                self.root = child
            elif parent.left == node:
                parent.left = child
            else:
                parent.right = child

        # два потомка
        else:
            successor_parent = node
            successor = node.right

            while successor.left:
                successor_parent = successor
                successor = successor.left

            node.value = successor.value

            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right

    # поиск минимума
    def find_min(self):
        if self.root is None:
            return None

        node = self.root
        while node.left:
            node = node.left
        return node.value

    # поиск максимума
    def find_max(self):
        if self.root is None:
            return None

        node = self.root
        while node.right:
            node = node.right
        return node.value

    # прямой обход(корень, левое поддерево, правое поддерево)
    def pre_order(self):
        self._pre_order(self.root)

    def _pre_order(self, node):
        if node:
            print(node.value)
            self._pre_order(node.left)
            self._pre_order(node.right)


    # центрированный обход(левое поддерево, корень, правое поддерево)
    def in_order(self):
        self._in_order(self.root)

    def _in_order(self, node):
        if node:
            self._pre_order(node.left)
            print(node.value)
            self._pre_order(node.right)

    # обратный обход(левое поддерево, правое поддерево, корень)
    def post_order(self):
        self._post_order(self.root)

    def _post_order(self, node):
        if node:
            self._pre_order(node.left)
            self._pre_order(node.right)
            print(node.value)

    # обход в ширину
    def breadth_search(self):
        return self._breadth_search(self.root)

    def _breadth_search(self, node):
        res = []
        if node is None:
            return res
        queue = [node]

        while queue:
            cur = queue.pop(0)
            res.append(cur.value)
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)

        return res