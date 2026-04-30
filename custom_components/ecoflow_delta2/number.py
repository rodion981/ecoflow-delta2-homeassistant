"""Number platform for EcoFlow Delta 2 - adjustable settings."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


NUMBER_TYPES = {
    "max_charge_soc": {
        "name": "Max Charge Level",
        "key": "bms_emsStatus.maxChargeSoc",
        "unit": PERCENTAGE,
        "min": 50,
        "max": 100,
        "step": 1,
        "icon": "mdi:battery-charging-100",
        "command": "set_max_charge_soc",
    },
    "min_discharge_soc": {
        "name": "Min Discharge Level",
        "key": "bms_emsStatus.minDsgSoc",
        "unit": PERCENTAGE,
        "min": 0,
        "max": 30,
        "step": 1,
        "icon": "mdi:battery-outline",
        "command": "set_min_discharge_soc",
    },
    "charge_power_ac": {
        "name": "AC Charge Power Limit",
        "key": "mppt.cfgChgWatts",
        "unit": UnitOfPower.WATT,
        "min": 200,
        "max": 1200,
        "step": 100,
        "icon": "mdi:flash",
        "command": "set_ac_charge_power",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EcoFlow Delta 2 number entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    
    entities = []
    for number_type, number_info in NUMBER_TYPES.items():
        entities.append(
            EcoFlowDelta2Number(
                coordinator,
                api,
                entry,
                number_type,
                number_info,
            )
        )
    
    async_add_entities(entities)


class EcoFlowDelta2Number(CoordinatorEntity, NumberEntity):
    """Representation of an EcoFlow Delta 2 number entity."""

    def __init__(self, coordinator, api, entry, number_type, number_info):
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._api = api
        self._number_type = number_type
        self._number_info = number_info
        self._attr_unique_id = f"{entry.data['device_sn']}_{number_type}"
        self._attr_native_unit_of_measurement = number_info["unit"]
        self._attr_native_min_value = number_info["min"]
        self._attr_native_max_value = number_info["max"]
        self._attr_native_step = number_info["step"]
        self._attr_icon = number_info["icon"]
        self._attr_mode = NumberMode.SLIDER
        self._attr_has_entity_name = True
        self._attr_translation_key = number_type
        self._attr_entity_category = EntityCategory.CONFIG
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
    def native_value(self):
        """Return the current value."""
        if self.coordinator.data is None:
            return None
        
        key = self._number_info["key"]
        
        if key in self.coordinator.data:
            return self.coordinator.data[key]
        else:
            # Fallback: try nested dictionary navigation
            keys = key.split(".")
            value = self.coordinator.data
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return None
            
            return value

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        import logging
        _LOGGER = logging.getLogger(__name__)
        _LOGGER.info(f"Setting {self._number_type} to {value}")
        
        command_name = self._number_info["command"]
        
        # Call API method to set the value
        if hasattr(self._api, command_name):
            command = getattr(self._api, command_name)
            success = await self.hass.async_add_executor_job(command, int(value))
            
            _LOGGER.info(f"Command result for {self._number_type}: {success}")
            
            if success:
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error(f"Failed to set {self._number_type} to {value}")
