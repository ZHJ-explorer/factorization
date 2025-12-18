import csv
import logging
import re
import subprocess
import sys
from pathlib import Path

# 配置日志
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('factorization_test.log'),
            logging.StreamHandler()
        ]
    )

# 数据准备模块：读取、验证和排序数据
def read_and_prepare_data(file_path):
    logging.info(f"开始读取数据文件: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        numbers = []
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                # 解析行，提取整数（处理行号前缀格式）
                if '→' in line:
                    # 格式：行号→数字
                    _, num_str = line.split('→', 1)
                    num = int(num_str.strip())
                else:
                    # 格式：纯数字
                    num = int(line.strip())
                numbers.append(num)
            except ValueError as e:
                logging.error(f"第 {line_num} 行数据格式错误: {line}, 错误信息: {e}")
                raise
        
        # 排序数据
        numbers.sort()
        logging.info(f"成功读取并排序 {len(numbers)} 个数字")
        return numbers
    except FileNotFoundError:
        logging.error(f"数据文件未找到: {file_path}")
        raise
    except PermissionError:
        logging.error(f"没有权限读取数据文件: {file_path}")
        raise
    except Exception as e:
        logging.error(f"读取数据文件时发生错误: {e}")
        raise

# 执行算法并捕获输出
def run_algorithm(algorithm_file, number):
    logging.debug(f"执行算法: {algorithm_file}, 数字: {number}")
    try:
        # 构建命令
        cmd = [sys.executable, algorithm_file, str(number)]
        # 执行命令并捕获输出
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"执行算法 {algorithm_file} 失败，数字: {number}, 错误: {e.stderr}")
        raise
    except Exception as e:
        logging.error(f"执行算法 {algorithm_file} 时发生未知错误，数字: {number}, 错误: {e}")
        raise

# 从输出中提取执行时间
def extract_execution_time(output):
    logging.debug(f"从输出中提取执行时间: {output[:100]}...")
    # 匹配 "任务执行时间: X.XXXX秒" 或科学计数法格式 "任务执行时间: X.XXXXXe-XX秒"
    pattern = r'任务执行时间: ([0-9]+(?:\.[0-9]+)?(?:e[-+]?[0-9]+)?)秒'
    match = re.search(pattern, output)
    if match:
        time_str = match.group(1)
        logging.debug(f"提取到时间: {time_str}秒")
        return float(time_str)
    else:
        logging.error(f"无法从输出中提取执行时间: {output}")
        raise ValueError(f"无法从输出中提取执行时间: {output}")

# 测试单个数字
def test_single_number(number, pollard_file, naive_file):
    logging.info(f"测试数字: {number}")
    
    # 执行Pollard's Rho算法5次
    pollard_times = []
    for i in range(5):
        logging.debug(f"执行Pollard's Rho算法第 {i+1} 次，数字: {number}")
        output = run_algorithm(pollard_file, number)
        time_taken = extract_execution_time(output)
        pollard_times.append(time_taken)
    
    # 执行Naive算法1次
    logging.debug(f"执行Naive算法，数字: {number}")
    output = run_algorithm(naive_file, number)
    naive_time = extract_execution_time(output)
    
    return {
        'original_number': number,
        'pollard_times': pollard_times,
        'naive_time': naive_time
    }

# 生成CSV输出文件
def generate_csv_output(results, output_file):
    logging.info(f"生成CSV输出文件: {output_file}")
    try:
        # CSV文件头部
        fieldnames = [
            "Original Number",
            "Pollard's Rho Run 1 Time",
            "Pollard's Rho Run 2 Time",
            "Pollard's Rho Run 3 Time",
            "Pollard's Rho Run 4 Time",
            "Pollard's Rho Run 5 Time",
            "Naive Algorithm Time"
        ]
        
        # 写入CSV文件
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            
            for result in results:
                row = {
                    "Original Number": result['original_number'],
                    "Pollard's Rho Run 1 Time": result['pollard_times'][0],
                    "Pollard's Rho Run 2 Time": result['pollard_times'][1],
                    "Pollard's Rho Run 3 Time": result['pollard_times'][2],
                    "Pollard's Rho Run 4 Time": result['pollard_times'][3],
                    "Pollard's Rho Run 5 Time": result['pollard_times'][4],
                    "Naive Algorithm Time": result['naive_time']
                }
                writer.writerow(row)
        
        logging.info(f"成功生成CSV文件: {output_file}")
    except PermissionError:
        logging.error(f"没有权限写入CSV文件: {output_file}")
        raise
    except Exception as e:
        logging.error(f"生成CSV文件时发生错误: {e}")
        raise

# 验证输出文件
def verify_output_files(file_paths):
    logging.info("验证输出文件")
    try:
        for file_path in file_paths:
            if not Path(file_path).exists():
                logging.error(f"输出文件不存在: {file_path}")
                return False
            
            # 检查文件大小
            if Path(file_path).stat().st_size == 0:
                logging.error(f"输出文件为空: {file_path}")
                return False
            
            # 检查文件格式
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                if not headers:
                    logging.error(f"输出文件没有表头: {file_path}")
                    return False
                # 检查是否有数据行
                if not any(reader):
                    logging.error(f"输出文件没有数据行: {file_path}")
                    return False
        
        logging.info("所有输出文件验证通过")
        return True
    except Exception as e:
        logging.error(f"验证输出文件时发生错误: {e}")
        return False

# 主函数
def main():
    # 设置日志
    setup_logging()
    logging.info("开始因式分解算法性能测试")
    
    try:
        # 配置文件路径
        data_file = "test.txt"
        pollard_file = "Pollard_rho.py"
        naive_file = "Naive_factorization.py"
        output_files = [
            "Pollard_rho_test_results.csv",
            "Naive_factorization_test_results.csv"
        ]
        
        # 1. 数据准备
        numbers = read_and_prepare_data(data_file)
        
        logging.info(f"开始测试所有 {len(numbers)} 个数字")
        
        # 2. 执行测试
        results = []
        for number in numbers:
            try:
                result = test_single_number(number, pollard_file, naive_file)
                results.append(result)
            except Exception as e:
                logging.error(f"测试数字 {number} 时发生错误，跳过该数字: {e}")
                # 可以选择继续测试其他数字
        
        # 3. 生成输出文件
        for output_file in output_files:
            generate_csv_output(results, output_file)
        
        # 4. 验证输出文件
        if verify_output_files(output_files):
            logging.info("因式分解算法性能测试完成，所有输出文件验证通过")
        else:
            logging.error("因式分解算法性能测试完成，但输出文件验证失败")
            sys.exit(1)
        
        logging.info("测试完成")
    except Exception as e:
        logging.error(f"测试过程中发生严重错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()