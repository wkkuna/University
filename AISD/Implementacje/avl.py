import pytest


def get_height(node):
    return 0 if not node else node.height


def get_parent_height(left, right):
    return max(get_height(left), get_height(right)) + 1


class Node:
    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.height = get_parent_height(left, right)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return all(
            [
                self.height == other.height,
                self.value == other.value,
                self.left == other.left,
                self.right == other.right,
            ]
        )


class AVLTree:
    def __init__(self, root: Node) -> None:
        self.root = root

    def insert(self, node: Node) -> None:
        def inner(node: Node, root: Node):
            if not root:
                return node
            elif node.value < root.value:
                root.left = inner(node, root.left)
            else:
                root.right = inner(node, root.right)

            root.height = get_parent_height(root.left, root.right)
            return self.balance(root)

        self.root = inner(node, self.root)

    def find(self, value: int) -> Node | None:
        def find_inner(node, value):
            if node is None or node.value == value:
                return node
            elif node.value > value:
                return find_inner(node.left, value)
            else:
                return find_inner(node.right, value)

        return find_inner(self.root, value)

    def successor(self, node):
        if not node or not node.left:  # leftmost node or no such found
            return node

        return self.successor(node.left)

    def delete(self, value) -> None:
        def inner(root, value):
            if not root:
                return root
            # Search for smaller elements in the left subtree
            elif value < root.value:
                root.left = inner(root.left, value)
            # Search for larger elements in the right subtree
            elif value > root.value:
                root.right = inner(root.right, value)
            # Otherwise, encountered element to be deleted
            # If any of the subtrees is empty, just move the next child upwards
            elif not root.left or not root.right:
                succ = root.right if root.right else root.left
                root = None
                return succ
            # Else, find the successor, remove it from the bottom of the tree
            # and assign in place of the deleted element
            else:
                succ = self.successor(root.right)
                root.value = succ.value
                root.right = inner(root.right, succ.value)

            # Empty upon deletion, no need to balance
            if not root:
                return root

            # Update the height
            root.height = get_parent_height(root.left, root.right)

            return self.balance(root)

        return inner(self.root, value)

    def get_balance(self, node) -> bool:
        return get_height(node.left) - get_height(node.right)

    # Move upwards to detect subtree heights that violate AVL properties
    # (the difference between them is more than 1)
    def balance(self, node: Node) -> None:
        balance = self.get_balance(node)
        if abs(balance) < 2:  # Acceptable height difference
            return node

        # Right rotation (left-heavy)
        #        z                            y
        #       / \                          / \
        #      y  T4         ---->          x   z
        #     / \                          / \  / \
        #    x   T3                       T1 T2 T3 T4
        #   / \
        #  T1  T2
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # Left rotation (right-heavy)
        #      z                              y
        #     / \                            / \
        #    T1  y          ---->           z   x
        #        / \                       / \  / \
        #       T2  x                     T1 T2 T3 T4
        #          / \
        #         T3  T4
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # Left-right rotation (left-heavy on right subtree)
        #      z                       z                    y
        #     / \                     / \                  / \
        #    x   T4     ---->        y   T4    ---->      x   z
        #   / \                     / \                  / \  / \
        #  T1  y                   x   T3               T1 T2 T3 T4
        #      / \                / \
        #     T2  T3             T1 T2
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right-left rotation (right-heavy on left subtree)
        #        z                z                       y
        #       / \              / \                     / \
        #      T1  x     ---->  T1  y        ---->     z   x
        #          / \              / \               / \  / \
        #         y  T4            T2  x             T1 T2 T3 T4
        #        / \                  / \
        #       T2  T3               T3  T4
        #
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

    def rotate_left(self, node: Node) -> None:
        new_top = node.right
        assert new_top is not None, "Requested to rotate non to the internal node"

        lost_child = new_top.left
        new_top.left = node

        # Set 'lost_child` as the right child of the pre-rotation top node
        new_top.left.right = lost_child

        # Calculate new height for left subtree
        new_top.left.height = get_parent_height(new_top.left.left, new_top.left.right)
        # Calculate new height for the top node
        new_top.height = get_parent_height(new_top.left, new_top.right)
        # The right subtree's height doesn't require any alterations
        return new_top

    def rotate_right(self, node: Node) -> None:
        new_top = node.left
        assert new_top is not None, "Requested to rotate non to the internal node"

        lost_child = new_top.right
        new_top.right = node

        # Set 'lost_child` as the left child of the pre-rotation top node
        new_top.right.left = lost_child

        # Calculate the new height for the right subtree
        new_top.right.height = get_parent_height(new_top.right.left, new_top.right.right)
        # Calculate the new height for the top node
        new_top.height = get_parent_height(new_top.left, new_top.right)
        # The left subtree's height doesn't require any alterations
        return new_top


def get_tree_lines(root, curr_index=0, index=False, delimiter="-"):
    if root is None:
        return [], 0, 0, 0

    line1, line2 = [], []
    node_repr = f"{root.value}" if not index else f"{curr_index}{delimiter}{root.value}"

    new_root_w = gap_size = len(node_repr)

    lbox, lbox_w, lroot_start, lroot_end = get_tree_lines(root.left, 2 * curr_index + 1, index, delimiter)
    rbox, rbox_w, rroot_start, rroot_end = get_tree_lines(root.right, 2 * curr_index + 2, index, delimiter)

    if lbox_w > 0:
        l_root = (lroot_start + lroot_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (lbox_w - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (lbox_w - l_root))
        new_root_start = lbox_w + 1
        gap_size += 1
    else:
        new_root_start = 0

    line1.append(node_repr)
    line2.append(" " * new_root_w)

    if rbox_w > 0:
        r_root = (rroot_start + rroot_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (rbox_w - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (rbox_w - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_w - 1

    new_box = ["".join(line1), "".join(line2)]
    for i in range(max(len(lbox), len(rbox))):
        l_line = lbox[i] if i < len(lbox) else " " * lbox_w
        r_line = rbox[i] if i < len(rbox) else " " * rbox_w
        new_box.append(l_line + " " * gap_size + r_line)

    return new_box, len(new_box[0]), new_root_start, new_root_end


def print_tree(root):
    lines, *_ = get_tree_lines(root)
    for line in lines:
        print(line)


def check_if_avl_valid(avl: AVLTree):
    def check_tree_balance(node):
        assert abs(avl.get_balance(node)) <= 1

        avl.get_balance(node.left)
        avl.get_balance(node.right)

    check_tree_balance(avl.root)


@pytest.fixture()
def avl():
    root = Node(1)
    tree = AVLTree(root)
    nodes = [2, 3, 4, 5, 6]
    for node_value in nodes:
        new_node = Node(node_value)
        tree.insert(new_node)
    return tree


def test_avl_init(avl):
    assert avl.root is not None


def test_avl_insert(avl):
    value = 7
    old_height = avl.root.height
    avl.insert(Node(value))
    assert avl.find(value) is not None
    assert avl.root.height == old_height + 1 or avl.root.height == old_height


def test_avl_deletion(avl):
    value = 6
    old_height = avl.root.height
    avl.delete(value)
    assert avl.find(value) is None
    assert avl.root.height <= old_height


def test_avl_balance(avl):
    check_if_avl_valid(avl)


def test_avl_single_node():
    root = Node(1)
    avl = AVLTree(root)
    assert avl.find(1).value == 1
    assert avl.find(2) is None


def test_avl_empty():
    root = None
    avl = AVLTree(root)
    assert avl.find(1) is None


tree = AVLTree(Node(0))
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for e in arr:
    tree.insert(Node(e))
print_tree(tree.root)
tree.delete(3)
print_tree(tree.root)
