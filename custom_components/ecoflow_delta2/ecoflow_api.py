"""EcoFlow API client."""
import hashlib
import hmac
import json
import time
import logging
from datetime import datetime
from typing import Any, Dict
import requests

from .const import API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class EcoFlowAPI:
    """EcoFlow API client."""

    def __init__(self, access_key: str, secret_key: str, device_sn: str, region: str = "eu"):
        """Initialize the API client."""
        self.access_key = access_key
        self.secret_key = secret_key
        self.device_sn = device_sn
        self.base_url = API_BASE_URL[region]
        self.session = requests.Session()

    def _generate_signature(self, params: Dict[str, Any], nonce: str, timestamp: str, method: str = "GET") -> str:
        """Generate HMAC signature for API request."""
        if method == "GET":
            # GET: only sn + accessKey + nonce + timestamp
            sign_str = f"sn={params['sn']}&accessKey={self.access_key}&nonce={nonce}&timestamp={timestamp}"
        else:
            # POST: try including cmdCode in signature
            # Format: sn + cmdCode + accessKey + nonce + timestamp
            if 'cmdCode' in params:
                sign_str = f"sn={params['sn']}&cmdCode={params['cmdCode']}&accessKey={self.access_key}&nonce={nonce}&timestamp={timestamp}"
            else:
                sign_str = f"sn={params['sn']}&accessKey={self.access_key}&nonce={nonce}&timestamp={timestamp}"
        
        _LOGGER.debug(f"Sign string for {method}: {sign_str}")
        
        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None, method: str = "GET") -> Dict[str, Any]:
        """Make authenticated request to EcoFlow API."""
        if params is None:
            params = {}
        
        # Add device serial number if not present
        if "sn" not in params:
            params["sn"] = self.device_sn
        
        # Generate nonce and timestamp according to EcoFlow API requirements
        # Nonce: 6-digit random number
        # Timestamp: milliseconds (not seconds!)
        import random
        
        nonce = str(random.randint(100000, 999999))  # 6-digit random number
        timestamp = str(int(time.time() * 1000))     # milliseconds
        
        _LOGGER.debug(f"Generated nonce: {nonce}, timestamp: {timestamp}")
        
        # Generate signature
        signature = self._generate_signature(params, nonce, timestamp, method)
        
        # Log for debugging
        _LOGGER.debug(f"Request to {endpoint} ({method})")
        _LOGGER.debug(f"Params: {params}")
        _LOGGER.debug(f"Generated signature: {signature}")
        
        # Prepare headers
        headers = {
            "accessKey": self.access_key,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": signature,
        }
        
        # Make request
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                # For GET requests, add sn as query parameter
                response = self.session.get(url, params={"sn": params["sn"]}, headers=headers, timeout=10)
            else:
                # For POST requests, send as JSON body
                headers["Content-Type"] = "application/json"
                response = self.session.post(url, json=params, headers=headers, timeout=10)
            
            response.raise_for_status()
            
            result = response.json()
            _LOGGER.debug(f"Response: {result}")
            
            return result
        except Exception as e:
            _LOGGER.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                _LOGGER.error(f"Response status: {e.response.status_code}")
                _LOGGER.error(f"Response body: {e.response.text}")
            raise

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
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
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
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
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
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
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
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
            return response.get("code") == "0"
        except Exception:
            return False

    def set_max_charge_soc(self, soc: int) -> bool:
        """Set maximum charge level (50-100%)."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "WN511_SET_BAT_MAX_CAP",
            "params": {
                "maxChgSoc": soc
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
            return response.get("code") == "0"
        except Exception:
            return False

    def set_min_discharge_soc(self, soc: int) -> bool:
        """Set minimum discharge level (0-30%)."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "WN511_SET_BAT_MIN_CAP",
            "params": {
                "minDsgSoc": soc
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
            return response.get("code") == "0"
        except Exception:
            return False

    def set_ac_charge_power(self, watts: int) -> bool:
        """Set AC charging power limit (200-1200W)."""
        params = {
            "sn": self.device_sn,
            "cmdCode": "WN511_SET_AC_CHG_WATTS",
            "params": {
                "chgWatts": watts
            }
        }
        
        try:
            response = self._make_request("/iot-open/sign/device/quota", params, method="POST")
            return response.get("code") == "0"
        except Exception:
            return False

