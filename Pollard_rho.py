import sys
import time
import random
from math import gcd
from multiprocessing import Process, Queue, cpu_count

def is_prime(n, k=5):
    #米勒-拉宾素性测试
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # 将n-1表示为d*2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # 进行k次测试
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def pollard_rho(n, c=1):
    #Pollard Rho算法寻找非平凡因子
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    if n % 5 == 0:
        return 5
    
    f = lambda x: (pow(x, 2, n) + c) % n
    x, y, d = 2, 2, 1
    
    # 不设置最大迭代次数，持续运行直到找到因子
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    
    if d == n:
        return None
    return d

def factorize(n):
    #递归分解质因数
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    
    # 尝试不同的c值直到找到因子
    factor = None
    c = 1
    while factor is None:
        if c == 0 or c == n - 2:
            c += 1
            continue
        factor = pollard_rho(n, c)
        c += 1
        if c >= n:
            c = 1
    
    return factorize(factor) + factorize(n // factor)

def parallel_pollard_rho_task(n, c, result_queue):
    #并行执行Pollard Rho算法的任务函数
    try:
        factor = pollard_rho(n, c)
        if factor is not None and 1 < factor < n:
            result_queue.put(factor)
    except Exception:
        pass

def parallel_factorize(n):
    #    并行分解质因数
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    
    # 使用所有可用的CPU核心
    num_processes = cpu_count()
    result_queue = Queue()
    processes = []
    
    # 使用已知良好的c值和随机值
    good_c_values = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    for i in range(num_processes):
        if i < len(good_c_values):
            c = good_c_values[i]
        else:
            c = random.randint(1, n-1)
        
        p = Process(target=parallel_pollard_rho_task, args=(n, c, result_queue))
        processes.append(p)
        p.start()
    
    # 等待结果，不设置超时
    factor = None
    while factor is None:
        if not result_queue.empty():
            factor = result_queue.get()
            break
    
    # 终止所有进程
    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join()
    
    if factor is not None:
        return parallel_factorize(factor) + parallel_factorize(n // factor)
    else:
        return factorize(n)

def main():
    # 获取输入
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = int(input("Enter a number to factorize: "))
    
    # 记录开始时间
    time_start = time.time()
    
    # 分解质因数
    factors = parallel_factorize(n)
    
    # 排序并输出结果
    factors.sort()
    
    time_end = time.time()
    print(f"分解 {n} 的质因数结果: {factors}")
    print(f"任务执行时间: {time_end - time_start:.6f}秒")

if __name__ == '__main__':
    main()