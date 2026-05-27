# Codex Stream TypeError: 'NoneType' object is not iterable

Observed on `chatgpt.com/backend-api/codex` with `gpt-5.5` during peak hours (6-7pm PDT window, May 2026).

## Symptom

Cron jobs using `openai-codex` provider fail with:

```
agent.conversation_loop: API call failed (attempt 1/3)
error_type=TypeError
summary='NoneType' object is not iterable
agent.conversation_loop: Non-retryable client error: 'NoneType' object is not iterable
```

No retry — TypeError is classified as `is_local_validation_error` (conversation_loop.py:2826), which triggers immediate abort.

## Root Cause

The OpenAI SDK's Responses API stream parser raises `TypeError` when the Codex backend emits a malformed SSE frame. This happens in `run_codex_create_stream_fallback()` (`agent/codex_runtime.py`) during `for event in stream_or_response:` — the SDK's internal `__next__` tries to iterate over `None`.

## Fix

Convert `TypeError` to `RuntimeError` at the fallback boundary so the upstream retry loop treats it as retryable:

```python
except TypeError as exc:
    logger.warning(
        "Codex fallback stream raised TypeError; converting to retryable RuntimeError. "
        "error=%s %s", exc, agent._client_log_context(),
    )
    raise RuntimeError(
        f"Codex Responses fallback stream: {exc}. "
        f"Retrying with backoff/fallback."
    ) from exc
```

This lets the retry loop apply backoff, credential rotation, or provider fallback instead of aborting immediately.

## File: `agent/codex_runtime.py`

- `run_codex_stream()` — primary path. Catches TypeError at line 274 together with httpx transport errors. On failure, retries once then falls back to `run_codex_create_stream_fallback()`.
- `run_codex_create_stream_fallback()` — the gap was here. Had `try/finally` but no `except TypeError`. Iteration inside `for event in stream_or_response:` could raise TypeError that propagated uncaught.