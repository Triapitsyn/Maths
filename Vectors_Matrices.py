class Numbers:
    number = (int, float, complex)


class VectorOperationError(Exception):
    def __init__(self, vec1, vec2, op):
        self.txt = f"Can not {op} vectors with sizes {len(vec1)} and {len(vec2)}"

    def __str__(self):
        return self.txt


class MyTypeError(Exception):
    def __init__(self, obj1, obj2, op):
        self.txt = f"Can not {op} objects with types {type(obj1)} and {type(obj2)}"

    def __str__(self):
        return self.txt


class VectorInitError(Exception):
    def __init__(self):
        self.txt = "Can not initialize non-math-expression Vector"

    def __str__(self):
        return self.txt


class Vector(Numbers):
    import copy
    def __init__(self, vec):
        for elem in list(vec):
            if not isinstance(elem, self.number):
                raise VectorInitError()
        self.data = self.copy.deepcopy(list(vec))

    def __iter__(self):
        for x in self.data:
            yield x

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iadd__(self, other):
        if isinstance(other, Vector):
            if len(self) == len(other):
                for i in range(len(other)):
                    self[i] += other[i]
            else:
                raise VectorOperationError(self, other, '+')
        elif isinstance(other, self.number):
            for i in range(len(self)):
                self[i] += other
        else:
            raise MyTypeError(self, other, '+')
        return self

    def __add__(self, other):
        mediator = self.copy.deepcopy(self)
        mediator += other
        return mediator

    def __radd__(self, other):
        return self + other

    def __imul__(self, other):
        if isinstance(other, self.number):
            for i in range(len(self)):
                self[i] *= other
        else:
            raise MyTypeError(self, other, '*=')
        return self

    def __mul__(self, other):
        if isinstance(other, self.number):
            mediator = self.copy.deepcopy(self)
            mediator *= other
            return mediator
        elif isinstance(other, Vector):
            if len(self) == len(other):
                return sum(map(lambda x, y: x * y, self, other))
            else:
                raise VectorOperationError(self, other, '*')
        else:
            raise MyTypeError(self, other, '*')

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return self * (-1)

    def __pos__(self):
        return self

    def __isub__(self, other):
        self += -other
        return self

    def __sub__(self, other):
        mediator = self.copy.deepcopy(self)
        mediator -= other
        return mediator

    def __rsub__(self, other):
        return self - other

    def __itruediv__(self, other):
        if isinstance(other, self.number):
            for i in range(len(self)):
                self[i] /= other
        else:
            raise MyTypeError(self, other, '/')
        return self

    def __truediv__(self, other):
        mediator = self.copy.deepcopy(self)
        mediator /= other
        return mediator

    @staticmethod
    def ones(size):
        return Vector([1 for _ in range(size)])

    @staticmethod
    def zeros(size):
        return Vector([0 for _ in range(size)])

    @staticmethod
    def one(size, pos):
        vec = Vector.zeros(size)
        vec[pos] = 1
        return vec

    def __eq__(self, other):
        if isinstance(other, Vector):
            zeros = Vector.zeros(max(len(self), len(other)))
            return all(map(lambda x, y: x == y, self - other, zeros))
        elif isinstance(other, self.number):
            return all([x == other for x in self])
        else:
            return False

    def __ne__(self, other):
        return (not isinstance(other, Vector)) or (not (self == other))

    def length(self):
        from math import sqrt
        return sqrt(sum(map(lambda x, y: x * y, self, self)))

    def __str__(self):
        return str(self.data)


class MatrixOperationError(Exception):
    def __init__(self, m1, m2, op):
        self.matrix1 = m1
        self.matrix2 = m2
        self.txt = (f'''Can't '{op}' two matriсes with 
                    sizes {m1.size()} and {m2.size()}.''')

    def __str__(self):
        return self.txt


class MatrixInitError(Exception):
    def __init__(self):
        self.txt = "Can not initialize non-rectangle Matrix"

    def __str__(self):
        return self.txt


class Matrix(Numbers):
    import copy
    def __init__(self, a):
        columnCntMax = max(map(lambda x: len(x), a))
        columnCntMin = min(map(lambda x: len(x), a))
        if columnCntMax != columnCntMin:
            raise MatrixInitError
        self.data = []
        for vec in a:
            self.data.append(Vector(vec))

    def __iter__(self):
        for vec in self.data:
            yield vec

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        return '\n'.join(map(lambda x: '\t'.join(map(str, x)), self))

    def size(self):
        return len(self), len(self[0])

    def __iadd__(self, other):
        if isinstance(other, Matrix):
            if self.size() == other.size():
                for i in range(len(self)):
                    mid = self[i] + other[i]
                    self[i] = mid
            else:
                raise MatrixOperationError(self, other, '+')
        elif isinstance(other, self.number):
            for i in range(len(self)):
                self[i] += other
        else:
            raise MyTypeError(self, other, '+')
        return self

    def __add__(self, other):
        mediator = self.copy.deepcopy(self)
        mediator += other
        return mediator

    def __radd__(self, other):
        return self + other

    def __isub__(self, other):
        self += (-other)
        return sub

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self - other

    @staticmethod
    def zeros(shape):
        a = [Vector.zeros(shape[1]) for j in range(shape[0])]
        return Matrix(a)

    @staticmethod
    def diag(rang, lmbd=1):
        a = Matrix.zeros([rang, rang])
        for i in range(rang):
            a[i][i] = lmbd
        return a

    @staticmethod
    def E(rang):
        return Matrix.diag(rang)

    def T(self):
        return Matrix.transposed(self)

    def __imul__(self, other):
        return self * other

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.size()[1] == other.size()[0]:
                ans = Matrix.zeros([self.size()[0], other.size()[1]])
                oth = Matrix.transposed(other)
                for i in range(self.size()[0]):
                    for j in range(other.size()[1]):
                        ans[i][j] = self[i] * oth[j]
                return ans
            else:
                raise MatrixOperationError(self, other, '*')
        elif isinstance(other, self.number):
            ans = Matrix.zeros(self.size())
            for i in range(len(self)):
                ans[i] = self[i] * other
            return ans
        else:
            raise MyTypeError(self, other, '*')

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return self * (-1)

    def __pos__(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if self.size() == other.size():
                zeros = Matrix.zeros(self.size())
                return all(map(lambda x, y: x == y, self - other, zeros))
            else:
                return False
        elif isinstance(other, self.number):
            return all([x == other for x in self])
        else:
            return False

    def transpose(self):
        self.data = Matrix.transposed(self).data
        return Matrix(self.data)

    @staticmethod
    def transposed(matrix):
        return Matrix(list(map(lambda *x: Vector(x), *matrix)))

    def solve(self, bias):
        ext = Matrix(list(map(lambda x, y: list(x) + [y], self, bias)))
        row = 0
        for column in range(len(ext[0]) - 1):
            print(ext)
            print()
            row_now = int(row)
            while ext[row_now][column] == 0:
                row_now += 1
                if row_now == len(ext):
                    break
            if row_now == len(ext):
                continue
            ext[row], ext[row_now] = ext[row_now], ext[row]
            ext[row] /= ext[row][column]
            for i in range(len(ext)):
                if i == row:
                    continue
                ext[i] += ext[row] * (-ext[i][column])
            row += 1
        print(Matrix(ext))
        for i in range(row, len(ext)):
            if ext[i][-1] != 0:
                return "NO SOLUTIONS"
        if row != len(ext[0]) - 1:
            return 'INFINITY SOLUTIONS'
        return Matrix.transposed(Matrix(ext))[-1]
