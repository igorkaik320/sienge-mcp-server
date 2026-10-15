"""Sienge API Client with HTTP Basic Authentication"""
import os
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()


class SiengeClient:
    """Client for Sienge API with Basic Authentication"""

    def __init__(
        self,
        subdomain: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.subdomain = subdomain or os.getenv("SIENGE_SUBDOMAIN")
        self.username = username or os.getenv("SIENGE_USERNAME")
        self.password = password or os.getenv("SIENGE_PASSWORD")

        if not all([self.subdomain, self.username, self.password]):
            raise ValueError(
                "Missing Sienge credentials. Please set SIENGE_SUBDOMAIN, "
                "SIENGE_USERNAME, and SIENGE_PASSWORD environment variables."
            )

        self.base_url = f"https://api.sienge.com.br/{self.subdomain}/public/api/v1"
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        """Lazy initialization of HTTP client"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                auth=(self.username, self.password),
                headers={"Accept": "application/json"},
                timeout=30.0,
            )
        return self._client

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        """Make a GET request to the Sienge API"""
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, data: Optional[dict] = None, json: Optional[dict] = None) -> dict:
        """Make a POST request to the Sienge API"""
        response = self.client.post(path, data=data, json=json)
        response.raise_for_status()
        return response.json()

    def patch(self, path: str, json: Optional[dict] = None) -> dict:
        """Make a PATCH request to the Sienge API"""
        response = self.client.patch(path, json=json)
        response.raise_for_status()
        return response.json()

    def put(self, path: str, json: Optional[dict] = None) -> dict:
        """Make a PUT request to the Sienge API"""
        response = self.client.put(path, json=json)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Close the HTTP client"""
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
