import subprocess


def run_jmeter_test(jmx_file, result_dir):
    # 构建JMeter命令行命令
    # 注意：根据你的JMeter安装路径和需要，命令可能有所不同
    # 这里的例子假设JMeter的bin目录已添加到PATH中
    command = [
        '/home/zhangkexin/jmeter/apache-jmeter-5.6.3/bin/jmeter',
        '-n',  # 非GUI模式
        '-t', jmx_file,  # 指定JMX文件
        '-l', result_file,  # 指定结果文件
        '-e',  # 生成报告
        '-o', '/home/zhangkexin/apitest/'  # 报告输出目录
    ]

    # 运行JMeter命令
    process = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印输出（可选）
    print("JMeter输出:")
    print(process.stdout)

    if process.stderr:
        print("JMeter错误:")
        print(process.stderr)

    # 使用示例


jmx_file = 'your_script.jmx'
result_file = 'your_result.jtl'
run_jmeter_test(jmx_file, result_file)