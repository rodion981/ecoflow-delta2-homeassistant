"""Sensor platform for EcoFlow Delta 2."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


SENSOR_TYPES = {
    "battery_level": {
        "name": "Battery Level",
        "key": "bms_bmsStatus.soc",
        "unit": PERCENTAGE,
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery",
        "entity_category": None,  # Main sensor
    },
    "battery_capacity_remain": {
        "name": "Battery Capacity Remaining",
        "key": "bms_bmsStatus.designCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "battery_temp": {
        "name": "Battery Temperature",
        "key": "bms_bmsStatus.temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "battery_voltage": {
        "name": "Battery Voltage",
        "key": "bms_bmsStatus.vol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:lightning-bolt",
        "value_fn": lambda x: x / 1000,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "battery_current": {
        "name": "Battery Current",
        "key": "bms_bmsStatus.amp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-dc",
        "value_fn": lambda x: x / 1000,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "cycles": {
        "name": "Battery Cycles",
        "key": "bms_bmsStatus.cycles",
        "unit": "cycles",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:counter",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "soh": {
        "name": "State of Health",
        "key": "bms_bmsStatus.soh",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:heart-pulse",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "input_watts": {
        "name": "Total Input Power",
        "key": "pd.wattsInSum",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:transmission-tower-import",
        "entity_category": None,  # Main sensor
    },
    "output_watts": {
        "name": "Total Output Power",
        "key": "pd.wattsOutSum",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:transmission-tower-export",
        "entity_category": None,  # Main sensor
    },
    "ac_in_watts": {
        "name": "AC Input Power",
        "key": "inv.inputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:power-plug",
        "entity_category": None,  # Main sensor
    },
    "ac_out_watts": {
        "name": "AC Output Power",
        "key": "inv.outputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:power-socket",
        "entity_category": None,  # Main sensor
    },
    "ac_in_volts": {
        "name": "AC Input Voltage",
        "key": "inv.acInVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "value_fn": lambda x: x / 1000,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "ac_out_volts": {
        "name": "AC Output Voltage",
        "key": "inv.invOutVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "value_fn": lambda x: x / 1000,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "solar_in_watts": {
        "name": "Solar Input Power",
        "key": "mppt.inWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
        "entity_category": None,  # Main sensor
    },
    "solar_in_volts": {
        "name": "Solar Input Voltage",
        "key": "mppt.inVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-panel",
        "value_fn": lambda x: x / 1000,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "dc_out_watts": {
        "name": "DC Output Power",
        "key": "mppt.outWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
        "entity_category": None,  # Main sensor
    },
    "type_c_1_watts": {
        "name": "USB-C 1 Output Power",
        "key": "pd.typec1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "entity_category": None,  # Main sensor
    },
    "type_c_2_watts": {
        "name": "USB-C 2 Output Power",
        "key": "pd.typec2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "entity_category": None,  # Main sensor
    },
    "usb_a_1_watts": {
        "name": "USB-A 1 Output Power",
        "key": "pd.usb1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "entity_category": None,  # Main sensor
    },
    "usb_a_2_watts": {
        "name": "USB-A 2 Output Power",
        "key": "pd.usb2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "entity_category": None,  # Main sensor
    },
    "remain_time": {
        "name": "Remaining Time",
        "key": "bms_bmsStatus.remainTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer-outline",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "max_charge_soc": {
        "name": "Max Charge Level",
        "key": "bms_emsStatus.maxChargeSoc",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging-100",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "min_discharge_soc": {
        "name": "Min Discharge Level",
        "key": "bms_emsStatus.minDsgSoc",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging-outline",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "charge_power_limit": {
        "name": "Charge Power Limit",
        "key": "mppt.cfgChgWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "lcd_timeout": {
        "name": "LCD Timeout",
        "key": "pd.lcdOffSec",
        "unit": UnitOfTime.SECONDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:monitor",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "ac_standby_time": {
        "name": "AC Standby Time",
        "key": "inv.standbyMins",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer-sand",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EcoFlow Delta 2 sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    entities = []
    for sensor_type, sensor_info in SENSOR_TYPES.items():
        entities.append(
            EcoFlowDelta2Sensor(
                coordinator,
                entry,
                sensor_type,
                sensor_info,
            )
        )
    
    async_add_entities(entities)


class EcoFlowDelta2Sensor(CoordinatorEntity, SensorEntity):
    """Representation of an EcoFlow Delta 2 sensor."""

    def __init__(self, coordinator, entry, sensor_type, sensor_info):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._attr_unique_id = f"{entry.data['device_sn']}_{sensor_type}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_device_class = sensor_info["device_class"]
        self._attr_state_class = sensor_info["state_class"]
        self._attr_icon = sensor_info["icon"]
        self._attr_entity_category = sensor_info.get("entity_category")
        self._attr_entity_registry_enabled_default = sensor_info.get("entity_registry_enabled_default", True)
        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_type
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
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        # EcoFlow API returns flat keys with dots (e.g., "bms_bmsStatus.soc")
        # Try direct key access first
        key = self._sensor_info["key"]
        
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
                    return None
        
        # Apply value transformation if defined
        if "value_fn" in self._sensor_info and value is not None:
            value = self._sensor_info["value_fn"](value)
        
        return value
