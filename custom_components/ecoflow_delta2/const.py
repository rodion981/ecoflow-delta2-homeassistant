"""Constants for the EcoFlow Delta 2 integration."""

DOMAIN = "ecoflow_delta2"

# API endpoints
API_BASE_URL = {
    "eu": "https://api-e.ecoflow.com",
    "us": "https://api.ecoflow.com",
}

MQTT_BROKER = {
    "eu": "mqtt-e.ecoflow.com",
    "us": "mqtt.ecoflow.com",
}

# Device types
DEVICE_TYPE_DELTA2 = "DELTA_2"

# Sensor types
SENSOR_BATTERY_LEVEL = "battery_level"
SENSOR_BATTERY_TEMP = "battery_temp"
SENSOR_INPUT_WATTS = "input_watts"
SENSOR_OUTPUT_WATTS = "output_watts"
SENSOR_REMAIN_TIME = "remain_time"
SENSOR_CYCLES = "cycles"
SENSOR_SOH = "soh"
SENSOR_AC_IN_WATTS = "ac_in_watts"
SENSOR_AC_OUT_WATTS = "ac_out_watts"
SENSOR_SOLAR_IN_WATTS = "solar_in_watts"
SENSOR_DC_OUT_WATTS = "dc_out_watts"
SENSOR_TYPE_C_1_WATTS = "type_c_1_watts"
SENSOR_TYPE_C_2_WATTS = "type_c_2_watts"
SENSOR_USB_A_1_WATTS = "usb_a_1_watts"
SENSOR_USB_A_2_WATTS = "usb_a_2_watts"
SENSOR_USB_QC_1_WATTS = "usb_qc_1_watts"
SENSOR_USB_QC_2_WATTS = "usb_qc_2_watts"
SENSOR_AC_IN_VOLTS = "ac_in_volts"
SENSOR_AC_OUT_VOLTS = "ac_out_volts"
SENSOR_SOLAR_IN_VOLTS = "solar_in_volts"
SENSOR_BATTERY_VOLTS = "battery_volts"
SENSOR_BATTERY_CURRENT = "battery_current"

# Switch types
SWITCH_AC_ENABLED = "ac_enabled"
SWITCH_DC_ENABLED = "dc_enabled"
SWITCH_XBOOST_ENABLED = "xboost_enabled"
SWITCH_BEEPER_ENABLED = "beeper_enabled"
