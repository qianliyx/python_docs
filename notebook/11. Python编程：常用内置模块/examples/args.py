import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--input_file", help="input file path")
parser.add_argument("-o", "--output_file", help="output file path")
args = parser.parse_args()

print(f"-f或者--input_file的命令行参数是：{args.input_file}")
print(f"-o或者--output_file的命令行参数是：{args.output_file}")