"""Config flow for EcoFlow Delta 2 integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .ecoflow_api import EcoFlowAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("access_key"): cv.string,
        vol.Required("secret_key"): cv.string,
        vol.Required("device_sn"): cv.string,
        vol.Required("region", default="eu"): vol.In(["eu", "us"]),
    }
)


async def validate_input(hass: HomeAssistant, data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = EcoFlowAPI(
        data["access_key"],
        data["secret_key"],
        data["device_sn"],
        data["region"]
    )

    # Test the connection
    try:
        device_data = await hass.async_add_executor_job(api.get_device_data)
        if not device_data:
            raise Exception("No data returned from device")
    except Exception as e:
        raise Exception(f"Cannot connect to EcoFlow API: {e}")

    return {"title": f"EcoFlow Delta 2 ({data['device_sn']})"}


class EcoFlowDelta2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EcoFlow Delta 2."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Exception as e:
                _LOGGER.exception("Unexpected exception: %s", e)
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input["device_sn"])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
