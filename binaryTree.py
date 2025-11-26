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
