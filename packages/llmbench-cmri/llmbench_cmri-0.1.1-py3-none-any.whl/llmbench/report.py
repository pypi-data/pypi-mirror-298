"""
@author:cmcc
@file: report.py
@time: 2024/9/1 20:50
"""
import json
import re
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Iterable
import numpy as np
import pandas as pd
from llmbench.common.constants import METRICS
from llmbench.utils import flatten_dict, convert_numpy


class Report:

    def __init__(self, model: str, output_dir: str, **kwargs):
        self.model = model
        filename = re.sub(r"-{2,}", "-",
                          re.sub(r"[^\w\d-]+", "-", f"{model}_token_benchmark"))
        if output_dir is None or len(output_dir) == 0 or not Path(output_dir).exists():
            output_dir = os.getcwd() + "/results/" + filename + "/" + datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            output_dir += "/" + filename + "/" + datetime.now().strftime("%Y%m%d%H%M%S")
        results_dir = Path(output_dir)
        self.result_dir = results_dir
        if not results_dir.exists():
            results_dir.mkdir(parents=True)
        elif not results_dir.is_dir():
            raise ValueError(f"{results_dir} is not a directory")
        self.filename = results_dir / f"{model}_token_benchmark.jsonl"
        self.filename_summary = results_dir / f"{model}_token_benchmark_summary.json"
        self.token_df = None
        self.report_df = None
        self.report_info = {}
        self.print_exec_info: bool = True if os.environ.get("print_exec_info", "on") == "on" else False
        self.start_t = kwargs.get("start_t")

    def save_result(self, results: List[Dict], last=False):
        if not results:
            return
        data = []
        for result in results:
            data.append(json.dumps(flatten_dict(result), ensure_ascii=False))
        with open(self.filename, "a+") as f:
            data = "\n".join(data) + "\n"
            f.write(data)
        self.calc_summary(last)

    def calc_summary(self, last=False):
        def flatten(item):
            for sub_item in item:
                if isinstance(sub_item, Iterable) and not isinstance(sub_item, str):
                    yield from flatten(sub_item)
                else:
                    yield sub_item
        df = pd.read_json(self.filename, orient="records", lines=True)
        start_time = df[METRICS.START_TIME_M].min()
        end_time = df[METRICS.END_TIME_M].max()
        df_without_errored_req = df[df[METRICS.ERROR_CODE].isna()]
        # 分位数
        df_calc = df_without_errored_req[[
            METRICS.TTFT, METRICS.INTER_TOKEN_LAT, METRICS.E2E_LAT,
            METRICS.REQ_OUTPUT_THROUGHPUT, METRICS.NUM_INPUT_TOKENS, METRICS.NUM_OUTPUT_TOKENS]]
        df_calc.loc[:, :] = df_calc.replace('', np.nan)
        df_calc = df_calc.apply(pd.to_numeric, errors='coerce')
        quantiles = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        quantiles_df = df_calc.quantile(quantiles).transpose()
        quantiles_df.columns = [f'P{int(q * 100)}' for q in quantiles]
        # 计算其他统计量
        stats = {
            'mean': df_calc.mean(),
            'std': df_calc.std(),
            'max': df_calc.max(),
            'min': df_calc.min()
        }
        stats_df = pd.DataFrame(stats)
        # 合并所有统计量到一个表格
        df_result = pd.concat([stats_df, quantiles_df], axis=1)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', None)
        if self.print_exec_info:
            print("==" * 80)
            print(df_result)
        if last:
            self.token_df = df_result
        ret = {}
        for index, row in df_result.iterrows():
            for col in df_result.columns:
                ret[f"{index}_{col}"] = row[col]
        ret[METRICS.NUM_REQ_STARTED] = df.shape[0]
        ret[METRICS.TOTAL_COST_TIME] = end_time - start_time
        if self.print_exec_info:
            print("=="*80)
            print(f"model name: {self.model}")
            print(f"start_time: {df['start_time'].min()}")
            print(f"end_time: {df['end_time'].max()}")
            print(f"total cost time: {end_time - start_time}")
        error_codes = df[METRICS.ERROR_CODE].dropna()
        num_errors = len(error_codes)
        ret[METRICS.ERROR_RATE] = num_errors / df.shape[0] if df.shape[0] else 0
        ret[METRICS.NUM_ERRORS] = num_errors
        if self.print_exec_info:
            print(f"Number Of Errored Requests: {num_errors}")
        error_code_frequency = dict(error_codes.value_counts())
        if num_errors:
            error_code_frequency = dict(error_codes.value_counts())
            print("Error Code Frequency")
            print(convert_numpy(error_code_frequency))
        ret[METRICS.ERROR_CODE_FREQ] = convert_numpy(error_code_frequency)
        overall_output_throughput = df_without_errored_req[METRICS.NUM_OUTPUT_TOKENS].sum() / (end_time - start_time)
        ret[METRICS.OUTPUT_THROUGHPUT] = overall_output_throughput
        num_completed_requests = len(df_without_errored_req)
        num_completed_requests_per_min = (num_completed_requests / (end_time - start_time) * 60)
        if self.print_exec_info:
            print(f"Overall Output Throughput: {overall_output_throughput}")
            print(f"Number Of Completed Requests: {num_completed_requests}")
            print(f"Completed Requests Per Minute: {num_completed_requests_per_min}")
            print("==" * 80)
        ret[METRICS.NUM_COMPLETED_REQUESTS] = num_completed_requests
        ret[METRICS.COMPLETED_REQUESTS_PER_MIN] = num_completed_requests_per_min

        with open(self.filename_summary, "w") as f:
            f.write(json.dumps(flatten_dict(convert_numpy(ret)), indent=4, ensure_ascii=False))

        if last:
            self.report_info.update({
                "测试模型": [self.model], "开始时间": [df['start_time'].min()], "结束时间": [df['end_time'].max()],
                "总时间花费": [end_time - start_time], "错误请求数": [num_errors],
                "总体输出吞吐量": [overall_output_throughput],
                "完成请求的数量": [num_completed_requests],
                "每分钟的请求数": [num_completed_requests_per_min],
                "执行总耗时": [time.time() - self.start_t]
            })
        self.report_df = pd.DataFrame(self.report_info)
