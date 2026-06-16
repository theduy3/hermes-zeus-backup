---
name: mlops-lifecycle
description: "Umbrella for ML operations lifecycle: model/dataset hub workflows, evaluation, experiment tracking, local/server inference, quantization, and visualization tools."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mlops, huggingface, evaluation, wandb, llama-cpp, vllm, inference, quantization]
---

# MLOps Lifecycle

Use this umbrella for machine-learning operational work: finding/downloading/uploading models or datasets, evaluating LLMs, tracking experiments, running local inference, serving models, and managing quantization or artifacts.

## Hub and artifact management

Use Hugging Face Hub workflows for model/dataset search, download, upload, repo metadata, and tokens. Record repo IDs, revisions, file patterns, and license constraints.

## Evaluation

Use benchmark/evaluation harness workflows for MMLU/GSM8K/etc. Capture model, dataset, prompts/templates, seeds, hardware, and exact command lines.

## Experiment tracking

Use Weights & Biases for runs, sweeps, artifacts, model registry, dashboards, and framework integrations. Verify project/entity/run URLs or IDs.

## Inference and serving

- llama.cpp/GGUF: local CPU/GPU inference, quantization-aware setup, server mode, optimization, and HF Hub model discovery.
- vLLM or other servers: high-throughput OpenAI-compatible serving, batching, tensor parallelism, and deployment diagnostics.

## Verification

Always report exact models, revisions, hardware, command output, ports/endpoints, and benchmark metrics. Do not invent scores or successful runs.