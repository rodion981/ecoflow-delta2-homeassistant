"""EcoFlow API client."""
import hashlib
import hmac
import json
import time
from typing import Any, Dict
import requests

from .const import API_BASE_URL


class EcoFlowAPI:
    """EcoFlow API client."""

    def __init__(self, access_key: str, secret_key: str, device_sn: str, region: str = "eu"):
        """Initialize the API client."""
        self.access_key = access_key
        self.secret_key = secret_key
        self.device_sn = device_sn
        self.base_url = API_BASE_URL[region]
        self.session = requests.Session()

    def _generate_signature(self, params: Dict[str, Any], nonce: str, timestamp: str) -> str:
        """Generate HMAC signature for API request."""
        # Sort parameters
        sorted_params = sorted(params.items())
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        
        # Create signature string
        sign_str = f"{param_str}&accessKey={self.access_key}&nonce={nonce}&timestamp={timestamp}"
        
        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key.encode(),
            sign_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to EcoFlow API."""
        if params is None:
            params = {}
        
        # Add device serial number
        params["sn"] = self.device_sn
        
        # Generate nonce and timestamp
        nonce = str(int(time.time() * 1000))
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature
        signature = self._generate_signature(params, nonce, timestamp)
        
        # Prepare headers
        headers = {
            "accessKey": self.access_key,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": signature,
            "Content-Type": "application/json"
        }
        
        # Make request
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.json()

    def get_device_data(self) -> Dict[str, Any]:
        """Get device data from API."""
        try:
            response = self._make_request("/iot-open/sign/device/quota/all")
            
            if response.get("code") == "0" and response.get("data"):
                return response["data"]
            else:
                raise Exception(f"API error: {response.get('message', 'Unknown error')}")
        except Exception as e:
            raise Exception(f"Failed to get device data: {e}")

    def set_ac_output(self, enabled: bool) -> bool:
        """Enable or disable AC output."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "WN511_SET_AC_ENABLED",
            "params": {
                "enabled": 1 if enabled else 0
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params)
            return response.get("code") == "0"
        except Exception:
            return False

    def set_dc_output(self, enabled: bool) -> bool:
        """Enable or disable DC output."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "DCOUT_CFG",
            "params": {
                "enabled": 1 if enabled else 0
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params)
            return response.get("code") == "0"
        except Exception:
            return False

    def set_xboost(self, enabled: bool) -> bool:
        """Enable or disable X-Boost."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "WN511_SET_XBOOST_ENABLED",
            "params": {
                "xboost": 1 if enabled else 0
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params)
            return response.get("code") == "0"
        except Exception:
            return False

    def set_beeper(self, enabled: bool) -> bool:
        """Enable or disable beeper."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "WN511_SET_BEEP_MODE",
            "params": {
                "flag": 1 if enabled else 0
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params)
            return response.get("code") == "0"
        except Exception:
            return False
