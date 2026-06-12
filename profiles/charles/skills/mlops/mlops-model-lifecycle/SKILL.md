---
name: mlops-model-lifecycle
description: "Use when working across the ML model lifecycle: Hub discovery/download/upload, local inference/serving, benchmarking/evaluation, experiment tracking, and model-specific tooling."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, huggingface, inference, evaluation, wandb, llama-cpp, vllm]
    related_skills: []
---

# MLOps Model Lifecycle

## Overview

This umbrella covers the practical lifecycle around ML/LLM models: finding artifacts, running local inference, serving models, evaluating quality, and tracking experiments. Detailed tool packages are preserved under `references/source-packages/`.

## When to Use

- Search, download, upload, or inspect Hugging Face Hub assets.
- Run local GGUF inference with llama.cpp or serve models with vLLM.
- Run benchmark suites such as lm-eval-harness.
- Track experiments, sweeps, artifacts, dashboards, and model registry entries with W&B.
- Use model-specific workflows such as Segment Anything or AudioCraft.

## Workflow Map

1. **Discover/get assets:** Hugging Face Hub.
2. **Run inference locally:** llama.cpp for GGUF/local CPU/GPU paths; vLLM for high-throughput OpenAI-compatible serving.
3. **Evaluate:** lm-eval-harness and task-specific test sets.
4. **Track:** Weights & Biases for runs, sweeps, artifacts, and dashboards.
5. **Specialized models:** Segment Anything and AudioCraft references.

## Verification Checklist

- [ ] Model artifact, revision, and license/source verified.
- [ ] Hardware/VRAM constraints checked before heavy runs.
- [ ] Evaluation or serving endpoint tested with real output.
