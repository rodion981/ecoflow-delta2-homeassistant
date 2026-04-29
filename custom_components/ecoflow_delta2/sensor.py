"""Sensor platform for EcoFlow Delta 2 - OPTIMIZED with short names and hidden sensors."""
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

from .const import DOMAIN


SENSOR_TYPES = {
    # Battery Main Status - VISIBLE by default
    "battery_level": {
        "name": "Battery Level",
        "key": "bms_bmsStatus.soc",
        "unit": PERCENTAGE,
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery",
        "enabled": True,
    },
    "battery_temp": {
        "name": "Battery Temp",
        "key": "bms_bmsStatus.temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": True,
    },
    "battery_voltage": {
        "name": "Battery Voltage",
        "key": "bms_bmsStatus.vol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:lightning-bolt",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": True,
    },
    "battery_current": {
        "name": "Battery Current",
        "key": "bms_bmsStatus.amp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-dc",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": True,
    },
    "cycles": {
        "name": "Battery Cycles",
        "key": "bms_bmsStatus.cycles",
        "unit": "cycles",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:counter",
        "enabled": True,
    },
    "soh": {
        "name": "Battery SOH",
        "key": "bms_bmsStatus.soh",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:heart-pulse",
        "enabled": True,
    },
    
    # Battery Details - HIDDEN by default
    "battery_capacity_remain": {
        "name": "Battery Capacity Remaining",
        "key": "bms_bmsStatus.remainCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
        "enabled": False,
    },
    "battery_capacity_design": {
        "name": "Battery Design Capacity",
        "key": "bms_bmsStatus.designCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
        "enabled": False,
    },
    "battery_capacity_full": {
        "name": "Battery Full Capacity",
        "key": "bms_bmsStatus.fullCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
        "enabled": False,
    },
    "battery_temp_min": {
        "name": "Battery Min Cell Temp",
        "key": "bms_bmsStatus.minCellTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer-low",
        "enabled": False,
    },
    "battery_temp_max": {
        "name": "Battery Max Cell Temp",
        "key": "bms_bmsStatus.maxCellTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer-high",
        "enabled": False,
    },
    "battery_cell_voltage_min": {
        "name": "Battery Min Cell Voltage",
        "key": "bms_bmsStatus.minCellVol",
        "unit": UnitOfElectricPotential.MILLIVOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-low",
        "enabled": False,
    },
    "battery_cell_voltage_max": {
        "name": "Battery Max Cell Voltage",
        "key": "bms_bmsStatus.maxCellVol",
        "unit": UnitOfElectricPotential.MILLIVOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-high",
        "enabled": False,
    },
    "battery_mos_temp_min": {
        "name": "Battery Min MOS Temp",
        "key": "bms_bmsStatus.minMosTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    "battery_mos_temp_max": {
        "name": "Battery Max MOS Temp",
        "key": "bms_bmsStatus.maxMosTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    
    # Power - Main - VISIBLE by default
    "input_watts": {
        "name": "Total Input",
        "key": "pd.wattsInSum",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:transmission-tower-import",
        "enabled": True,
    },
    "output_watts": {
        "name": "Total Output",
        "key": "pd.wattsOutSum",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:transmission-tower-export",
        "enabled": True,
    },
    "battery_input_watts": {
        "name": "Battery Input",
        "key": "bms_bmsStatus.inputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging",
        "enabled": False,
    },
    "battery_output_watts": {
        "name": "Battery Output",
        "key": "bms_bmsStatus.outputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-minus",
        "enabled": False,
    },
    
    # AC Input/Output - VISIBLE by default (main), HIDDEN (details)
    "ac_in_watts": {
        "name": "AC Input",
        "key": "inv.inputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:power-plug",
        "enabled": True,
    },
    "ac_out_watts": {
        "name": "AC Output",
        "key": "inv.outputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:power-socket",
        "enabled": True,
    },
    "ac_in_volts": {
        "name": "AC Input Voltage",
        "key": "inv.acInVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "ac_out_volts": {
        "name": "AC Output Voltage",
        "key": "inv.invOutVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "ac_in_amps": {
        "name": "AC Input Current",
        "key": "inv.acInAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "ac_out_amps": {
        "name": "AC Output Current",
        "key": "inv.invOutAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "ac_in_freq": {
        "name": "AC Input Freq",
        "key": "inv.acInFreq",
        "unit": "Hz",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "enabled": False,
    },
    "ac_out_freq": {
        "name": "AC Output Freq",
        "key": "inv.invOutFreq",
        "unit": "Hz",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "enabled": False,
    },
    "inv_out_temp": {
        "name": "Inverter Temp",
        "key": "inv.outTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    
    # Solar/MPPT - VISIBLE (main), HIDDEN (details)
    "solar_in_watts": {
        "name": "Solar Input",
        "key": "mppt.inWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
        "enabled": True,
    },
    "solar_in_volts": {
        "name": "Solar Voltage",
        "key": "mppt.inVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-panel",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "solar_in_amps": {
        "name": "Solar Current",
        "key": "mppt.inAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "mppt_temp": {
        "name": "MPPT Temp",
        "key": "mppt.mpptTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    
    # DC Output - ALL HIDDEN by default
    "dc_out_watts": {
        "name": "DC Output",
        "key": "mppt.outWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
        "enabled": False,
    },
    "dc_out_volts": {
        "name": "DC Voltage",
        "key": "mppt.outVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "dc_out_amps": {
        "name": "DC Current",
        "key": "mppt.outAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-dc",
        "value_fn": lambda x: round(x / 1000, 2),
        "enabled": False,
    },
    "dc_12v_watts": {
        "name": "DC 12V Output",
        "key": "mppt.dcdc12vWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
        "enabled": False,
    },
    "car_watts": {
        "name": "Car Port",
        "key": "pd.carWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-electric",
        "enabled": False,
    },
    "car_temp": {
        "name": "Car Port Temp",
        "key": "pd.carTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    
    # USB Ports - ALL HIDDEN by default
    "type_c_1_watts": {
        "name": "USB-C 1",
        "key": "pd.typec1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "enabled": False,
    },
    "type_c_2_watts": {
        "name": "USB-C 2",
        "key": "pd.typec2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "enabled": False,
    },
    "usb_a_1_watts": {
        "name": "USB-A 1",
        "key": "pd.usb1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "enabled": False,
    },
    "usb_a_2_watts": {
        "name": "USB-A 2",
        "key": "pd.usb2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "enabled": False,
    },
    "usb_qc_1_watts": {
        "name": "USB QC 1",
        "key": "pd.qcUsb1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "enabled": False,
    },
    "usb_qc_2_watts": {
        "name": "USB QC 2",
        "key": "pd.qcUsb2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
        "enabled": False,
    },
    "typec_1_temp": {
        "name": "USB-C 1 Temp",
        "key": "pd.typec1Temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    "typec_2_temp": {
        "name": "USB-C 2 Temp",
        "key": "pd.typec2Temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
        "enabled": False,
    },
    
    # Time & Usage - VISIBLE (main), HIDDEN (stats)
    "remain_time": {
        "name": "Remaining Time",
        "key": "pd.remainTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer-outline",
        "value_fn": lambda x: abs(x),
        "enabled": True,
    },
    "inv_used_time": {
        "name": "Inverter Used Time",
        "key": "pd.invUsedTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:timer",
        "enabled": False,
    },
    "mppt_used_time": {
        "name": "MPPT Used Time",
        "key": "pd.mpptUsedTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:timer",
        "enabled": False,
    },
    
    # Settings & Configuration - VISIBLE (adjustable), HIDDEN (info)
    "max_charge_soc": {
        "name": "Max Charge Level",
        "key": "bms_emsStatus.maxChargeSoc",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging-100",
        "enabled": True,
    },
    "min_discharge_soc": {
        "name": "Min Discharge Level",
        "key": "bms_emsStatus.minDsgSoc",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging-outline",
        "enabled": True,
    },
    "charge_power_limit": {
        "name": "Charge Power Limit",
        "key": "mppt.cfgChgWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
        "enabled": True,
    },
    "lcd_timeout": {
        "name": "LCD Timeout",
        "key": "pd.lcdOffSec",
        "unit": UnitOfTime.SECONDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:monitor",
        "enabled": False,
    },
    "ac_standby_time": {
        "name": "AC Standby Time",
        "key": "inv.standbyMins",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer-sand",
        "enabled": False,
    },
    "brightness_level": {
        "name": "Screen Brightness",
        "key": "pd.brightLevel",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:brightness-6",
        "enabled": False,
    },
    "wifi_rssi": {
        "name": "WiFi Signal",
        "key": "pd.wifiRssi",
        "unit": "dBm",
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi",
        "enabled": False,
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
        self._attr_name = sensor_info['name']
        self._attr_unique_id = f"{entry.data['device_sn']}_{sensor_type}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_device_class = sensor_info["device_class"]
        self._attr_state_class = sensor_info["state_class"]
        self._attr_icon = sensor_info["icon"]
        self._attr_entity_registry_enabled_default = sensor_info.get("enabled", True)
        self._entry = entry

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.data["device_sn"])},
            "name": f"EcoFlow Delta 2",
            "manufacturer": "EcoFlow",
            "model": "Delta 2",
            "sw_version": "1.0",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        # EcoFlow API returns flat keys with dots
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
