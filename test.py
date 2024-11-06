import time

START = time.perf_counter()

# twod_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# for row in twod_list:
#     print(row)
# print(twod_list[1][2])

# [print(row) for row in twod_list]

# print("\n".join([str(row) for row in twod_list]))
# def func():
#     start = time.perf_counter()
#     import random
#     end = time.perf_counter()
#     elapsed = end - start
#     return elapsed

END = time.perf_counter()

print(END - START)
# print(func())
