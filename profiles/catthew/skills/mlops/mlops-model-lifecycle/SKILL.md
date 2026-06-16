---
name: mlops-model-lifecycle
description: "Use when managing machine-learning model lifecycle tasks: Hub search/download/upload, local inference, LLM serving, evaluation benchmarks, experiment tracking, and vision/audio model utilities."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, huggingface, inference, serving, evaluation, wandb, llama-cpp, vllm]
    related_skills: []
---

# MLOps Model Lifecycle

## Overview

This umbrella covers recurring model-operations tasks from discovery through deployment and evaluation: Hugging Face Hub operations, local GGUF/llama.cpp inference, vLLM serving, benchmark evaluation, W&B experiment tracking, and common model-family utilities when used operationally.

## When to Use

- Find, download, upload, or manage models/datasets on Hugging Face Hub.
- Run a model locally with llama.cpp/GGUF or serve it with vLLM/OpenAI-compatible APIs.
- Benchmark models with lm-eval-harness or similar tools.
- Log, compare, or manage experiments with Weights & Biases.
- Do operational setup/troubleshooting around ML model tools.

## Hub and Artifact Management

Authenticate explicitly for private artifacts. Verify repo type: model, dataset, or Space. Record exact model IDs, revisions, filenames, and local cache/output paths. Avoid giant downloads until disk/GPU needs are checked.

## Local Inference and Serving

For CPU/local inference, prefer GGUF models with llama.cpp. Match quantization level to memory and quality constraints. For vLLM, check GPU memory, tensor parallelism, dtype, max model length, and quantization support. A server is ready only after a real API request succeeds.

## Evaluation and Tracking

Use lm-eval-harness for standard benchmarks. Pin model, revision, prompt/chat template, task list, batch size, and seed where possible. Use W&B for runs, sweeps, artifacts, tables, and registry workflows; confirm project/entity/login before logging.

## Common Pitfalls

1. Version drift: record package versions and model revisions.
2. GPU assumptions: check hardware before selecting settings.
3. Fake readiness: health-check and send a request.
4. Benchmark ambiguity: metrics need task/model/template details.

## Verification Checklist

- [ ] Auth, hardware, disk, and dependencies were checked.
- [ ] Exact model/artifact identifiers and paths were recorded.
- [ ] Inference/serving/evaluation/tracking actions were verified with real output.
- [ ] Final response includes commands/settings and reproducible result locations.
