# LLMBench

A Tool for evaulation the performance of LLM APIs.

# Installation
```bash
git clone ...
cd LLMBench
pip install -e .
```

# Basic Usage


### Example
```bash
llmbench_tokenmark \
--dataset "test1" \
--model test \   # 发起用那个客户端
--num_concurrent_requests 10 \
--timeout 600 \
--max_request_num 1000 \       # test1 数据集中 取1000条数据
--results-dir "result_outputs" \
--extra_params '{}'

```


