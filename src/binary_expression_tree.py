# Student ID: 52199280

# README File is located in same directory as this app called README.md - Please read it before executing this program.

import pickle
import os.path
import unittest

#~~~~~~ Constants ~~~~~~#
OPERATORS = "+-*x/"
#~~~~~~~~~~~~~~~~~~~~~~~#

# Modified, Goodrich at https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988
# Removed the Position class and some other irrelevant dead code.
class Tree:
    """Abstract base class representing a tree structure."""

    # ---------- abstract methods that concrete subclass must support ----------
    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))


# Modified, Goodrich at https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988
# Remove unutilized methods
class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""

    # --------------------- additional abstract methods ---------------------
    def left(self, p):
        """Return a Position representing p's left child.
        Return None if p does not have a left child.
        """
        raise NotImplementedError('must be implemented by subclass')

    def right(self, p):
        """Return a Position representing p's right child.
        Return None if p does not have a right child.
        """
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:          # if left child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p                               # visit p between its subtrees
        if self.right(p) is not None:         # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other

    # override inherited version to make inorder the default
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder()                 # make inorder the default


# Modified, Goodrich at https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988 - Chapter 8
# Position is now implemented directly with no inheritance. Removed dead code.
class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right'  # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    # -------------------------- nested Position class --------------------------
    class Position:
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    # ------------------------------- utility methods -------------------------------
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:      # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    # -------------------------- binary tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # -------------------------- public accessors --------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:     # left child exists
            count += 1
        if node._right is not None:    # right child exists
            count += 1
        return count

    # -------------------------- nonpublic mutators --------------------------
    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2, respectively, as the left and right subtrees of the external Position p.
        As a side effect, set t1 and t2 to empty.
        Raise TypeError if trees t1 and t2 do not match type of this tree.
        Raise ValueError if Position p is invalid or not external.
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):    # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():         # attached t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None             # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():         # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None             # set t2 instance to empty
            t2._size = 0


# Modified, Goodrich at https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988
# Chapter 8
# 'x' is included with list of operators to be used with multiplication.
class ExpressionTree(LinkedBinaryTree):
    """An arithmetic expression tree."""

    def __init__(self, token, left=None, right=None):
        """Create an expression tree.
        In a single parameter form, token should be a leaf value (e.g., '42'),
        and the expression tree will have that value at an isolated node.
        In a three-parameter version, token should be an operator,
        and left and right should be existing ExpressionTree instances
        that become the operands for the binary operator.
        """
        super().__init__()                        # LinkedBinaryTree initialization
        if not isinstance(token, str):
            raise TypeError('Token must be a string')
        # use inherited, nonpublic method
        self._add_root(token)
        if left is not None:                      # presumably three-parameter form
            if token not in '+-*x/':
                raise ValueError('token must be valid operator')
            # use inherited, nonpublic method
            self._attach(self.root(), left, right)

    def __str__(self):
        """Return string representation of the expression."""
        pieces = []                 # sequence of piecewise strings to compose
        self._parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)

    def _parenthesize_recur(self, p, result):
        """Append piecewise representation of p's subtree to resulting list."""
        if self.is_leaf(p):
            # leaf value as a string
            result.append(str(p.element()))
        else:
            # opening parenthesis
            result.append('(')
            self._parenthesize_recur(self.left(p), result)     # left subtree
            result.append(p.element())                         # operator
            self._parenthesize_recur(self.right(p), result)    # right subtree
            # closing parenthesis
            result.append(')')

    def evaluate(self):
        """Return the numeric result of the expression."""
        return self._evaluate_recur(self.root())

    def _evaluate_recur(self, p):
        """Return the numeric result of subtree rooted at p."""
        if self.is_leaf(p):
            return float(p.element())      # we assume element is numeric
        else:
            op = p.element()
            left_val = self._evaluate_recur(self.left(p))
            right_val = self._evaluate_recur(self.right(p))
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '/':
                return left_val / right_val
            else:                          # treat '*' as multiplication
                return left_val * right_val


# Unmodified, Goodrich at https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988
# Chapter 8
def tokenize(raw):
    """Produces list of tokens indicated by a raw expression string.
    For example the string '(43-(3*10))' results in the list
    ['(', '43', '-', '(', '3', '*', '10', ')', ')']
    """
    SYMBOLS = set('+-x*/() ')    # allow for '*' or 'x' for multiplication

    mark = 0
    tokens = []
    n = len(raw)
    for j in range(n):
        if raw[j] in SYMBOLS:
            if mark != j:
                tokens.append(raw[mark:j])  # complete preceding token
            if raw[j] != ' ':
                tokens.append(raw[j])       # include this token
            mark = j+1                    # update mark to being at next index
    if mark != n:
        tokens.append(raw[mark:n])      # complete preceding token
    return tokens


# Unmodified, Goodrich at https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88988
# Chapter 8
def build_expression_tree(tokens):
    """Returns an ExpressionTree based upon by a tokenized expression.
    tokens must be an iterable of strings representing a fully parenthesized
    binary expression, such as ['(', '43', '-', '(', '3', '*', '10', ')', ')']
    """
    S = []                                        # we use Python list as stack
    for t in tokens:
        if t in '+-x*/':                            # t is an operator symbol
            # push the operator symbol
            S.append(t)
        elif t not in '()':                         # consider t to be a literal
            # push trivial tree storing value
            S.append(ExpressionTree(t))
        elif t == ')':       # compose a new tree from three constituent parts
            right = S.pop()                           # right subtree as per LIFO
            op = S.pop()                              # operator symbol
            left = S.pop()                            # left subtree
            S.append(ExpressionTree(op, left, right))  # repush tree
        # we ignore a left parenthesis
    return S.pop()


#~~~~~~~~~~~~~~~~~~~~~~~ Expression validity checking ~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Used for checking that all characters used in the expression meet the criteria.

def check_only_valid_characters(expression):
    """Check all characters are either brackets, integers, or operators"""
    for char in expression:
        if char not in "0123456789" and char not in "()" and char not in OPERATORS:
            return False
    return True


# Parenthesis mathing function taken from Goodrich book Ch.6, Code Fragment 6.4
# https://bcs.wiley.com/he-bcs/Books?action=chapter&bcsId=8028&itemId=1118290275&chapterId=88986
def check_parentheses_match(expression):
    """Check that all parenthesis in the expression match"""

    lefty = "("
    righty = ")"

    s = [] # indicates a stack

    for char in expression:
        if char in lefty:
            s.append(char)
        elif char in righty:
            if len(s) == 0:
                return False
            if righty.index(char) != lefty.index(s.pop()):
                return False
    return len(s) == 0


def check_operators_between_brackets(expression):
    """Check there is only one operator per each bracket pair.
    This function checks there is operands on both sides of the all operators
    and that check_parentheses_match(expression) has been called before it"""

    s = []    # inicates stack
    result = ""

    for char in expression:
        if char == "(":
            s.append(char)
        elif char in OPERATORS:
            if len(s) == 0 or s[-1] in OPERATORS:
                result = "too many operators"
                return result
            s.append(char)
        elif char == ")":
            # if between a closing and an opening bracket there isn't an operator then the expression is invalid.
            if s[-1] not in OPERATORS:
                result = "operator missing bewteen brackets"
                return result
            else:
                # pop the opening bracket and operator if no issues where found
                s.pop()
                s.pop()


class InvalidExpression(Exception):
    pass


def run_checks(expression):
    """Run all expression checks"""

    if not check_only_valid_characters(expression):
        raise InvalidExpression("ERROR: Expression must only contains parentheses, integers for the operands and the operators '+-*x/'")

    if not check_parentheses_match(expression):
        raise InvalidExpression("ERROR: Parentheses mismatched. Check all your parentheses match.")

    # Advanced checks required for check_operators_between_brackets(expression)
    if check_operators_between_brackets(expression) == "too many operators":
        raise InvalidExpression("ERROR: Too many operators per parentheses. Try adding more prentheses.")
    elif check_operators_between_brackets(expression) == "operator missing bewteen parentheses":
        raise InvalidExpression("ERROR: Operator missing between parentheses. Try adding an operator or removing operands or parentheses.")


#~~~~~~~~~~~~~~~~~~~~~ Visualise Tree ~~~~~~~~~~~~~~~~~~~~~~#

def visualize(exp_tree):
    """Do an inorder traversal of the tree and display all nodes in the inorder (infix) hierarchy"""
    for pos in exp_tree.positions():
        result = "  " * exp_tree.depth(pos) + pos.element()
        print(result)


#~~~~~~~~~~~~~~~~~~~~~~ Unit testing ~~~~~~~~~~~~~~~~~~~~~~~#
"""Unit testing methods obtained and utilised from https://docs.python.org/3/library/unittest.html ."""
class ExpressionValidityTests(unittest.TestCase):
    def test_valid_chars(self):
        self.assertTrue(check_only_valid_characters("(4*3*2)"))
        self.assertFalse(check_only_valid_characters("(f*7*4)"))
        self.assertFalse(check_only_valid_characters("(9 * 2 * 1)"))
        self.assertTrue(check_only_valid_characters("(4x3x2)"))
        self.assertFalse(check_only_valid_characters("(2*3-4+§9)"))

    def test_parentheses_matcher(self):
        self.assertTrue(check_parentheses_match(
            "(((6+4) *(4-3))/((1+9)+((6-1)+2)) *9)"))
        self.assertFalse(check_parentheses_match("((2+3)*(4*5)"))
        self.assertFalse(check_parentheses_match("(2+5)*(4/(2+2)))"))

    def test_ops_between_brackets(self):
        self.assertEqual(check_operators_between_brackets(
            "((7/4*3)*6)"), "too many operators")
        self.assertEqual(check_operators_between_brackets(
            "((4*3*4)/2)"), "too many operators")
        self.assertEqual(check_operators_between_brackets(
            "(4*6*(6))"), "too many operators")
        self.assertEqual(check_operators_between_brackets(
            "(4*(6))"), "operator missing bewteen brackets")
        self.assertEqual(check_operators_between_brackets(
            "(4*(66))"), "operator missing bewteen brackets")  # integers between 1-9 are only accepted in this assignment.

class ExpressionTreeTests(unittest.TestCase):
# Test that the expression is reconstructed properly after being turned into a tree.
    def test_expression_reconstruction(self):
        self.assertEqual(build_expression_tree("(((2*(3+2))+5)/2)").__str__(), "(((2*(3+2))+5)/2)")
        
    def test_tree_evaluation(self):
        self.assertEqual(build_expression_tree("(((2*(3+2))+5)/2)").evaluate(), 7.5)




#~~~~~~~~~~~~~~~~~~~~~ Saving and loading  ~~~~~~~~~~~~~~~~~~~~~#

class NameError(Exception):
    pass


class FileAlreadyExistsError(Exception):
    pass


def save_expression(exp_tree):
    """Prompt user for filename and saves .pickle file"""

    save_input = True
    # keep prompting until the filename meets criteria.
    while save_input:
        try:
            filename = prompt_user_input(
                "Please enter a filename (ext not needed). Use only aA-zZ, '_'(Underscores) and integers allowed.")
            for char in filename:
                if not char.isalpha() and char not in "0123456789" and char != "_":
                    raise NameError()

            # check if the file already exists
            if os.path.isfile(filename + ".pickle"):
                raise FileAlreadyExistsError()
            else:
                save_input = False  # no more need to check input
        except NameError:
            print("**ERROR: Input a valid filename!**")
        except FileAlreadyExistsError:
            print(
                "\n**ERROR: A filename already exists.  Please input a different name.**")
    with open(filename + ".pickle", "wb") as f:  # type: ignore
        pickle.dump(exp_tree, f)


def load_expression():
    """Prompt the user to input the .pickle file and return a error if not found."""

    keep_prompting = True
    while keep_prompting:
        try:
            u_input = prompt_user_input("Please enter the name of the file to be loaded (ext not needed). Input explicitly 'exit' to exit the load operation.") + ".pickle"
            if u_input[0:4] == "exit": # accepts first 4 characters as exit to run regardless if its a typo.
                keep_prompting = False
            elif os.path.isfile(u_input):
                with open(u_input, "rb") as f:   # rb indicates that binary file is being read.
                    load_tree = pickle.load(f)
                    print("\nVisualization of loaded tree:")
                    visualize(load_tree)
                    print("\nResult of loaded expression:")
                    print(load_tree, '=', load_tree.evaluate())
                keep_prompting = False
            else:
                print("ERROR: No such file! Try again.")
        except FileNotFoundError as e:
            print(e, "ERROR: File not found. Try again")
        except IOError as e:
            print(e, "ERROR: User input error. Try again")




#~~~~~~~~~~~~~~~~~~~ Execute app ~~~~~~~~~~~~~~~~~#

def prompt_user_input(prompt):
    """Utility function that returns the user's input"""
    user_input = input(f"\n{prompt}:\n")
    return user_input

def restart():
    """Prompts the user to restart the app."""

    keep_prompting = True
    # keep prompting user has inputted exactly "y" or "n"
    while keep_prompting:
        keep_running = prompt_user_input("Do you want to run the app again (y/n)?")
        # stop running only if the answer starts with "n"
        if keep_running == "y":
            keep_prompting = False
            return True
        elif keep_running == "n":
            keep_prompting = False
            return False
        else:
            print("\nWARNING: Please input exactly a 'y' or 'n'!")


def run_app():
    """Runs all app functions and provides a terminal menu interface for the user."""
    run = True

    while run:
        menu_screen = prompt_user_input("Please input whether you want to load or create a new expression, please enter either (load/new or exit)?")
        if menu_screen == "load":
            load_expression()
            run = restart()
        elif menu_screen == "exit":
            return exit()
        elif menu_screen == "new":
            # Assume by default that the expression is invalid and prompt until a valid one is given.
            exp_is_invalid = True
            while exp_is_invalid:
                expression = prompt_user_input("Please input a valid expression or input 'back' to return to main menu or 'exit' to close the app")
                if expression == "exit":
                    return exit()
                elif expression == "back":
                    return run_app()
                else:
                    try:
                        run_checks(expression)
                        exp_tree = build_expression_tree(tokenize(expression))
                        print("\nVisualization of the expression tree:")
                        visualize(exp_tree)
                        print("\nResult of the expression:")
                        print(exp_tree, '=', exp_tree.evaluate())
                        exp_is_invalid = False
                    except InvalidExpression as e:
                        print(e)
                    except IndexError as e:
                        print(e, "\nINVALID: This IndexError is caused by a missing operand!")
                    except TypeError as e:
                        print(e, "\nINVALID: This TypeError is caused by a missing operand!")
        
            keep_prompting = True
            while keep_prompting:
                save = prompt_user_input(
                    "Save the expression? (y/n)")
                if save == "y":
                    save_expression(exp_tree)
                    keep_prompting = False
                elif save == "n":
                    print("\nExpression is not saved.")
                    keep_prompting = False
                else:
                    print("\nINVALID: Please input explicitly a 'y' or 'n'!")

            run = restart()

        # keep asking until user has inputted exactly "load" or "new"
        else:
            print("\nINVALID: Please input explicitly 'load' or 'new'!")


"""Driver Code"""
# Modify Commenting to either execute the app or to run unit tests.

if __name__ == '__main__':
    # To run the unit tests, remove the comment '#' from unittest.main() and run the app.
    #unittest.main()
    run_app()
