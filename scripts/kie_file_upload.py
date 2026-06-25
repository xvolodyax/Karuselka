"""Kie.ai File Upload API — https://docs.kie.ai/file-upload-api/quickstart"""

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError as exc:
    raise SystemExit("Install requests: pip install requests") from exc

from kie_common import KieTaskClient

DEFAULT_UPLOAD_BASE = "https://kieai.redpandaai.co"


class KieFileUploadClient(KieTaskClient):
    """Upload files to Kie CDN; same KIE_API_KEY as image/video generation."""

    def __init__(self, api_key: str | None = None, upload_base: str | None = None, **kwargs: Any) -> None:
        super().__init__(api_key=api_key, **kwargs)
        self.upload_base = (
            upload_base or os.getenv("KIE_FILE_UPLOAD_BASE") or DEFAULT_UPLOAD_BASE
        ).rstrip("/")

    def _extract_file_url(self, body: dict) -> str:
        if not body.get("success") and body.get("code") != 200:
            raise RuntimeError(f"Kie upload failed: {body.get('msg', body)}")
        data = body.get("data") or {}
        url = data.get("fileUrl") or data.get("downloadUrl")
        if not url or not str(url).startswith("http"):
            raise RuntimeError(f"No fileUrl in response: {body}")
        return str(url)

    def upload_stream(
        self,
        local_path: Path,
        upload_path: str = "carusel",
        file_name: str | None = None,
    ) -> dict[str, Any]:
        """File Stream Upload — локальные PNG/MP4 (рекомендуется для слайдов)."""
        local_path = Path(local_path)
        if not local_path.is_file():
            raise FileNotFoundError(local_path)

        name = file_name or local_path.name
        mime, _ = mimetypes.guess_type(name)

        # Session inherits Content-Type: application/json from KieTaskClient — must remove
        # so requests can set multipart/form-data boundary.
        saved_ct = self.session.headers.pop("Content-Type", None)
        try:
            with local_path.open("rb") as fh:
                files = {"file": (name, fh, mime or "application/octet-stream")}
                data: dict[str, str] = {"uploadPath": upload_path, "fileName": name}
                resp = self.session.post(
                    f"{self.upload_base}/api/file-stream-upload",
                    files=files,
                    data=data,
                    timeout=300,
                )
        finally:
            if saved_ct is not None:
                self.session.headers["Content-Type"] = saved_ct
        resp.raise_for_status()
        body = resp.json()
        url = self._extract_file_url(body)
        body["publicUrl"] = url
        return body

    def upload_from_url(
        self,
        file_url: str,
        upload_path: str = "carusel",
        file_name: str | None = None,
    ) -> dict[str, Any]:
        """URL File Upload — видео/картинка уже на HTTPS (например результат Grok)."""
        payload: dict[str, str] = {
            "fileUrl": file_url,
            "uploadPath": upload_path,
        }
        if file_name:
            payload["fileName"] = file_name

        resp = self.session.post(
            f"{self.upload_base}/api/file-url-upload",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        body = resp.json()
        url = self._extract_file_url(body)
        body["publicUrl"] = url
        return body

    def upload_base64(
        self,
        local_path: Path,
        upload_path: str = "carusel",
        file_name: str | None = None,
    ) -> dict[str, Any]:
        """Base64 Upload — только для файлов ≤10MB (fallback)."""
        local_path = Path(local_path)
        mime, _ = mimetypes.guess_type(local_path.name)
        mime = mime or "application/octet-stream"
        raw = local_path.read_bytes()
        if len(raw) > 10 * 1024 * 1024:
            raise ValueError(f"File too large for base64 ({len(raw)} bytes), use stream upload")
        b64 = base64.b64encode(raw).decode("ascii")
        data_url = f"data:{mime};base64,{b64}"
        name = file_name or local_path.name

        resp = self.session.post(
            f"{self.upload_base}/api/file-base64-upload",
            json={
                "base64Data": data_url,
                "uploadPath": upload_path,
                "fileName": name,
            },
            timeout=300,
        )
        resp.raise_for_status()
        body = resp.json()
        url = self._extract_file_url(body)
        body["publicUrl"] = url
        return body

    def upload_local(self, local_path: Path, upload_path: str = "carusel") -> str:
        """Умный выбор: stream для локальных файлов."""
        result = self.upload_stream(local_path, upload_path=upload_path, file_name=local_path.name)
        return result["publicUrl"]
