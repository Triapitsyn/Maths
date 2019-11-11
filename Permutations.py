'''
Class of permutation with defined '*', '*=', '==', '!=', '~', '**' and '**=' operators
Alexander Tryapitsyn for Linear Algebra Personal Homework
Contact me @tryapitsyn01 if something went wrong or needed to be clarified
'''


class permutation():
    def __init__(self, sigma):
        '''
        Building 0-indexed permutation from 0-indexed list or permutation itself
        '''
        if isinstance(sigma, permutation):
            self.sigma = sigma.sigma[:]
        else:
            if len(sigma) - 1 != max(sigma) or 0 != min(sigma) or len(set(sigma)) != len(sigma):
                raise Exception('''Argument can not be observed as permutation''')
            else:
                self.sigma = sigma

    def __mul__(self, other):
        '''
        Implementation of '*' operator between 2 permutations with same length's
        '''
        if not isinstance(other, permutation):
            raise Exception(f'''Can not multiply permutation and {type(other)}''')
        if len(self.sigma) != len(other.sigma):
            raise Exception('''Can not multiply 2 permutation's with different length's''')
        ans = [None for _ in range(len(other.sigma))]
        for i in range(len(other.sigma)):
            ans[i] = self.sigma[other.sigma[i]]
        return permutation(ans)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        '''
        Implementation of '==' operator
        '''
        return (type(other) == permutation) and (other.sigma == self.sigma)

    def __ne__(self, other):
        '''
        Implementation of '!=' operator
        '''
        return not self == other

    def __str__(self, latex=False):
        '''
        Return 1-indexed permutation as string.
        Use 'latex = True' to return latex matrix of permutation
        '''
        if latex:
            return ('\\[\\left(\\begin{matrix} \n' +
                    ' & '.join(map(str, range(1, len(self.sigma) + 1))) + '\\\\\n' +
                    ' & '.join(map(lambda x: str(x + 1), self.sigma)) + '\\\\\n' +
                    '\\end{matrix}\\right)\]')
        else:
            return str(self.sigma)

    def __invert__(self):
        '''
        Return permutation ** (-1)
        '''
        keymap = {self.sigma[i]: i for i in range(len(self.sigma))}
        return permutation([keymap[i] for i in range(len(self.sigma))])

    def __pow__(self, power):
        '''
        Return permutation ** power in O(log(power))
        '''
        if power == 0:
            return permutation(list(range(len(self.sigma))))
        elif power == 1:
            return permutation(self)
        elif power == 2:
            return self * self
        elif power > 0:
            return (self ** (power // 2)) ** 2 * self ** (power % 2)
        else:
            return (~self) ** (-power)

    def __ipow__(self, other):
        return self ** other

    @staticmethod
    def permutations(vec, r=None, start=0):
        '''
        Generate permutations
            with length r
            of items in vec
            using vec[:start] as beginning of permutation
        Code says for itself
        '''
        n = len(vec)
        if r == None:
            r = n
        if r <= start:
            yield permutation(vec[:r])
        else:
            for i in range(start, n):
                vec[start], vec[i] = vec[i], vec[start]
                for new in permutation.permutations(vec, r, start + 1):
                    yield new
                vec[start], vec[i] = vec[i], vec[start]


s1 = permutation([2, 7, 4, 5, 6, 0, 1, 3])
s2 = permutation([2, 4, 6, 5, 3, 0, 7, 1])
leftSideMid = permutation([3, 6, 1, 5, 4, 0, 2, 7])  # Left middle side of equation
# Solving: sigma * leftSideMid * sigma = (s1 ** (-1) * s2 ** 11) ** 173
# For sigma as permutation of 8 elements

rightSide = (s1 ** (-1) * s2 ** 11) ** 173
for sigma in permutation.permutations(list(range(8))):  # Brute-trying all permutation's with length 8
    if sigma * leftSideMid * sigma == rightSide:  # Check if another sigma is root of equation
        print(sigma.__str__(latex=False))  # Print latex matrix of equation's root
