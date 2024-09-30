import os
import plotly.express as px
import plotly.io as pio
import pandas as pd

from llmbench.report import Report


class CalcStatic:
    """
    生成html，性能测试报告
    """
    def __init__(self, report: Report):
        self.report = report
        self.token_jsonl_file = self.report.filename  # path to the individual responses json file
        self.output_dir = self.report.result_dir
        df = pd.read_json(self.token_jsonl_file, encoding="utf-8", lines=True)
        self.valid_df = df[(df["error_code"].isna())]
        self.input_output_token_info = ""
        self.ttfts_pic = None
        self.latency_pic = None

    def run(self):
        self.pic_to_ttft()
        self.pic_to_token_latencies()
        token_df = self.report.token_df.rename(
            index={"ttft_s": "首 Token 延迟", "inter_token_latency_s": "内token延迟", "end_to_end_latency_s": "端到端延迟",
                   "number_input_tokens": "输入token量", "request_output_throughput_token_per_s": "token吞吐量",
                   "number_output_tokens": "输出token量"})
        self.report.report_df.set_index("测试模型", inplace=True)
        summary_df = self.report.report_df.T

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>llmbench report</title>
        </head>
        <body>
            <div>
                <h1 style='text-align:center;'>LlmBench 性能测试报告</h1> 
                <h5 style='text-align:center;'>CMRI-testGroup</h5> 
            </div>
            <h1>概览：</h1>
            <hr />
            <div id="desc">
                <h2> 本次测试信息 </h2>
                {summary_df.to_html()}
            </div>
            </br>
            <div id="desc">
                {token_df.to_html()}
            <div>
                <h4>{self.input_output_token_info}</h5>
            </div>
                <h6>注:</br>
                    内token延迟: 可能表示在两个标记之间（token）的网络延迟，这有助于了解数据在网络中的传输速度。</br>
                    端到端延迟: 是端到端的总延迟，它包括了所有传输和处理的时间，是衡量整个通信链路性能的重要指标。</br>
                    输入token量: 指的是输入到系统中的数据量(token)。</br>
                    输出token量: 则是系统输出的数据量(token)。</br>
                    token吞吐量：吞吐量，即每秒针对所有请求生成的 token 数。以上六个指标都针对单个请求，而吞吐量是针对所有并发请求的。
                </h6>
            </div>
            <h1>详情：</h1>
            <hr />
            <div>
                <h3>首 Token 延迟:</h3>
                <h6>注：即从输入到输出第一个 token 的延迟。在在线的流式应用中，TTFT 是最重要的指标，因为它决定了用户体验。</h6>
                {pio.to_html(self.ttfts_pic, full_html=False)}
            </div>
            <div>
                <h3>延迟:</h3>
                <h6>注：即从输入到输出最后一个 token 的延迟。 Latency = (TTFT) + (TPOT) * (the number of tokens to be generated). Latency 可以转换为 Tokens Per Second (TPS)：TPS = (the number of tokens to be generated) / Latency。</h6>
                {pio.to_html(self.latency_pic, full_html=False)}
            </div>
        </body>""" + """
        <style>
            .dataframe {border-collapse: collapse !important;}
        </style>
        </html>
        """
        with open(os.path.join(self.output_dir, "report.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    def pic_to_ttft(self):
        final_df = pd.DataFrame()
        final_df["number_input_tokens"] = self.valid_df["number_input_tokens"]
        final_df["number_output_tokens"] = self.valid_df["number_output_tokens"]
        final_df["ttft_s"] = self.valid_df["ttft_s"]
        final_df["end_to_end_latency_s"] = self.valid_df["end_to_end_latency_s"]
        final_df["generation_throughput"] = self.valid_df["request_output_throughput_token_per_s"]

        mean_tokens_in = final_df["number_input_tokens"].mean()
        mean_tokens_out = self.valid_df["number_output_tokens"].mean()
        self.input_output_token_info = f"平均输入token数: {mean_tokens_in}.</br> 平均输出token数: {mean_tokens_out}."
        self.ttfts_pic = px.scatter(final_df, x="number_input_tokens", y="ttft_s")

    def pic_to_token_latencies(self):
        all_token_latencies = self.valid_df['end_to_end_latency_s'].apply(pd.Series).stack()
        all_token_latencies = all_token_latencies.reset_index(drop=True)
        self.latency_pic = px.scatter(all_token_latencies)


if __name__ == "__main__":
    CalcStatic(
        r"D:\code\llm_bench\llmbench\src\llmbench\cli\results\test_token_benchmark\20240920181416\test_token_benchmark.jsonl",
        r"D:\code\llm_bench\llmbench\src\llmbench\cli\results\test_token_benchmark\20240920181416").run()
