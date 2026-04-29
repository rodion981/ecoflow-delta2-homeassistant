# Приклади використання

## Автоматизації

### 1. Сповіщення про низький заряд

```yaml
automation:
  - alias: "EcoFlow: Низький заряд батареї"
    description: "Надіслати сповіщення коли заряд нижче 20%"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        below: 20
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "⚠️ EcoFlow Delta 2"
          message: "Заряд батареї {{ states('sensor.ecoflow_delta_2_battery_level') }}%"
          data:
            priority: high
```

### 2. Автоматичне вимкнення при повному заряді

```yaml
automation:
  - alias: "EcoFlow: Вимкнути AC при повному заряді"
    description: "Вимкнути AC вихід коли батарея заряджена на 100%"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        above: 99
    condition:
      - condition: state
        entity_id: switch.ecoflow_delta_2_ac_output
        state: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
      - service: notify.mobile_app_your_phone
        data:
          message: "EcoFlow Delta 2 повністю заряджена. AC вихід вимкнено."
```

### 3. Увімкнення AC при наявності сонячної енергії

```yaml
automation:
  - alias: "EcoFlow: Увімкнути AC при сонячній енергії"
    description: "Увімкнути AC коли є сонячна енергія більше 100W"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_solar_in_watts
        above: 100
        for:
          minutes: 2
    condition:
      - condition: state
        entity_id: switch.ecoflow_delta_2_ac_output
        state: "off"
      - condition: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        above: 30
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
```

### 4. Вимкнення AC при низькому заряді

```yaml
automation:
  - alias: "EcoFlow: Вимкнути AC при низькому заряді"
    description: "Вимкнути AC вихід при заряді нижче 15%"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        below: 15
    condition:
      - condition: state
        entity_id: switch.ecoflow_delta_2_ac_output
        state: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
      - service: notify.mobile_app_your_phone
        data:
          title: "🔋 EcoFlow Delta 2"
          message: "AC вихід вимкнено через низький заряд ({{ states('sensor.ecoflow_delta_2_battery_level') }}%)"
```

### 5. Моніторинг температури батареї

```yaml
automation:
  - alias: "EcoFlow: Висока температура батареї"
    description: "Сповіщення при високій температурі"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_temp
        above: 45
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🌡️ EcoFlow Delta 2"
          message: "Висока температура батареї: {{ states('sensor.ecoflow_delta_2_battery_temp') }}°C"
          data:
            priority: high
```

### 6. Щоденний звіт про стан

```yaml
automation:
  - alias: "EcoFlow: Щоденний звіт"
    description: "Надіслати звіт про стан кожен ранок"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "📊 EcoFlow Delta 2 - Щоденний звіт"
          message: |
            Заряд: {{ states('sensor.ecoflow_delta_2_battery_level') }}%
            Температура: {{ states('sensor.ecoflow_delta_2_battery_temp') }}°C
            Цикли: {{ states('sensor.ecoflow_delta_2_cycles') }}
            SOH: {{ states('sensor.ecoflow_delta_2_soh') }}%
            AC вихід: {{ states('switch.ecoflow_delta_2_ac_output') }}
```

### 7. Розумне керування навантаженням

```yaml
automation:
  - alias: "EcoFlow: Розумне керування навантаженням"
    description: "Вимкнути навантаження при низькому заряді"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        below: 25
    action:
      - service: switch.turn_off
        target:
          entity_id:
            - switch.living_room_heater
            - switch.office_fan
      - service: notify.mobile_app_your_phone
        data:
          message: "Навантаження вимкнено через низький заряд EcoFlow"
```

---

## Lovelace картки

### 1. Базова картка з інформацією

```yaml
type: entities
title: EcoFlow Delta 2
icon: mdi:battery-charging
entities:
  - entity: sensor.ecoflow_delta_2_battery_level
    name: Заряд батареї
    icon: mdi:battery
  - entity: sensor.ecoflow_delta_2_battery_temp
    name: Температура
  - entity: sensor.ecoflow_delta_2_input_watts
    name: Вхідна потужність
  - entity: sensor.ecoflow_delta_2_output_watts
    name: Вихідна потужність
  - entity: sensor.ecoflow_delta_2_remain_time
    name: Залишковий час
  - type: divider
  - entity: switch.ecoflow_delta_2_ac_output
    name: AC вихід
  - entity: switch.ecoflow_delta_2_dc_output
    name: DC вихід
  - entity: switch.ecoflow_delta_2_xboost_enabled
    name: X-Boost
```

### 2. Gauge для рівня батареї

```yaml
type: gauge
entity: sensor.ecoflow_delta_2_battery_level
name: Батарея Delta 2
unit: "%"
min: 0
max: 100
needle: true
severity:
  green: 60
  yellow: 30
  red: 0
```

### 3. Картка з потужністю

```yaml
type: vertical-stack
cards:
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.ecoflow_delta_2_input_watts
        name: Вхід
        min: 0
        max: 1200
        needle: true
      - type: gauge
        entity: sensor.ecoflow_delta_2_output_watts
        name: Вихід
        min: 0
        max: 1800
        needle: true
  - type: entities
    entities:
      - entity: sensor.ecoflow_delta_2_ac_in_watts
        name: AC вхід
      - entity: sensor.ecoflow_delta_2_solar_in_watts
        name: Сонячна панель
      - entity: sensor.ecoflow_delta_2_ac_out_watts
        name: AC вихід
      - entity: sensor.ecoflow_delta_2_dc_out_watts
        name: DC вихід
```

### 4. Детальна картка з графіками

```yaml
type: vertical-stack
cards:
  - type: glance
    title: EcoFlow Delta 2
    entities:
      - entity: sensor.ecoflow_delta_2_battery_level
        name: Заряд
      - entity: sensor.ecoflow_delta_2_battery_temp
        name: Температура
      - entity: sensor.ecoflow_delta_2_cycles
        name: Цикли
      - entity: sensor.ecoflow_delta_2_soh
        name: SOH
  - type: history-graph
    title: Потужність (24 години)
    hours_to_show: 24
    entities:
      - entity: sensor.ecoflow_delta_2_input_watts
        name: Вхід
      - entity: sensor.ecoflow_delta_2_output_watts
        name: Вихід
      - entity: sensor.ecoflow_delta_2_solar_in_watts
        name: Сонце
  - type: history-graph
    title: Заряд батареї (24 години)
    hours_to_show: 24
    entities:
      - entity: sensor.ecoflow_delta_2_battery_level
```

### 5. Картка з USB портами

```yaml
type: entities
title: USB порти
icon: mdi:usb
entities:
  - entity: sensor.ecoflow_delta_2_type_c_1_watts
    name: USB-C 1
    icon: mdi:usb-c-port
  - entity: sensor.ecoflow_delta_2_type_c_2_watts
    name: USB-C 2
    icon: mdi:usb-c-port
  - entity: sensor.ecoflow_delta_2_usb_a_1_watts
    name: USB-A 1
    icon: mdi:usb-port
  - entity: sensor.ecoflow_delta_2_usb_a_2_watts
    name: USB-A 2
    icon: mdi:usb-port
```

### 6. Картка з перемикачами

```yaml
type: entities
title: Керування
icon: mdi:toggle-switch
entities:
  - entity: switch.ecoflow_delta_2_ac_output
    name: AC вихід
    icon: mdi:power-socket
  - entity: switch.ecoflow_delta_2_dc_output
    name: DC вихід
    icon: mdi:car-battery
  - entity: switch.ecoflow_delta_2_xboost_enabled
    name: X-Boost
    icon: mdi:lightning-bolt
  - entity: switch.ecoflow_delta_2_beeper_enabled
    name: Звуковий сигнал
    icon: mdi:volume-high
```

### 7. Повна dashboard картка

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # 🔋 EcoFlow Delta 2
      **Заряд:** {{ states('sensor.ecoflow_delta_2_battery_level') }}% | 
      **Температура:** {{ states('sensor.ecoflow_delta_2_battery_temp') }}°C | 
      **Цикли:** {{ states('sensor.ecoflow_delta_2_cycles') }}
  
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.ecoflow_delta_2_battery_level
        name: Батарея
        min: 0
        max: 100
        severity:
          green: 60
          yellow: 30
          red: 0
      - type: gauge
        entity: sensor.ecoflow_delta_2_input_watts
        name: Вхід
        min: 0
        max: 1200
      - type: gauge
        entity: sensor.ecoflow_delta_2_output_watts
        name: Вихід
        min: 0
        max: 1800
  
  - type: entities
    title: Потужність
    entities:
      - entity: sensor.ecoflow_delta_2_ac_in_watts
        name: AC вхід
      - entity: sensor.ecoflow_delta_2_solar_in_watts
        name: Сонячна панель
      - entity: sensor.ecoflow_delta_2_ac_out_watts
        name: AC вихід
      - entity: sensor.ecoflow_delta_2_dc_out_watts
        name: DC вихід
  
  - type: entities
    title: Керування
    entities:
      - entity: switch.ecoflow_delta_2_ac_output
      - entity: switch.ecoflow_delta_2_dc_output
      - entity: switch.ecoflow_delta_2_xboost_enabled
  
  - type: history-graph
    title: Історія (24 години)
    hours_to_show: 24
    entities:
      - entity: sensor.ecoflow_delta_2_battery_level
      - entity: sensor.ecoflow_delta_2_solar_in_watts
```

---

## Скрипти

### 1. Режим економії енергії

```yaml
script:
  ecoflow_power_save_mode:
    alias: "EcoFlow: Режим економії"
    sequence:
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_dc_output
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_xboost_enabled
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_beeper_enabled
```

### 2. Повне увімкнення

```yaml
script:
  ecoflow_full_power_mode:
    alias: "EcoFlow: Повна потужність"
    sequence:
      - service: switch.turn_on
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
      - service: switch.turn_on
        target:
          entity_id: switch.ecoflow_delta_2_dc_output
      - service: switch.turn_on
        target:
          entity_id: switch.ecoflow_delta_2_xboost_enabled
```

### 3. Перезапуск виходів

```yaml
script:
  ecoflow_restart_outputs:
    alias: "EcoFlow: Перезапуск виходів"
    sequence:
      - service: switch.turn_off
        target:
          entity_id:
            - switch.ecoflow_delta_2_ac_output
            - switch.ecoflow_delta_2_dc_output
      - delay:
          seconds: 5
      - service: switch.turn_on
        target:
          entity_id:
            - switch.ecoflow_delta_2_ac_output
            - switch.ecoflow_delta_2_dc_output
```

---

## Шаблони сенсорів

### 1. Залишковий час у годинах

```yaml
template:
  - sensor:
      - name: "EcoFlow Delta 2 Remain Hours"
        unit_of_measurement: "h"
        state: >
          {{ (states('sensor.ecoflow_delta_2_remain_time') | float / 60) | round(1) }}
```

### 2. Статус заряду

```yaml
template:
  - sensor:
      - name: "EcoFlow Delta 2 Charge Status"
        state: >
          {% set level = states('sensor.ecoflow_delta_2_battery_level') | float %}
          {% if level >= 80 %}
            Повний заряд
          {% elif level >= 50 %}
            Достатньо
          {% elif level >= 20 %}
            Низький
          {% else %}
            Критичний
          {% endif %}
        icon: >
          {% set level = states('sensor.ecoflow_delta_2_battery_level') | float %}
          {% if level >= 80 %}
            mdi:battery-high
          {% elif level >= 50 %}
            mdi:battery-medium
          {% elif level >= 20 %}
            mdi:battery-low
          {% else %}
            mdi:battery-alert
          {% endif %}
```

### 3. Ефективність заряду

```yaml
template:
  - sensor:
      - name: "EcoFlow Delta 2 Charge Efficiency"
        unit_of_measurement: "%"
        state: >
          {% set input = states('sensor.ecoflow_delta_2_input_watts') | float %}
          {% if input > 0 %}
            {{ ((input / 1200) * 100) | round(0) }}
          {% else %}
            0
          {% endif %}
```

Ці приклади допоможуть вам максимально використати можливості інтеграції EcoFlow Delta 2 у вашому Home Assistant!
