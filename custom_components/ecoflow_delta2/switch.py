"""Switch platform for EcoFlow Delta 2."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SWITCH_TYPES = {
    "ac_enabled": {
        "name": "AC Output",
        "key": "inv.cfgAcEnabled",
        "icon": "mdi:power-socket",
        "command": "set_ac_output",
    },
    "dc_enabled": {
        "name": "DC Output",
        "key": "pd.dcOutState",
        "icon": "mdi:car-battery",
        "command": "set_dc_output",
    },
    "xboost_enabled": {
        "name": "X-Boost",
        "key": "inv.cfgAcXboost",
        "icon": "mdi:lightning-bolt",
        "command": "set_xboost",
    },
    "beeper_enabled": {
        "name": "Beeper",
        "key": "pd.beepMode",
        "icon": "mdi:volume-high",
        "command": "set_beeper",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EcoFlow Delta 2 switch based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    
    entities = []
    for switch_type, switch_info in SWITCH_TYPES.items():
        entities.append(
            EcoFlowDelta2Switch(
                coordinator,
                api,
                entry,
                switch_type,
                switch_info,
            )
        )
    
    async_add_entities(entities)


class EcoFlowDelta2Switch(CoordinatorEntity, SwitchEntity):
    """Representation of an EcoFlow Delta 2 switch."""

    def __init__(self, coordinator, api, entry, switch_type, switch_info):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._api = api
        self._switch_type = switch_type
        self._switch_info = switch_info
        self._attr_unique_id = f"{entry.data['device_sn']}_{switch_type}"
        self._attr_icon = switch_info["icon"]
        self._attr_translation_key = switch_type
        self._entry = entry

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
    def is_on(self) -> bool:
        """Return true if switch is on."""
        if self.coordinator.data is None:
            return False
        
        # EcoFlow API returns flat keys with dots (e.g., "inv.cfgAcEnabled")
        # Try direct key access first
        key = self._switch_info["key"]
        
        if key in self.coordinator.data:
            value = self.coordinator.data[key]
        else:
            # Fallback: try nested dictionary navigation
            keys = key.split(".")
            value = self.coordinator.data
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return False
        
        return bool(value)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        command = getattr(self._api, self._switch_info["command"])
        success = await self.hass.async_add_executor_job(command, True)
        
        if success:
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        command = getattr(self._api, self._switch_info["command"])
        success = await self.hass.async_add_executor_job(command, False)
        
        if success:
            await self.coordinator.async_request_refresh()
