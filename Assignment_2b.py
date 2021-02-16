# BINF6200 Assignment 2 - Part 2
# Michelle Jimenez

import sys
import math


def calc_average(numbers):
    """Calculate the average of a list of numbers

    Args:
        numbers (list): List of floats

    Returns:
        float: The average
    """
    return float(sum(numbers) / len(numbers))


def calc_variance(numbers):
    """Calculate the variance of a list of numbers

    Args:
        numbers (list): List of floats

    Returns:
        float: The variance. None if numbers contains only one entry.
    """
    n = len(numbers)
    if n == 1:
        return None
    else:
        mean = sum(numbers) / float(n)
        variance = sum((x - mean) ** 2 for x in numbers) / float(n - 1)
        return variance


def calc_std_dev(numbers):
    """Calculate the standard deviation of a list of numbers

    Args:
        numbers (list): List of floats

    Returns:
        float: The standard deviation
    """
    n = len(numbers)
    if n <= 1:
        return 0.0
    else:
        return math.sqrt(calc_variance(numbers))


def calc_median(numbers):
    """Calculate the median of a list of numbers

    Args:
        numbers (list): List of floats

    Returns:
        float: The median
    """
    n = len(numbers)
    numbers.sort()
    if n % 2 == 0:
        median1 = numbers[n//2]
        median2 = numbers[n//2 - 1]
        median = (median1 + median2)/2
    else:
        median = numbers[n//2]
    return median


def main():
    numbers = []
    while True:
        number = input("Enter number: ")
        if not number:
            break
        try:
            numbers.append(float(number))
        except:
            print(f'Invalid input ({number}). Please enter a valid number.')

    if numbers:
        print('---------------')
        print('The list is:', numbers)
        print('Count:', len(numbers))
        print('Average:', calc_average(numbers))
        print('Maximum: ', max(numbers))
        print('Minimum: ', min(numbers))
        print('Variance:', calc_variance(numbers))
        print('Standard Deviation:', calc_std_dev(numbers))
        print('Median:', calc_median(numbers))
    else:
        print("Statistics not performed")


if __name__ == '__main__':
    main()
