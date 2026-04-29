# EcoFlow Delta 2 Integration for Home Assistant

Кастомна інтеграція для Home Assistant, яка дозволяє моніторити та керувати вашою EcoFlow Delta 2 через офіційний EcoFlow API.

## Можливості

### Сенсори (20+)
- **Батарея**: рівень заряду, температура, напруга, струм, цикли, стан здоров'я (SOH)
- **Потужність**: загальна вхідна/вихідна потужність, AC вхід/вихід, сонячний вхід, DC вихід
- **USB порти**: Type-C (2x), USB-A (2x) - потужність кожного порту
- **Напруга**: AC вхід/вихід, сонячна панель, батарея
- **Час**: залишковий час роботи

### Перемикачі (4)
- AC вихід (увімкнути/вимкнути)
- DC вихід (увімкнути/вимкнути)
- X-Boost (увімкнути/вимкнути)
- Звуковий сигнал (увімкнути/вимкнути)

## Встановлення

### Крок 1: Отримання API ключів

1. Зареєструйтеся на порталі розробників EcoFlow:
   - Європа: https://developer-eu.ecoflow.com
   - США: https://developer.ecoflow.com

2. Створіть додаток та отримайте:
   - Access Key
   - Secret Key

3. Знайдіть серійний номер вашого пристрою (Device SN):
   - Відкрийте додаток EcoFlow
   - Виберіть ваш Delta 2
   - Серійний номер знаходиться в налаштуваннях пристрою

### Крок 2: Встановлення інтеграції

#### Варіант A: Через SSH/Terminal (Рекомендовано)

1. Підключіться до вашого Home Assistant через SSH або Terminal

2. Виконайте команди:
   ```bash
   cd /config
   git clone https://github.com/ВАШЕ_ІМЯ/ecoflow-delta2-homeassistant.git temp_ecoflow
   mkdir -p custom_components
   cp -r temp_ecoflow/custom_components/ecoflow_delta2 custom_components/
   rm -rf temp_ecoflow
   ```

3. Перезапустіть Home Assistant

4. Перейдіть до **Settings** → **Devices & Services** → **Add Integration**

5. Знайдіть "EcoFlow Delta 2" та введіть ваші дані

#### Варіант B: Через File Editor addon

1. Встановіть "File Editor" addon в Home Assistant (якщо ще не встановлено)

2. Відкрийте File Editor

3. Створіть папку `custom_components/ecoflow_delta2`

4. Завантажте файли з GitHub:
   - Відкрийте https://github.com/ВАШЕ_ІМЯ/ecoflow-delta2-homeassistant
   - Перейдіть в `custom_components/ecoflow_delta2`
   - Скопіюйте вміст кожного файлу в File Editor

5. Перезапустіть Home Assistant

#### Варіант C: Через Samba/SMB

1. Підключіться до Home Assistant через Samba/SMB

2. Відкрийте папку `config`

3. Створіть папку `custom_components/ecoflow_delta2`

4. Завантажте та скопіюйте файли з GitHub в цю папку

5. Перезапустіть Home Assistant

## Використання

### Приклади автоматизацій

#### Сповіщення при низькому заряді
```yaml
automation:
  - alias: "EcoFlow Low Battery Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        below: 20
    action:
      - service: notify.mobile_app
        data:
          message: "EcoFlow Delta 2 заряд батареї нижче 20%!"
```

#### Автоматичне вимкнення AC при повному заряді
```yaml
automation:
  - alias: "EcoFlow Turn Off AC When Full"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_battery_level
        above: 99
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
```

#### Увімкнення AC коли є сонячна енергія
```yaml
automation:
  - alias: "EcoFlow Enable AC on Solar"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ecoflow_delta_2_solar_in_watts
        above: 100
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.ecoflow_delta_2_ac_output
```

### Energy Dashboard

Ви можете додати сенсори до Energy Dashboard:

1. Перейдіть до **Settings** → **Dashboards** → **Energy**
2. Додайте сенсори:
   - **Solar Production**: `sensor.ecoflow_delta_2_solar_in_watts`
   - **Battery Storage**: `sensor.ecoflow_delta_2_battery_level`
   - **Grid Consumption**: `sensor.ecoflow_delta_2_ac_in_watts`

## Структура проєкту

```
custom_components/ecoflow_delta2/
├── __init__.py           # Ініціалізація інтеграції
├── manifest.json         # Метадані інтеграції
├── const.py             # Константи
├── config_flow.py       # Налаштування через UI
├── ecoflow_api.py       # API клієнт для EcoFlow
├── sensor.py            # Сенсори (батарея, потужність, тощо)
└── switch.py            # Перемикачі (AC, DC, X-Boost, тощо)
```

## Технічні деталі

- **API**: Офіційний EcoFlow Developer API (REST + MQTT)
- **Оновлення**: Кожні 30 секунд
- **Аутентифікація**: HMAC-SHA256 підпис
- **Регіони**: Підтримка EU та US серверів

## Відомі обмеження

- Потрібне підключення до інтернету (хмарний API)
- Delta 2 повинна бути підключена до WiFi
- Оновлення даних кожні 30 секунд (можна змінити в коді)

## Усунення несправностей

### Помилка "Cannot connect to EcoFlow API"
- Перевірте правильність Access Key та Secret Key
- Переконайтеся, що вибрано правильний регіон (EU/US)
- Перевірте, що Delta 2 підключена до WiFi та онлайн в додатку EcoFlow

### Сенсори показують "Unknown" або "Unavailable"
- Зачекайте 30-60 секунд після додавання інтеграції
- Перевірте логи Home Assistant: **Settings** → **System** → **Logs**
- Перезапустіть інтеграцію: **Settings** → **Devices & Services** → **EcoFlow Delta 2** → **Reload**

### Перемикачі не працюють
- Переконайтеся, що у вас є права на керування пристроєм в додатку EcoFlow
- Деякі команди можуть не працювати, якщо пристрій в певному стані (наприклад, AC вихід не можна увімкнути при низькому заряді)

## Підтримка

Якщо у вас виникли проблеми або питання:
1. Перевірте логи Home Assistant
2. Переконайтеся, що ваш Delta 2 працює в додатку EcoFlow
3. Створіть issue на GitHub з детальним описом проблеми та логами

## Ліцензія

MIT License

## Подяки

Дякую спільноті Home Assistant та розробникам існуючих EcoFlow інтеграцій за натхнення та документацію.
