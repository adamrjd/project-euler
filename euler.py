class gregorian(object):
    calendar = list()
    gregorian = dict()
    days = list()

    def __init__(self):
        self.calendar = ["JAN", "FEB", "MAR", "APR", "MAY",
                         "JUN", "JUL", "AUG", "SEP",  "OCT",  "NOV",  "DEC"]
        self.gregorian = {"JAN": [31, 31], "FEB": [28, 29], "MAR": [31, 31], "APR": [30, 30], "MAY": [31, 31],
                          "JUN": [30, 30], "JUL": [31, 31], "AUG": [31, 31], "SEP": [30, 30], "OCT": [31, 31], "NOV": [30, 30], "DEC": [31, 31]}
        self.days = ["Mon", "Tue", "Wed", "Thu",
                     "Fri", "Sat", "Sun"]


class arithmetic(object):
    """ A set of methods for scalable arithmetic functions like divisors, factors, and primes """

    def __init__(self, maxnum=1000, alist=False):
        self.sieve = arithmetic._sieve(maxnum)
        if alist:
            self.abundants = self.abundant_list(maxnum)

    def _sieve(n):
        # sieve of eratosthenes...space-complex
        a = {i: True for i in range(2, n)}
        for i in range(2, n):
            if a[i]:
                for j in range(i * i, n, i):
                    if a[j]:
                        a[j] = False
        return [i for i in a.keys() if a[i]]

    def prime_factors_and_multiplicities(n):
        from math import ceil
        sieve = arithmetic(1000 * (n % 1000 + 1)).sieve
        pfactors_mults = dict()
        for prime in sieve:
            if prime <= ceil(n / 2):
                if n % prime == 0:
                    i = 1
                    mult = prime
                    pfactors_mults[prime] = list()
                    while mult < n:
                        if n % mult == 0:
                            pfactors_mults[prime].append(i)
                        i = i + 1
                        mult = prime * i
            else:
                break
        return [[k * p for p in pfactors_mults[k]] for k in pfactors_mults]

    def pprop_divs(self, n):
        '''Returns a sorted list of the proper divisors of int n.'''
        divisors = set()
        for prime in self.sieve:
            if prime <= (n // 2):
                if n % prime == 0:
                    i = 1
                    factor = prime
                    while factor < n:
                        if n % factor == 0:
                            divisors.add(factor)
                        i += 1
                        factor = prime * i
            else:
                break
        return list(sorted(divisors))

    def prime_proper_divisors(sieve, n):
        from math import ceil
        l = set()
        for prime in sieve:
            if prime <= ceil(n / 2):
                if n % prime == 0:
                    i = 1
                    mult = prime
                    while n % mult == 0:
                        if mult in sieve:
                            l.add(mult)
                        i += 1
                        mult = prime * i
            else:
                break
        return sorted(l)

    def quality(self, n):
        return bool(n < sum(self.pprop_divs(n)))

    def abundant_list(self, n):
        return [i + 1 for i, b in enumerate([False if not self.quality(i) else True for i in range(1, n + 1)]) if b]

    def reciprocal_cycles(n, precision):
        def reciprocal(num, prec):
            n = 1
            rem = n * 10 % num
            count = 0
            while count < prec:
                if rem == 0:
                    yield int(n * 10 / num)
                    return
                yield int(n * 10 / num)
                n = rem
                rem = n * 10 % num
                count += 1
        digits = list(reciprocal(n, precision))
        i = 1
        pos = 0
        cycle = list()
        while pos < len(digits):
            l = digits[pos:pos + i]
            if len(l) > 0 and l == digits[pos + i:pos + 2 * i] and l == digits[pos + 2 * i:pos + 3 * i]:
                cycle = l
                break
            elif i > len(digits):
                pos += 1
                i = 1
            else:
                i += 1
        dec = '0.' + ''.join([str(x) for x in digits])
        return (cycle, dec)


class euler(object):

    @staticmethod
    def fib_gen(n):
        a, b = 0, 1
        while n > 0:
            yield a
            a, b, n = b, a + b, n - 1

    @staticmethod
    def interesting_pattern(i, j, sieve_ls=arithmetic._sieve(1000)):
        # a elem 1,3,5,7,9,...
        # b elem primes
        from sys import maxsize
        f = lambda n, a, b: n * n + a * n + b
        count = 0
        for x in range(0, maxsize):
            if f(x, i, j) in sieve_ls:
                count += 1
            else:
                break
        return count

    @staticmethod
    def lexicographic_permutation(ls):
        ls = sorted(ls)
        output = dict()
        output[min(ls)] = [([i], list(ls)[0:i] + list(ls)[i + 1:]) for i in ls]
        while max(ls) not in output:
            key = max(output.keys()) + 1
            output[key] = list()
            for i in output[key - 1]:
                for item in i[1]:
                    output[key].append(
                        (i[0] + [item], [_ for _ in i[1] if _ != item]))
        return [item[0] for item in output[max(ls)]]

    @staticmethod
    def spiral(n):
        # traverse spiral counterclockwise and calculate pos
        # if in diagonal coord set, add to sum
        diagonal_sum = 0
        diagonal_set = {(_, n - 1 - _) for _ in range(n)}
        visited_diagonals = set()
        '''
        should be O(n*n) but isnt lol...

        possible optimizations:
        -change data struct for diagonals sets;
        checking sets over and over is time and space complex
        -change position update to a lambda'''
        [diagonal_set.add((_, _)) for _ in range(n)]
        pos = (0, n - 1)
        dir = -1  # 0:left, 1:down, 2:right, 3:up, -1: up-right corner
        i = n * n
        # state machine
        while i > -1:
            # change state based on position
            if pos in diagonal_set:
                if pos not in visited_diagonals:
                    diagonal_sum += i
                    visited_diagonals.add(pos)
                    dir += 1
                else:  # only ever going to reach here when dir=3
                    dir = -1
                    i += 1
                    pos = (pos[0] + 1, pos[1] - 1)
            # update position based on state
            if dir == 0:
                pos = (pos[0], pos[1] - 1)
            elif dir == 1:
                pos = (pos[0] + 1, pos[1])
            elif dir == 2:
                pos = (pos[0], pos[1] + 1)
            elif dir == 3:
                pos = (pos[0] - 1, pos[1])
            i -= 1
        return diagonal_sum

    @staticmethod
    def coin_sums(denominations=[1, 2, 5, 10, 20, 50, 100, 200], money=200, i=0):
        if len(denominations) > 1:
            return coin_sums(denominations[1:], money, i)
        else:
            return money // denominations[0]

    @staticmethod
    def largest_pandigital_prime():
        digits = set()
        # need to make this generator
        sieve = reversed(arithmetic(987654321).sieve)
        for prime in sieve:
            testing_set = set([str(x) for x in range(1, len(prime))])
            if set(str(prime)) == testing_set:
                return prime  # guaranteed to be largest


class roman(object):
    numerals = dict()

    def __init__(self):
        self.numerals = {1: "I", 5: "V", 10: "X",
                         50: "L", 100: "C", 500: "D", 1000: "M"}


class scientific(object):
    digits = list()
    precision = 324  # default float
    power = 1
    negative = False

    def __init__(self, num):
        if isinstance(num, str) and len(num.split('.')) == 2:
            self.power -= len(num.split('.')[0])
            [self.digits.append(int(digit)) for digit in list(
                ''.join(num.split('.')))]
            # add scientific notation

    def __truediv__(self, y):
        pass

if __name__ == "__main__":
    print(euler.dp_change(200, [1, 2, 5, 10, 20, 50, 100]))
    print('hello world')
    # consecutive numbers that have 4 unique prime factors
    '''
    from sys import maxsize
    c = 4
    s = arithmetic(100000).sieve
    func = arithmetic.prime_proper_divisors
    for i in range(647, maxsize):
        lst = list(func(s, i))
        if len(lst) == c:
            l = [list(func(s, j)) for j in range(i, i + c)]
            if all([len(lst) == c for lst in l]):
                print(i)
                break'''
