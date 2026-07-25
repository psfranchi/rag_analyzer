"""Ollama HTTP client for generation and embeddings."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)

GENERATE_TIMEOUT = (5, 120)
EMBED_TIMEOUT = (5, 60)


class OllamaError(Exception):
    """Base error for Ollama client failures."""


class OllamaConnectionError(OllamaError):
    """Network / connection / timeout talking to Ollama."""


class OllamaHTTPError(OllamaError):
    """Non-success HTTP response or unexpected JSON body."""


class OllamaClient:
    """Thin wrapper around Ollama `/api/generate` and `/api/embeddings`."""

    def __init__(
        self,
        settings: Settings | None = None,
        *,
        base_url: str | None = None,
        analysis_model: str | None = None,
        embedding_model: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        if settings is None and (
            base_url is None or analysis_model is None or embedding_model is None
        ):
            settings = get_settings()
        self.base_url = (base_url or (settings.ollama_url if settings else "")).rstrip("/")
        self.analysis_model = analysis_model or (settings.analysis_model if settings else "")
        self.embedding_model = embedding_model or (settings.embedding_model if settings else "")
        if not self.base_url:
            raise ValueError("Ollama base_url is required")
        self._session = session or requests.Session()

    def generate(
        self,
        prompt: str,
        *,
        model: str | None = None,
        format: str | None = None,
    ) -> str:
        used_model = model or self.analysis_model
        url = f"{self.base_url}/api/generate"
        payload: dict[str, Any] = {
            "model": used_model,
            "prompt": prompt,
            "stream": False,
        }
        if format is not None:
            payload["format"] = format

        started = time.perf_counter()
        try:
            response = self._session.post(url, json=payload, timeout=GENERATE_TIMEOUT)
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise OllamaConnectionError(
                f"Ollama generate connection failed model={used_model} url={url}: {exc}"
            ) from exc

        latency_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "ollama generate model=%s prompt_len=%s latency_ms=%.1f status=%s",
            used_model,
            len(prompt),
            latency_ms,
            response.status_code,
        )

        if response.status_code >= 400:
            raise OllamaHTTPError(
                f"Ollama generate HTTP {response.status_code} model={used_model}: {response.text[:500]}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise OllamaHTTPError(f"Ollama generate returned non-JSON model={used_model}") from exc

        text = body.get("response")
        if not isinstance(text, str):
            raise OllamaHTTPError(
                f"Ollama generate missing response string model={used_model} keys={list(body.keys())}"
            )
        return text

    def embed(self, text: str, *, model: str | None = None) -> list[float]:
        used_model = model or self.embedding_model
        url = f"{self.base_url}/api/embeddings"
        payload = {"model": used_model, "prompt": text}

        started = time.perf_counter()
        try:
            response = self._session.post(url, json=payload, timeout=EMBED_TIMEOUT)
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise OllamaConnectionError(
                f"Ollama embed connection failed model={used_model} url={url}: {exc}"
            ) from exc

        latency_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "ollama embed model=%s prompt_len=%s latency_ms=%.1f status=%s",
            used_model,
            len(text),
            latency_ms,
            response.status_code,
        )

        if response.status_code >= 400:
            raise OllamaHTTPError(
                f"Ollama embed HTTP {response.status_code} model={used_model}: {response.text[:500]}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise OllamaHTTPError(f"Ollama embed returned non-JSON model={used_model}") from exc

        vector = body.get("embedding")
        if vector is None and isinstance(body.get("embeddings"), list) and body["embeddings"]:
            vector = body["embeddings"][0]
        if not isinstance(vector, list) or not vector:
            raise OllamaHTTPError(
                f"Ollama embed missing embedding list model={used_model} keys={list(body.keys())}"
            )
        return [float(x) for x in vector]
