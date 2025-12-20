# Pollard-Rho 算法大整数因式分解项目

## 项目简介

本项目实现了基于 $Pollard-Rho$ 算法的大整数因式分解，并提供了与传统朴素因式分解算法的性能对比验证脚本。
$Pollard-Rho$ 算法是一种高效的随机化因式分解算法，特别适合于分解大整数，其平均时间复杂度为 $O(n^{1/4})log(n)$，远优于传统朴素算法的 $O(\sqrt{n})$。

## 依赖

- Python 3.6+
- 标准库：`sys`, `time`, `random`, `math`, `multiprocessing`

## 克隆仓库

```bash
git clone https://github.com/your-username/factorization.git
cd factorization
```

## 项目架构

### 核心文件结构

```
factorization/
├── Pollard_rho.py        # Pollard-Rho 算法实现(含并行优化)
├── Naive_factorization.py # 朴素因式分解算法实现
├── factorization_test.py  # 性能对比测试脚本
├── test.txt              # 测试数据文件
├── LICENSE               # 许可证文件
└── README.md             # 项目说明文档
```

### 模块功能说明

1. **Pollard_rho.py**：
   - 实现了 Pollard-Rho 算法的核心逻辑
   - 集成了 Miller-Rabin 素性测试用于素数判定
   - 提供了单进程和多进程并行两种因式分解方式
   - 支持命令行参数输入和交互式输入

2. **Naive_factorization.py**：
   - 实现了传统的朴素因式分解算法
   - 用于与 Pollard-Rho 算法进行性能对比

3. **factorization_test.py**：
   - 从测试文件读取待分解的数字列表
   - 分别使用两种算法对每个数字进行因式分解
   - 记录并比较两种算法的执行时间
   - 生成 CSV 格式的测试结果报告
   - 支持日志记录

## $Pollard-Rho$ 算法原理与实现

### 算法原理

$Pollard-Rho$ 算法是一种基于随机化的因式分解算法，其核心思想是通过寻找一个非平凡的因子 $d$ ，使得 $1 < d < n$，并递归地分解 $d$ 和 $\frac{n}{d}$。

算法步骤：

1. **素性测试**：使用 $Miller-Rabin$ 算法判断 n 是否为素数，若是则直接返回。
2. **寻找因子**：通过迭代计算函数 $$f(x) = (x^2 + c) \mod n$$生成伪随机序列，并使用 Floyd 判圈算法寻找序列中的碰撞点，从而得到 n 的一个非平凡因子 d 。
3. **递归分解**：递归地分解 $d$ 和 $\frac{n}{d}$ ，直到所有因子都是素数。

### 关键实现细节

1. **Miller-Rabin 素性测试**：
   - 实现了确定性的 $Miller-Rabin$ 测试，对于 $2^{64}$ 以内的数字使用固定的 7 个基数 $[2, 325, 9375, 28178, 450775, 9780504, 1795265022]$，保证测试结果正确。
   - 时间复杂度：$O(k \log^3 n)$ ，其中 $k$ 是测试的基数数量，此处为7。

2. **Pollard-Rho 因子寻找**：
   - 采用 $Floyd$ 判圈算法检测序列中的循环，避免无限循环。
   - 使用随机化的常数 $c$ 来提高算法效率，若当前 $c$ 无法找到因子，则尝试其他 $c$ 值。
   - 优化：预检查小因子$2、3、5$，提高算法效率。

3. **并行化优化**：
   - 利用 Python 的 `multiprocessing` 模块实现并行计算。
   - 为每个 CPU 核心创建一个进程，每个进程使用不同的 $c$ 值同时执行 $Pollard-Rho$ 算法。
   - 一旦某个进程找到因子，立即终止所有其他进程，提高效率。

### 算法复杂度分析

- **时间复杂度**：平均情况下为 $O(n^{1/4} \log (n))$ ，远优于朴素算法的 $O(\sqrt{n})$ 。
- **空间复杂度**：$O(\log n)$ ，主要用于递归调用栈。

## 性能对比验证

### 测试方法

1. **测试数据**：从 `test.txt` 文件中读取待分解的数字列表。
2. **测试流程**：
   - 由于 $Pollard-Rho$ 算法的随机性，对每个数字，使用 $Pollard-Rho$ 算法运行 5 次，取平均时间。
   - 对每个数字，使用朴素算法运行 1 次，记录时间。
   - 生成包含原始数字、$Pollard-Rho$ 算法各次运行时间和朴素算法时间的 CSV 报告。
3. **性能指标**：执行时间(秒)。

### 预期结果

- 对于小整数(小于 $10^6$ )，两种算法性能差异不大。
- 对于大整数(大于 $10^{10}$ )，$Pollard-Rho$ 算法的性能优势将明显体现。

## 使用方法

### 直接使用算法

1. **使用 $Pollard-Rho$ 算法**：
   ```bash
   python Pollard_rho.py [number]
   ```
   或
   ```bash
   python Pollard_rho.py
   # 根据提示输入数字
   ```

2. **使用朴素因式分解算法**：
   ```bash
   python Naive_factorization.py [number]
   ```
   或
   ```bash
   python Naive_factorization.py
   # 然后根据提示输入数字
   ```

### 运行性能对比测试

1. **准备测试数据**：在 `test.txt` 文件中添加待测试的数字，每个数字占一行。

2. **运行测试脚本**：
   ```bash
   python factorization_test.py
   ```

3. **查看测试结果**：
   - 测试结果将保存在 `factorization_test_results.csv` 文件中。
   - 日志信息将同时输出到控制台和 `factorization_test.log` 文件中。

## 代码结构详解

### Pollard_rho.py 核心函数

1. **`is_prime(n)`**：$Miller-Rabin$ 素性测试函数。
2. **`pollard_rho(n, c=1)`**：$Pollard-Rho$ 因子寻找函数。
3. **`factorize(n)`**：单进程递归因式分解函数。
4. **`parallel_factorize(n)`**：多进程并行因式分解函数。
5. **`main()`**：主函数，处理命令行输入和输出。

### factorization_test.py 核心函数

1. **`read_and_prepare_data(file_path)`**：读取并准备测试数据。
2. **`run_algorithm(algorithm_file, number)`**：执行指定算法并捕获输出。
3. **`test_single_number(number, pollard_file, naive_file)`**：测试单个数字的因式分解性能。
4. **`generate_csv_output(result, output_file, write_header=False)`**：生成 CSV 格式的测试结果。
5. **`main()`**：主函数，协调整个测试流程。


## 许可证

本项目采用 MIT 许可证，详见 `LICENSE` 文件。

## 参考文献

[1] G. L. Miller, “Riemann’s hypothesis and tests for primality,” J. Comput. Syst. Sci., vol. 13, no. 3, pp. 300–317, Dec. 1976, doi: 10.1016/S0022-0000(76)80043-8.
[2] J. M. Pollard, “A monte carlo method for factorization,” BIT, vol. 15, no. 3, pp. 331–334, Sept. 1975, doi: 10.1007/BF01933667.
[3] M. O. Rabin, “Probabilistic algorithm for testing primality,” J. Number Theory, vol. 12, no. 1, pp. 128–138, Feb. 1980, doi: 10.1016/0022-314X(80)90084-0.