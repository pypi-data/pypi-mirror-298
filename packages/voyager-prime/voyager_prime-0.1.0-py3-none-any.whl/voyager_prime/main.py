import os
import math
import sys


def prime(limit, print_prime=False):
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    for number in range(2, int(limit ** 0.5) + 1):
        if primes[number]:
            for multiple in range(number * number, limit + 1, number):
                primes[multiple] = False
    prime_numbers = [num for num in range(limit + 1) if primes[num]]

    if print_prime == True:
        print(f"[Voyager] [INFO] Prime numbers found: {prime_numbers}")

    return prime_numbers


def prime_mnmx_lim(min_limit, max_limit, print_prime=False):
    if min_limit == "":
        min_limit = 1
    if max_limit == "":
        print("[Voyager] [ERR] Please provide max_limit argument.")
        exit(13)
    primes = [True] * (max_limit + 1)
    primes[0] = primes[1] = False
    for number in range(2, int(max_limit ** 0.5) + 1):
        if primes[number]:
            for multiple in range(number * number, max_limit + 1, number):
                primes[multiple] = False

    prime_numbers = [num for num in range(min_limit, max_limit + 1) if primes[num]]

    if print_prime:
        print(f"[Voyager] [INFO] Prime numbers between {min_limit} and {max_limit} found: {prime_numbers}")

    return prime_numbers


def prime_iter_lim(limit=10, print_prime=False):
    prime_numbers = []

    number = 2

    while len(prime_numbers) < limit:
        is_prime = True

        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break
        if is_prime:
            prime_numbers.append(number)
        number += 1
    if print_prime:
        print(f"[Voyager] [INFO] First {limit} prime numbers found: {prime_numbers}")

    return prime_numbers


def prime_mnmxiter_lim(limit=10, min_limit=2, max_limit=30, print_prime=False):
    primes = [True] * (max_limit + 1)
    primes[0] = primes[1] = False
    for number in range(2, int(max_limit ** 0.5) + 1):
        if primes[number]:
            for multiple in range(number * number, max_limit + 1, number):
                primes[multiple] = False

    prime_numbers = [num for num in range(min_limit, max_limit + 1) if primes[num]]

    prime_numbers = prime_numbers[:limit]

    if print_prime:
        print(f"[Voyager] [INFO] First {limit} prime numbers between {min_limit} and {max_limit} found: {prime_numbers}")

    return prime_numbers










