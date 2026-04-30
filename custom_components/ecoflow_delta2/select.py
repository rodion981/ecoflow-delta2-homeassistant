"""Select platform for EcoFlow Delta 2 - dropdown settings."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


# Timeout options in seconds (converted to minutes for display)
SCREEN_TIMEOUT_OPTIONS = {
    "never": {"value": 0, "label": "Never"},
    "10sec": {"value": 10, "label": "10 seconds"},
    "30sec": {"value": 30, "label": "30 seconds"},
    "1min": {"value": 60, "label": "1 minute"},
    "5min": {"value": 300, "label": "5 minutes"},
    "30min": {"value": 1800, "label": "30 minutes"},
}

AC_TIMEOUT_OPTIONS = {
    "never": {"value": 0, "label": "Never"},
    "30min": {"value": 30, "label": "30 minutes"},
    "1hr": {"value": 60, "label": "1 hour"},
    "2hr": {"value": 120, "label": "2 hours"},
    "3hr": {"value": 180, "label": "3 hours"},
    "4hr": {"value": 240, "label": "4 hours"},
    "6hr": {"value": 360, "label": "6 hours"},
    "12hr": {"value": 720, "label": "12 hours"},
    "24hr": {"value": 1440, "label": "24 hours"},
}

DC_TIMEOUT_OPTIONS = {
    "never": {"value": 0, "label": "Never"},
    "30min": {"value": 30, "label": "30 minutes"},
    "1hr": {"value": 60, "label": "1 hour"},
    "2hr": {"value": 120, "label": "2 hours"},
    "3hr": {"value": 180, "label": "3 hours"},
    "4hr": {"value": 240, "label": "4 hours"},
    "6hr": {"value": 360, "label": "6 hours"},
    "12hr": {"value": 720, "label": "12 hours"},
}

SELECT_TYPES = {
    "screen_timeout": {
        "name": "Screen Timeout",
        "key": "pd.lcdOffSec",
        "options": SCREEN_TIMEOUT_OPTIONS,
        "icon": "mdi:monitor-off",
        "command": "set_screen_timeout",
        "cmd_code": "WN511_SET_LCD_TIMEOUT",
        "param_name": "lcdTime",
    },
    "ac_timeout": {
        "name": "AC Timeout",
        "key": "pd.standByMode",
        "options": AC_TIMEOUT_OPTIONS,
        "icon": "mdi:power-plug-off",
        "command": "set_ac_timeout",
        "cmd_code": "WN511_SET_AC_STANDBY_TIME",
        "param_name": "standByMode",
    },
    "dc_timeout": {
        "name": "DC Timeout",
        "key": "mppt.dcChgCurrent",
        "options": DC_TIMEOUT_OPTIONS,
        "icon": "mdi:car-battery",
        "command": "set_dc_timeout",
        "cmd_code": "WN511_SET_DC_STANDBY_TIME",
        "param_name": "standByMode",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EcoFlow Delta 2 select entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    
    entities = []
    for select_type, select_info in SELECT_TYPES.items():
        entities.append(
            EcoFlowDelta2Select(
                coordinator,
                api,
                entry,
                select_type,
                select_info,
            )
        )
    
    async_add_entities(entities)


class EcoFlowDelta2Select(CoordinatorEntity, SelectEntity):
    """Representation of an EcoFlow Delta 2 select entity."""

    def __init__(self, coordinator, api, entry, select_type, select_info):
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._api = api
        self._select_type = select_type
        self._select_info = select_info
        self._attr_unique_id = f"{entry.data['device_sn']}_{select_type}"
        self._attr_icon = select_info["icon"]
        self._attr_has_entity_name = True
        self._attr_translation_key = select_type
        self._attr_entity_category = EntityCategory.CONFIG
        self._entry = entry
        
        # Build options list from labels
        self._attr_options = [opt["label"] for opt in select_info["options"].values()]

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.data["device_sn"])},
            "name": f"EcoFlow Delta 2 {self._entry.data['device_sn']}",
            "manufacturer": "EcoFlow",
            "model": "Delta 2",
            "sw_version": "1.0",
        }

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if self.coordinator.data is None:
            return None
        
        key = self._select_info["key"]
        
        # Try to get value from coordinator data
        if key in self.coordinator.data:
            current_value = self.coordinator.data[key]
        else:
            # Fallback: try nested dictionary navigation
            keys = key.split(".")
            value = self.coordinator.data
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return None
            
            current_value = value
        
        # Find matching option by value
        for option_key, option_data in self._select_info["options"].items():
            if option_data["value"] == current_value:
                return option_data["label"]
        
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        import logging
        _LOGGER = logging.getLogger(__name__)
        _LOGGER.info(f"Setting {self._select_type} to {option}")
        
        # Find the value for the selected label
        selected_value = None
        for option_data in self._select_info["options"].values():
            if option_data["label"] == option:
                selected_value = option_data["value"]
                break
        
        if selected_value is None:
            _LOGGER.error(f"Invalid option {option} for {self._select_type}")
            return
        
        # Build command parameters
        cmd_code = self._select_info["cmd_code"]
        param_name = self._select_info["param_name"]
        
        params = {
            "sn": self._entry.data["device_sn"],
            "cmdCode": cmd_code,
            "params": {
                param_name: selected_value
            }
        }
        
        _LOGGER.debug(f"Sending command: {params}")
        
        # Send command via API
        try:
            response = await self.hass.async_add_executor_job(
                self._api._make_request,
                "/iot-open/sign/device/quota",
                params,
                "POST"
            )
            
            _LOGGER.info(f"API response for {self._select_type}: {response}")
            
            if response.get("code") == "0":
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error(f"API returned error code for {self._select_type}: {response}")
        except Exception as e:
            _LOGGER.error(f"Failed to set {self._select_type}: {e}", exc_info=True)
