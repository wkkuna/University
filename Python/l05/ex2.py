class Formula:
	def __mul__(self, other):
		return And(self, other)
	def __add__(self, other):
		return Or(self, other)
	def eval(self, v):
		raise NotImplementedError("Plain formula can not be evaluated")


class BinOp(Formula):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	def __str__(self):
		return '(' + str(self.left) + ' ' + self.op + ' ' + str(self.right) + ')'

class And(BinOp):
	op = '∧'
	def eval(self, v):
		return self.left.eval(v) and self.right.eval(v)

class Or(BinOp):
	op = '∨'
	def eval(self, v):
		return self.left.eval(v) or self.right.eval(v)

class Not(Formula):
	def __init__(self, child):
		self.child = child
	def eval(self, v):
		return not self.child.eval(v)
	def __str__(self):
		return '¬' + str(self.child)

class Var(Formula):
	def __init__(self, name):
		self.name = name
	def eval(self, v):
		return self in v
	def __str__(self):
		return str(self.name)

class Const(Formula):
	def __init__(self, value):
        if type(value) != bool:
            raise ValueError("Const must be of type bool")
        self.value = value
	def eval(self, v):
		return self.value
	def __str__(self):
		return str(self.value)
