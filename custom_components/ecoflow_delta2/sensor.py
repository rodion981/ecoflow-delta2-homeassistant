"""Sensor platform for EcoFlow Delta 2 - FULL VERSION with ALL sensors."""
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
    # Battery Main Status
    "battery_level": {
        "name": "Battery Level",
        "key": "bms_bmsStatus.soc",
        "unit": PERCENTAGE,
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery",
    },
    "battery_capacity_remain": {
        "name": "Battery Capacity Remaining",
        "key": "bms_bmsStatus.remainCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
    },
    "battery_capacity_design": {
        "name": "Battery Design Capacity",
        "key": "bms_bmsStatus.designCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
    },
    "battery_capacity_full": {
        "name": "Battery Full Capacity",
        "key": "bms_bmsStatus.fullCap",
        "unit": "mAh",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-capacity",
    },
    "battery_temp": {
        "name": "Battery Temperature",
        "key": "bms_bmsStatus.temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "battery_temp_min": {
        "name": "Battery Min Cell Temperature",
        "key": "bms_bmsStatus.minCellTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer-low",
    },
    "battery_temp_max": {
        "name": "Battery Max Cell Temperature",
        "key": "bms_bmsStatus.maxCellTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer-high",
    },
    "battery_voltage": {
        "name": "Battery Voltage",
        "key": "bms_bmsStatus.vol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:lightning-bolt",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "battery_current": {
        "name": "Battery Current",
        "key": "bms_bmsStatus.amp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-dc",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "battery_cell_voltage_min": {
        "name": "Battery Min Cell Voltage",
        "key": "bms_bmsStatus.minCellVol",
        "unit": UnitOfElectricPotential.MILLIVOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-low",
    },
    "battery_cell_voltage_max": {
        "name": "Battery Max Cell Voltage",
        "key": "bms_bmsStatus.maxCellVol",
        "unit": UnitOfElectricPotential.MILLIVOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-high",
    },
    "battery_mos_temp_min": {
        "name": "Battery Min MOS Temperature",
        "key": "bms_bmsStatus.minMosTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "battery_mos_temp_max": {
        "name": "Battery Max MOS Temperature",
        "key": "bms_bmsStatus.maxMosTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "cycles": {
        "name": "Battery Cycles",
        "key": "bms_bmsStatus.cycles",
        "unit": "cycles",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:counter",
    },
    "soh": {
        "name": "State of Health",
        "key": "bms_bmsStatus.soh",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:heart-pulse",
    },
    
    # Power - Main
    "input_watts": {
        "name": "Total Input Power",
        "key": "pd.wattsInSum",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:transmission-tower-import",
    },
    "output_watts": {
        "name": "Total Output Power",
        "key": "pd.wattsOutSum",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:transmission-tower-export",
    },
    "battery_input_watts": {
        "name": "Battery Input Power",
        "key": "bms_bmsStatus.inputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging",
    },
    "battery_output_watts": {
        "name": "Battery Output Power",
        "key": "bms_bmsStatus.outputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-minus",
    },
    
    # AC Input/Output
    "ac_in_watts": {
        "name": "AC Input Power",
        "key": "inv.inputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:power-plug",
    },
    "ac_out_watts": {
        "name": "AC Output Power",
        "key": "inv.outputWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:power-socket",
    },
    "ac_in_volts": {
        "name": "AC Input Voltage",
        "key": "inv.acInVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "ac_out_volts": {
        "name": "AC Output Voltage",
        "key": "inv.invOutVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "ac_in_amps": {
        "name": "AC Input Current",
        "key": "inv.acInAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "ac_out_amps": {
        "name": "AC Output Current",
        "key": "inv.invOutAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-ac",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "ac_in_freq": {
        "name": "AC Input Frequency",
        "key": "inv.acInFreq",
        "unit": "Hz",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "ac_out_freq": {
        "name": "AC Output Frequency",
        "key": "inv.invOutFreq",
        "unit": "Hz",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sine-wave",
    },
    "inv_out_temp": {
        "name": "Inverter Temperature",
        "key": "inv.outTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    
    # Solar/MPPT
    "solar_in_watts": {
        "name": "Solar Input Power",
        "key": "mppt.inWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
    },
    "solar_in_volts": {
        "name": "Solar Input Voltage",
        "key": "mppt.inVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-panel",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "solar_in_amps": {
        "name": "Solar Input Current",
        "key": "mppt.inAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:solar-power",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "mppt_temp": {
        "name": "MPPT Temperature",
        "key": "mppt.mpptTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    
    # DC Output
    "dc_out_watts": {
        "name": "DC Output Power",
        "key": "mppt.outWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
    },
    "dc_out_volts": {
        "name": "DC Output Voltage",
        "key": "mppt.outVol",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "dc_out_amps": {
        "name": "DC Output Current",
        "key": "mppt.outAmp",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:current-dc",
        "value_fn": lambda x: round(x / 1000, 2),
    },
    "dc_12v_watts": {
        "name": "DC 12V Output Power",
        "key": "mppt.dcdc12vWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-battery",
    },
    "car_watts": {
        "name": "Car Port Power",
        "key": "pd.carWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:car-electric",
    },
    "car_temp": {
        "name": "Car Port Temperature",
        "key": "pd.carTemp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    
    # USB Ports
    "type_c_1_watts": {
        "name": "USB-C 1 Output Power",
        "key": "pd.typec1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
    },
    "type_c_2_watts": {
        "name": "USB-C 2 Output Power",
        "key": "pd.typec2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
    },
    "usb_a_1_watts": {
        "name": "USB-A 1 Output Power",
        "key": "pd.usb1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
    },
    "usb_a_2_watts": {
        "name": "USB-A 2 Output Power",
        "key": "pd.usb2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
    },
    "usb_qc_1_watts": {
        "name": "USB QC 1 Output Power",
        "key": "pd.qcUsb1Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
    },
    "usb_qc_2_watts": {
        "name": "USB QC 2 Output Power",
        "key": "pd.qcUsb2Watts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:usb-port",
    },
    "typec_1_temp": {
        "name": "USB-C 1 Temperature",
        "key": "pd.typec1Temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "typec_2_temp": {
        "name": "USB-C 2 Temperature",
        "key": "pd.typec2Temp",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    
    # Time & Usage
    "remain_time": {
        "name": "Remaining Time",
        "key": "pd.remainTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer-outline",
        "value_fn": lambda x: abs(x),
    },
    "inv_used_time": {
        "name": "Inverter Used Time",
        "key": "pd.invUsedTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:timer",
    },
    "mppt_used_time": {
        "name": "MPPT Used Time",
        "key": "pd.mpptUsedTime",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:timer",
    },
    
    # Settings & Configuration
    "max_charge_soc": {
        "name": "Max Charge Level",
        "key": "bms_emsStatus.maxChargeSoc",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging-100",
    },
    "min_discharge_soc": {
        "name": "Min Discharge Level",
        "key": "bms_emsStatus.minDsgSoc",
        "unit": PERCENTAGE,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-charging-outline",
    },
    "charge_power_limit": {
        "name": "Charge Power Limit",
        "key": "mppt.cfgChgWatts",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
    },
    "lcd_timeout": {
        "name": "LCD Timeout",
        "key": "pd.lcdOffSec",
        "unit": UnitOfTime.SECONDS,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:monitor",
    },
    "ac_standby_time": {
        "name": "AC Standby Time",
        "key": "inv.standbyMins",
        "unit": UnitOfTime.MINUTES,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:timer-sand",
    },
    "brightness_level": {
        "name": "Screen Brightness",
        "key": "pd.brightLevel",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:brightness-6",
    },
    "wifi_rssi": {
        "name": "WiFi Signal Strength",
        "key": "pd.wifiRssi",
        "unit": "dBm",
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:wifi",
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
        self._attr_name = f"EcoFlow Delta 2 {sensor_info['name']}"
        self._attr_unique_id = f"{entry.data['device_sn']}_{sensor_type}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_device_class = sensor_info["device_class"]
        self._attr_state_class = sensor_info["state_class"]
        self._attr_icon = sensor_info["icon"]
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
