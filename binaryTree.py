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
