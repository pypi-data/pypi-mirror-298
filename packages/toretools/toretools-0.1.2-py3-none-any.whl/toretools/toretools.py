#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# ToreTools - The useful tools for creating mathematical programs and more.
#
# Torrez Tsoi
# that1.stinkyarmpits@gmail.com
#
# License: MIT
#

import yt_dlp
import math
from echowave import ew
from typing import Self, Any
from functools import lru_cache
from fractions import Fraction
from . import trand
import random


def download(url: str, folder_dir: str):
    url = url
    ydl_opts = {"outtmpl": r"{}\%(title)s.%(ext)s".format(folder_dir)}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


class Const:
    @property
    def pi(self):
        return 3.14159265358979323846264338327950288419716939937510


const = Const()


class Trig:
    def sin(self, x, terms=9):
        x = x % (2 * const.pi)
        if x > const.pi:
            x = 2 * const.pi - x
        if x > const.pi / 2:
            x = const.pi - x

        sine = 0
        sign = 1
        power_of_x = x

        for n in range(terms):
            sine += sign * power_of_x / Factorial(2 * n + 1)
            sign *= -1
            power_of_x *= x * x

        return sine

    def cos(self, x, terms=9):
        x = x % (2 * const.pi)
        if x > const.pi:
            x = 2 * const.pi - x
        if x > const.pi / 2:
            x = const.pi - x
            flip_sign = -1
        else:
            flip_sign = 1

        cosine = 1
        sign = -1
        power_of_x = x * x

        for n in range(1, terms):
            cosine += sign * power_of_x / Factorial(2 * n)
            sign *= -1
            power_of_x *= x * x

        return flip_sign * cosine

    def tan(self, x):
        return math.tan(x)


trig = Trig()


@lru_cache(maxsize=None)
def Factorial(n: int):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    return n * Factorial(n - 1)


def ceil(x):
    n = int(x)
    return n if x == n else n + 1 if x > 0 else n


def floor(x):
    if isinstance(x, int):
        return x
    if x > 0:
        return int(x) if x == int(x) else int(x)
    else:
        return int(x) - 1 if x < int(x) else int(x)


def Primes(nth_prime: int):
    n = nth_prime
    p_sub_n = 1

    outsum_val = 0
    for i in range(1, 2**n + 1):
        jlist = []
        for j in range(1, i + 1):
            jlist.append((Factorial(j - 1) + 1) / j)

        insum_val = 0
        for element in jlist:
            insum_val += floor(trig.cos(element * const.pi) ** 2)

        outsum_val += floor((n / insum_val) ** (1 / n))

    p_sub_n += outsum_val

    return p_sub_n


def find_factors(n):
    factors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    return sorted(factors)


def isPrime(x: int):
    factors = find_factors(x)
    if len(factors) == 2 and factors[0] == 1 and factors[-1] == x:
        return True
    return False


def bigger_list_len(list1: list[Any], list2: list[Any]) -> str:
    return len(list1) if len(list1) > len(list2) else len(list2)


def bigger_int(int1: int, int2: int) -> int:
    return int1 if int1 > int2 else int2


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def nth_term_of_fibonacci(n: int):
    return round(
        (1 / math.sqrt(5)) * ((1 + math.sqrt(5)) / 2) ** n
        - (1 / math.sqrt(5)) * ((1 - math.sqrt(5)) / 2) ** n
    )


def matrix_multiply(matrix1, matrix2):
    rows_matrix1 = len(matrix1)
    cols_matrix1 = len(matrix1[0])
    rows_matrix2 = len(matrix2)
    cols_matrix2 = len(matrix2[0])

    if cols_matrix1 != rows_matrix2:
        raise ValueError(
            "Number of columns in matrix1 must equal number of rows in matrix2"
        )

    result = [[0 for _ in range(cols_matrix2)] for _ in range(rows_matrix1)]

    for i in range(rows_matrix1):
        for j in range(cols_matrix2):
            for k in range(cols_matrix1):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result


def quadratic_equation_solver(
    coefficients: list[int | float],
) -> None | int | float | list[int | float]:
    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]
    d = b**2 - 4 * a * c  # discriminant

    if d < 0:
        return None
    elif d == 0:
        x = (-b + math.sqrt(b**2 - 4 * a * c)) / 2 * a
        return x
    else:
        x1 = (-b + math.sqrt(b**2 - 4 * a * c)) / 2 * a
        x2 = (-b - math.sqrt(b**2 - 4 * a * c)) / 2 * a
        return [x1, x2]


def pi_estimater(interval=1000):
    """This function uses the Monte Carlo for Pi Estimation"""
    circle_points = 0
    square_points = 0

    # Total Random numbers generated= possible x
    # values* possible y values
    for i in range(interval**2):

        # Randomly generated x and y values from a
        # uniform distribution
        # Range of x and y values is -1 to 1
        rand_x = random.uniform(-1, 1)
        rand_y = random.uniform(-1, 1)

        # Distance between (x, y) from the origin
        origin_dist = rand_x**2 + rand_y**2

        # Checking if (x, y) lies inside the circle
        if origin_dist <= 1:
            circle_points += 1

        square_points += 1

        # Estimating value of pi,
        # pi= 4*(no. of points generated inside the
        # circle)/ (no. of points generated inside the square)
        pi = 4 * circle_points / square_points
    return pi


def sieve_of_eratosthenes(limit):
    if limit < 2:
        return []

    # Create a boolean array "prime[0..limit]" and initialize all entries as True.
    # A value in prime[i] will be False if i is not a prime, True if it is a prime.
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False  # 0 and 1 are not primes

    for start in range(2, int(math.sqrt(limit)) + 1):
        if sieve[start]:
            # Mark all multiples of start from start^2 onwards as False
            for i in range(start * start, limit + 1, start):
                sieve[i] = False

    # All True values in the sieve correspond to primes
    return [num for num, is_prime in enumerate(sieve) if is_prime]


def horner(poly, n, x):

    result = poly[0]

    for i in range(1, n):

        result = result * x + poly[i]

    return result


class PythagTripleConstraints:
    def __init__(self, m: int, n: int) -> None:
        self.m = m
        self.n = n

    def c1(self):
        return self.m > self.n > 0

    def c2(self):
        return math.gcd(self.m > self.n) == 1

    def c3(self):
        return (self.m > self.n) % 2 == 1

    def constraint1(self):
        return self.m > self.n > 0

    def constraint2(self):
        return math.gcd(self.m > self.n) == 1

    def constraint3(self):
        return (self.m > self.n) % 2 == 1


def gen_pythagorean_triples(
    triples: int | None = 1,
) -> tuple[int, int, int] | list[tuple[int, int, int]]:
    def gpt():
        mt = trand.MersenneTwister(trand.RandSeedGen().generate_seed())
        while True:
            m = mt.randint(2, 50)
            n = mt.randint(1, m - 1)
            ptc = PythagTripleConstraints(m, n)

            if ptc.c1() and ptc.c2() and ptc.c3():
                break

        return (m**2 - n**2, 2 * m * n, m**2 + n**2)

    triplelist = []
    for i in range(1, triples + 1):
        triplelist.append(gpt())
    if len(triplelist) == 1:
        return triplelist[0]
    else:
        return triplelist


def dec_to_bin(n: int) -> str:
    if n == 0:
        return "0"

    binary = ""

    while n > 0:
        remainder = n % 2
        binary = str(remainder) + binary  # Build the binary string
        n = n // 2  # Use integer division

    return binary


def bin_to_dec(binary_str: str) -> int:
    decimal = 0
    length = len(binary_str)

    for i in range(length):
        # Convert each bit to decimal
        bit = int(binary_str[length - 1 - i])  # Get the bit from the end
        decimal += bit * (2**i)  # Calculate the decimal value

    return decimal
