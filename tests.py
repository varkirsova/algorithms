from binaryTree import BinaryTree, AVLTree, RBTree

import random
import math
import matplotlib.pyplot as plt
import numpy as np


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def experiment(tree_class, values):
    tree = tree_class()
    heights = []
    for v in values:
        tree.insert(v)
        heights.append(height(tree.root))
    return heights


def log2(n):  # теоретический минимум - нижняя граница любых двоичных деревьев
    return math.log2(n) if n > 0 else 0


def bst_expect(n):  # ожидаемая высота асимптотически равна 4.311·ln(n) (по Риду)
    return 4.311 * math.log(n)


def avl_upper(n):  # верхняя граница для АВЛ дерева из теории
    return 1.44 * log2(n)


def rb_upper(n):  # верхняя граница для КЧ дерева из теории
    return 2 * log2(n)


def draw_graph(x, heights, title, bound_func=None, is_bst=False):
    plt.figure(figsize=(8, 5))

    plt.plot(x, heights, 'r-', linewidth=2, label="h(n)")

    plt.plot(x, [log2(n) for n in x], 'g--', label="нижняя граница (log2(n))")

    if bound_func:
        if is_bst:
            plt.plot(x, [bound_func(n) for n in x], 'b--',
                     label="ожидаемая высота")
        else:
            plt.plot(x, [bound_func(n) for n in x], 'b--',
                     label="верхняя граница")

    plt.xlabel("количество ключей, n")
    plt.ylabel("высота дерева, h")
    plt.title(title)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def estimate_log_constant_simple(ns, heights, log_base='e'):
    ns = np.array(ns)
    heights = np.array(heights)
    valid = ns > 0
    ns, heights = ns[valid], heights[valid]

    if log_base == 'e':
        log_ns = np.log(ns)
        theory_var = "ln(n)"
    else:
        log_ns = np.log2(ns)
        theory_var = "log2(n)"

    n = len(log_ns)
    sum_x = np.sum(log_ns)
    sum_y = np.sum(heights)
    sum_xy = np.sum(log_ns * heights)
    sum_x2 = np.sum(log_ns ** 2)

    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - a * sum_x) / n

    return a, b, theory_var


def run_all_experiments():
    n = 10000
    step = 200
    X = list(range(step, n + 1, step))

    rand_values = random.sample(range(1, n * 10), n)

    # bst на случайных ключах
    print("\n1 Бинарное дерево поиска на случайных ключах")
    print("ожидаемая высота: ~4.311 ln(n)")
    print("верхняя граница: n")
    print("нижняя граница: log2(n)")

    heights_bst = experiment(BinaryTree, rand_values)
    draw_graph(X, heights_bst[step - 1::step],
               "высота BST (случайные ключи)", bst_expect, is_bst=True)

    c, b, var = estimate_log_constant_simple(X, heights_bst[step - 1::step], log_base='e')
    print(f"по графику: h(n) ~ {c:.2f} {var} + {b:.2f}")
    print(f"из теории: h(n) ~ 4.311 ln(n)")

    # avl на случайных ключах
    print("\n2 АВЛ дерево на случайных ключах")
    print("верхняя граница: ≤ 1.44 log2(n)")
    print("нижняя граница: log2(n)")

    heights_avl = experiment(AVLTree, rand_values)
    draw_graph(X, heights_avl[step - 1::step],
               "высота АВЛ дерева (случайные ключи)", avl_upper)

    c, b, var = estimate_log_constant_simple(X, heights_avl[step - 1::step], log_base='2')
    print(f"по графику: h(n) ~ {c:.2f} {var} + {b:.2f}")
    print(f"из теории: h(n) ≤ 1.44 log2(n)")

    # rb на случайных ключах
    print("\n3 Красно черное дерево на случайных ключах")
    print("верхняя граница: ≤ 2.00 log2(n)")
    print("нижняя граница: log2(n)")

    heights_rb = experiment(RBTree, rand_values)
    draw_graph(X, heights_rb[step - 1::step],
               "высота КЧ дерева (случайные ключи)", rb_upper)

    c, b, var = estimate_log_constant_simple(X, heights_rb[step - 1::step], log_base='2')
    print(f"по графику: h(n) ~ {c:.2f} {var} + {b:.2f}")
    print(f"из теории: h(n) ≤ 2.00 log2(n)")

    sorted_values = list(range(1, n + 1))

    # avl на отсортированных ключах
    print("\n4 АВЛ дерево на отсортированных ключах")
    print("верхняя граница: ≤ 1.44 log2(n) (гарантируется)")
    print("нижняя граница: log2(n)")

    heights_avl_sorted = experiment(AVLTree, sorted_values)
    draw_graph(X, heights_avl_sorted[step - 1::step],
               "высота АВЛ дерева (отсортированные ключи)", avl_upper)

    c, b, var = estimate_log_constant_simple(X, heights_avl_sorted[step - 1::step], log_base='2')
    print(f"по графику: h(n) ~ {c:.2f} {var} + {b:.2f}")
    print(f"из теории: h(n) ≤ 1.44 log2(n)")

    # rb на отсортированных ключах
    print("\n5 Красно черное дерево на отсортированных ключах")
    print("верхняя граница: ≤ 2.00 log2(n)")
    print("нижняя граница: log2(n)")

    heights_rb_sorted = experiment(RBTree, sorted_values)
    draw_graph(X, heights_rb_sorted[step - 1::step],
               "высота КЧ дерева (отсортированные ключи)", rb_upper)

    c, b, var = estimate_log_constant_simple(X, heights_rb_sorted[step - 1::step], log_base='2')
    print(f"по графику: h(n) ~ {c:.2f} {var} + {b:.2f}")
    print(f"из теории: h(n) ≤ 2.00 log2(n)")

run_all_experiments()