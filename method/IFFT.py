from cmath import exp, pi, sqrt
from typing import List
from method.help_function import isPowerOf2, column
from PyQt5.QtGui import QImage, QColor


def IFFT(img: QImage) -> List[List[float]]:
    grey_matrix = []

    # get the grey value
    for h in range(img.height()):
        temp = []
        for w in range(img.width()):
            value = QColor(img.pixel(w, h))
            grey = value.red() * 0.299 + value.green() * 0.587 + value.blue() * 0.144
            grey = grey / pow(-1, w + h)  # move to side>?
            temp.append(grey)
        grey_matrix.append(temp)

    # do for row first
    row_FFT_list = []
    for i in grey_matrix:
        row_FFT_list.append(recursive_idft(i))

    # do for col then
    col_FFT_list = []
    for i in range(len(row_FFT_list[0])):
        col_FFT_list.append(recursive_idft(column(row_FFT_list, i)))

    # change the complex to float
    M = len(col_FFT_list)
    N = len(col_FFT_list[0])
    for i in range(M):
        for j in range(N):
            col_FFT_list[i][j] = abs(col_FFT_list[i][j] / sqrt(M * N))

    return col_FFT_list


def recursive_idft(x: List[float]) -> List[complex]:
    N = len(x)

    if isPowerOf2(N) is False:
        raise ValueError('The input array doesnt have the length as power of 2!\n')

    # base case
    if N <= 1:
        return x

    # get the even and odd part of dft of x
    even = recursive_idft(x[0::2])
    odd = recursive_idft(x[1::2])

    # calculate T (e^(2*pi*j*k/N) * odd)
    T = []
    for k in range(len(odd)):
        T.append(exp(2j * pi * k / N) * odd[k])

    # X[k] = E[k] + T
    # X[k+N//2] = E[k] - T

    first = []
    second = []
    # just return the abs value
    for k in range(N // 2):
        first.append((even[k] + T[k]) / 1)
        second.append((even[k] - T[k]) / 1)

    return first + second

