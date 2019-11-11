'''
Calculating determinant of square matrix X ∈ M_n(R ∪ {'x'}) as polynomial function of 'x'
Alexander Tryapitsyn for Linear Algebra Personal Homework
Contact me @tryapitsyn01 if something went wrong or needed to be clarified
'''

def permutations(vec, r = None, start = 0):
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
        yield vec[:r]
    else:
        for i in range(start, n):
            vec[start], vec[i] = vec[i], vec[start]
            for new in permutations(vec, r, start + 1):
                yield new
            vec[start], vec[i] = vec[i], vec[start]

def sgn(sigma):
    '''
    Return sign of permutation sigma by brute-finding all inversions
    '''
    sign = 1
    for i in range(n):
        for j in range(i, n):
            if sigma[j] < sigma[i]:
                sign = -sign
    return sign

def calc_sigma(sigma):
    '''
    Assuming sigma on X as (X[i][sigma[i] for i in range(len(sigma)))
    Return tuple (degree of 'x' in  on X, product of all const permutation X)
    '''
    deg_x, coef = 0, 1
    for i, j in zip(range(n), sigma):
        if X[i][j] == 'x':
            deg_x += 1
        else:
            coef *= X[i][j]
    return deg_x, sgn(sigma) * coef

X = [[-2, 9, 2, -4, -8, 3, 'x'],
     [-2, -7, -6, -1, 'x', 5, 6],
     [7, 2, 9, 'x', -7, -8, 2],
     [-7, -8, 5, 1, 'x', 9, 2],
     ['x', 2, 4, -3, -7, -9, 2],
     [-8, 1, 'x', -4, -6, 'x', -4],
     [1, 'x', 2, -2, -4, 2, -9]]
n = len(X)
polynom = [0 for i in range(n)]

print('Определитель, как полином: ')
for sigma in permutations(list(range(n))):
    deg_x, coef = calc_sigma(sigma)
    polynom[deg_x] += coef
print(' + '.join('(' + str(polynom[i]) + f'x^{i})'
              for i in range(n - 1, -1, -1)))
# Determinant as a polynom of 'x'
# prints (7x^6) + (27x^5) + (153x^4) + (318x^3) + (-92948x^2) + (821973x^1) + (1503972x^0)