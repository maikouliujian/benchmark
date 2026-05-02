import os
import random
import csv
from tabulate import tabulate

file_name = "/Users/qiubenzhang/Downloads/result_1.log"

with open(file_name, 'r', encoding='utf-8') as f, \
        open('result.csv', mode='w', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    # ["input_len", "output_len", "total_req", "batch_size", "freq", "Request_Throughput", "avg_TTFT", "P90_TTFT", "avg_TPOT", "P90_TPOT", "Input_Token_Throughput", "Output_Token_Throughput", "Total_Token_Throughput"]
    row = ["in_len", "out_len", "total_req", "bs", "freq", "Req_QPS", "avg_TTFT", "P90_TTFT", "avg_TPOT", "P90_TPOT",
           "In_QPS", "Out_QPS", "Total_QPS"]
    writer.writerow(row)
    lines = f.readlines()
    avg_ttft = 0
    p90_ttft = 0
    avg_tpot = 0
    p90_tpot = 0
    for line in lines:
        if "bash perf_test.sh" in line:
            task = line.strip().split(' ')
            input_len = task[3]
            output_len = task[4]
            total_req = task[5]
            batch_size = task[6]
            freq = 0 if len(task) < 8 else task[7]

        if "│ TTFT                     │" in line:
            task = line.strip().split("│")
            avg_ttft = task[3].strip().split(" ")[0]
            p90_ttft = task[8].strip().split(" ")[0]

        if "│ TPOT                     │" in line:
            task = line.strip().split("│")
            avg_tpot = task[3].strip().split(" ")[0]
            p90_tpot = task[8].strip().split(" ")[0]

        if "│ Request Throughput       │" in line:
            task = line.strip().split("│")
            concurrency = task[3].strip().split(" ")[0]

        if "│ Input Token Throughput   │" in line:
            task = line.strip().split("│")
            input_throughput = task[3].strip().split(" ")[0]
        if "│ Output Token Throughput  │" in line:
            task = line.strip().split("│")
            output_throughput = task[3].strip().split(" ")[0]

        if "│ Total Token Throughput   │" in line:
            task = line.strip().split("│")
            total_throughput = task[3].strip().split(" ")[0]
            # print([input_len, output_len, total_req, batch_size, freq, concurrency, avg_ttft, p90_ttft, avg_tpot, p90_tpot, input_throughput, output_throughput, total_throughput])
            row = [input_len, output_len, total_req, batch_size, freq, concurrency, avg_ttft, p90_ttft, avg_tpot,
                   p90_tpot, input_throughput, output_throughput, total_throughput]
            writer.writerow(row)

with open('result.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    data = list(reader)
    print(tabulate(data, headers='firstrow'))