class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class NodeAVL:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class NodeRB:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = 'R'

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
            self._in_order(node.left)
            print(node.value)
            self._in_order(node.right)

    # обратный обход(левое поддерево, правое поддерево, корень)
    def post_order(self):
        self._post_order(self.root)

    def _post_order(self, node):
        if node:
            self._post_order(node.left)
            self._post_order(node.right)
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

# класс АВЛ дерева со всеми функциями из BST,только вставка и удаление свои
class AVLTree(BinaryTree):
    def __init__(self):
        super().__init__()

    # доп функции (получение и обновление высоты, получения баланса, левый и правый поворот)
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def new_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def small_left_rotate(self, old_root):
        new_root = old_root.right
        subtree_between = new_root.left

        new_root.left = old_root
        old_root.right = subtree_between

        self.new_height(old_root)
        self.new_height(new_root)

        return new_root

    def small_right_rotate(self, old_root):
        new_root = old_root.left
        subtree_between = new_root.right

        new_root.right = old_root
        old_root.left = subtree_between

        self.new_height(old_root)
        self.new_height(new_root)

        return new_root

    # вставка AVL
    def insert(self, value):
        self.root = self._insertAVL(self.root, value)

    def _insertAVL(self, node, value):
        if node is None:
            return NodeAVL(value)
        if value < node.value:
            node.left = self._insertAVL(node.left, value)
        elif value > node.value:
            node.right = self._insertAVL(node.right, value)
        else:
            return node

        self.new_height(node)
        balance = self.get_balance(node)

        # малый левый
        if balance < -1 and value > node.right.value:
            return self.small_left_rotate(node)

        # малый правый
        if balance > 1 and value < node.left.value:
            return self.small_right_rotate(node)

        # большой левый
        if balance < -1 and value < node.right.value:
            node.right = self.small_right_rotate(node.right)
            return self.small_left_rotate(node)

        # бошльшой правый
        if balance > 1 and value > node.left.value:
            node.left = self.small_left_rotate(node.left)
            return self.small_right_rotate(node)

        return node

    # удаление AVL
    def delete(self, value):
        self.root = self._deleteAVL(self.root, value)

    def _deleteAVL(self, node, value):
        if node is None:
            return node
        if value < node.value:
            node.left = self._deleteAVL(node.left, value)
        elif value > node.value:
            node.right = self._deleteAVL(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            successor = node.right
            while successor.left:
                successor = successor.left
            node.value = successor.value
            node.right = self._deleteAVL(node.right, successor.value)

        if node is None:
            return node

        self.new_height(node)
        balance = self.get_balance(node)

        # малый левый
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.small_left_rotate(node)

        # малый правый
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.small_right_rotate(node)

        # большой левый
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.small_right_rotate(node.right)
            return self.small_left_rotate(node)

        # большой правый
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.small_left_rotate(node.left)
            return self.small_right_rotate(node)

        return node

class RBTree(BinaryTree):
    def __init__(self):
        super().__init__()

    def is_black(self, node):
        return node is None or node.colour == 'B'

    def is_red(self, node):
        return node is not None and node.colour == 'R'

    def small_left_rotate(self, old_root):
        new_root = old_root.right
        subtree_between = new_root.left
        old_root.right = subtree_between
        if subtree_between:
            subtree_between.parent = old_root

        new_root.parent = old_root.parent
        if old_root.parent is None:
            self.root = new_root
        elif old_root == old_root.parent.left:
            old_root.parent.left = new_root
        else:
            old_root.parent.right = new_root
        new_root.left = old_root
        old_root.parent = new_root

    def small_right_rotate(self, old_root):
        new_root = old_root.left
        subtree_between = new_root.right
        old_root.left = subtree_between
        if subtree_between:
            subtree_between.parent = old_root

        new_root.parent = old_root.parent
        if old_root.parent is None:
            self.root = new_root
        elif old_root == old_root.parent.right:
            old_root.parent.right = new_root
        else:
            old_root.parent.left = new_root

        new_root.right = old_root
        old_root.parent = new_root

    # вставка red-black
    def insert(self, value):



