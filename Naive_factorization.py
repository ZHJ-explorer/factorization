import math
import time
import sys
def breakdown(N):
    result = []
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:  # 如果 i 能够整除 N，说明 i 为 N 的一个质因子。
            while N % i == 0:
                N //= i
            result.append(i)
    if N != 1:  # 说明再经过操作之后 N 留下了一个素数
        result.append(N)
    return result

if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = int(input("Enter a number to factorize: "))

time_start = time.time()
result = breakdown(N)
time_end = time.time()
print(result)
print(f"任务执行时间: {time_end - time_start}秒")