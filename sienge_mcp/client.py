"""Sienge API Client with HTTP Basic Authentication, Logging and Cache"""
import os
import logging
import time
from typing import Optional, Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SiengeClient:
    """Client for Sienge API with Basic Authentication, Logging and Cache"""

    def __init__(
        self,
        subdomain: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        read_only: bool = False,
    ):
        self.subdomain = subdomain or os.getenv("SIENGE_SUBDOMAIN")
        self.username = username or os.getenv("SIENGE_USERNAME")
        self.password = password or os.getenv("SIENGE_PASSWORD")
        self.read_only = read_only or os.getenv("READ_ONLY", "false").lower() == "true"

        if not all([self.subdomain, self.username, self.password]):
            raise ValueError(
                "Missing Sienge credentials. Please set SIENGE_SUBDOMAIN, "
                "SIENGE_USERNAME, and SIENGE_PASSWORD environment variables."
            )

        self.base_url = f"https://api.sienge.com.br/{self.subdomain}/public/api/v1"
        self._client: Optional[httpx.Client] = None
        
        # Cache for creditor and company names
        self._creditor_cache: Dict[int, str] = {}
        self._company_cache: Dict[int, str] = {}

        if self.read_only:
            logger.info("Sienge client initialized in READ_ONLY mode")

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

    def _log_request(self, method: str, path: str, params: Optional[dict] = None, 
                     json_data: Optional[dict] = None, status_code: int = None, 
                     duration: float = None, result_count: int = None):
        """Log API request with sanitized parameters"""
        # Sanitize params to hide credentials
        safe_params = {}
        if params:
            for k, v in params.items():
                if 'password' in k.lower() or 'senha' in k.lower():
                    safe_params[k] = "***"
                else:
                    safe_params[k] = v
        
        log_msg = f"Sienge API: {method} {path}"
        if safe_params:
            log_msg += f" params={safe_params}"
        if status_code:
            log_msg += f" status={status_code}"
        if duration:
            log_msg += f" duration={duration:.2f}s"
        if result_count is not None:
            log_msg += f" results={result_count}"
        
        logger.info(log_msg)

    def _compact_response(self, data: Any) -> Any:
        """Remove verbose fields from response"""
        if isinstance(data, dict):
            # Remove verbose fields
            data_copy = data.copy()
            data_copy.pop('links', None)
            data_copy.pop('tenantUrl', None)
            
            # Recursively compact nested structures
            for key, value in data_copy.items():
                if isinstance(value, (dict, list)):
                    data_copy[key] = self._compact_response(value)
            
            return data_copy
        elif isinstance(data, list):
            return [self._compact_response(item) for item in data]
        return data

    def get(self, path: str, params: Optional[dict] = None, compact: bool = True) -> dict:
        """Make a GET request to the Sienge API"""
        start_time = time.time()
        try:
            response = self.client.get(path, params=params)
            duration = time.time() - start_time
            response.raise_for_status()
            
            data = response.json()
            result_count = data.get('resultSetMetadata', {}).get('count', len(data)) if isinstance(data, dict) else len(data)
            
            self._log_request("GET", path, params, status_code=response.status_code, 
                             duration=duration, result_count=result_count)
            
            if compact:
                data = self._compact_response(data)
            
            return data
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Sienge API GET {path} failed after {duration:.2f}s: {e}")
            raise

    def post(self, path: str, data: Optional[dict] = None, json: Optional[dict] = None) -> dict:
        """Make a POST request to the Sienge API"""
        if self.read_only:
            raise PermissionError("WRITE operation blocked: client is in READ_ONLY mode")
        
        start_time = time.time()
        try:
            response = self.client.post(path, data=data, json=json)
            duration = time.time() - start_time
            response.raise_for_status()
            
            self._log_request("POST", path, json_data=json, status_code=response.status_code, duration=duration)
            
            return response.json()
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Sienge API POST {path} failed after {duration:.2f}s: {e}")
            raise

    def patch(self, path: str, json: Optional[dict] = None) -> dict:
        """Make a PATCH request to the Sienge API"""
        if self.read_only:
            raise PermissionError("WRITE operation blocked: client is in READ_ONLY mode")
        
        start_time = time.time()
        try:
            response = self.client.patch(path, json=json)
            duration = time.time() - start_time
            response.raise_for_status()
            
            self._log_request("PATCH", path, json_data=json, status_code=response.status_code, duration=duration)
            
            return response.json()
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Sienge API PATCH {path} failed after {duration:.2f}s: {e}")
            raise

    def put(self, path: str, json: Optional[dict] = None) -> dict:
        """Make a PUT request to the Sienge API"""
        if self.read_only:
            raise PermissionError("WRITE operation blocked: client is in READ_ONLY mode")
        
        start_time = time.time()
        try:
            response = self.client.put(path, json=json)
            duration = time.time() - start_time
            response.raise_for_status()
            
            self._log_request("PUT", path, json_data=json, status_code=response.status_code, duration=duration)
            
            return response.json()
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Sienge API PUT {path} failed after {duration:.2f}s: {e}")
            raise

    def close(self):
        """Close the HTTP client"""
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
