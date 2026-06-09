---
name: mlops-model-workflows
description: "Use when discovering, evaluating, serving, instrumenting, or modifying ML/LLM models: Hugging Face Hub, llama.cpp/GGUF, W&B, live notebooks, and model-behavior surgery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, llm, huggingface, llama-cpp, gguf, wandb, evaluation, notebooks]
    related_skills: []
---

# MLOps Model Workflows

## Overview

This umbrella covers the model-operations lifecycle: discover models/datasets, run local inference, choose GGUF/quants, evaluate and log experiments, use live notebooks for iterative analysis, and perform specialized model-behavior interventions when explicitly requested.

## When to Use

- Search/download/upload Hugging Face models or datasets.
- Run llama.cpp local GGUF inference or inspect available quants.
- Log experiments, sweeps, artifacts, or dashboards with Weights & Biases.
- Use a live Jupyter kernel for iterative ML/data exploration.
- Perform model refusal/behavior analysis or abliteration-style workflows.

## Workflow

1. Identify the task phase: discovery, inference, evaluation, experiment tracking, notebook exploration, or model modification.
2. Check hardware, credentials, and installed commands before starting long jobs.
3. Prefer small smoke tests before full downloads, evaluations, or training-style runs.
4. Capture exact model IDs, revisions, quant names, config files, and metric outputs.
5. Never invent benchmark or experiment numbers; report only real outputs.

## Modes

### Hugging Face Hub
Use `hf` CLI/API for search, download, upload, metadata, and repo operations. Pin model IDs and revisions when reproducibility matters.

### llama.cpp / GGUF
Use llama.cpp for local inference and GGUF quant selection. Inspect available files in the repo and choose quant based on RAM/VRAM constraints.

### vLLM Serving
Use vLLM for high-throughput OpenAI-compatible serving, quantization-aware inference, tensor parallelism, and production-style benchmark smoke tests.

### Evaluation Harnesses
Use lm-eval-harness style workflows for reproducible benchmark runs such as MMLU, GSM8K, HumanEval, and other model-quality checks.

### Computer Vision Models
Use Segment Anything/SAM workflows for zero-shot image segmentation with points, boxes, and masks; verify masks visually or with saved output files.

### W&B
Use W&B for runs, sweeps, artifacts, model registry, and dashboards. Log configs and artifact aliases consistently.

### Live Jupyter Kernel
Use a live kernel for iterative data/ML exploration when repeated cell execution and stateful inspection are more useful than one-off scripts.

### Model Behavior Surgery
Use specialized workflows such as OBLITERATUS only when the user explicitly asks for refusal/behavior intervention and the hardware/model prerequisites are satisfied.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Starting huge downloads without checking disk/RAM/VRAM.
- Mixing model revisions or quant files without recording exact identifiers.
- Reporting benchmark scores from memory or previous runs.
- Using invasive model modification workflows when normal prompting/fine-tuning is the actual task.

## Verification Checklist

- [ ] Hardware and credentials were checked.
- [ ] Exact model/dataset/run/artifact identifiers are captured.
- [ ] A smoke test or real metric output verifies the work.
