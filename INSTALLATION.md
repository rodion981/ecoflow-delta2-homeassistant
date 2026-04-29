# Інструкція з встановлення

## Швидкий старт

### 1. Підготовка API ключів

Перед встановленням вам потрібно отримати API ключі від EcoFlow:

#### Крок 1: Реєстрація на порталі розробників
- **Для Європи**: https://developer-eu.ecoflow.com
- **Для США**: https://developer.ecoflow.com

#### Крок 2: Створення додатку
1. Увійдіть в акаунт
2. Перейдіть в розділ "Applications"
3. Натисніть "Create Application"
4. Заповніть форму:
   - Application Name: `Home Assistant`
   - Description: `Integration for Home Assistant`
5. Збережіть **Access Key** та **Secret Key** (вони знадобляться при налаштуванні)

#### Крок 3: Знайдіть серійний номер пристрою
1. Відкрийте мобільний додаток EcoFlow
2. Виберіть ваш Delta 2
3. Натисніть на іконку налаштувань (⚙️)
4. Знайдіть "Device Information" або "About"
5. Скопіюйте **Serial Number** (формат: R331...)

---

## Встановлення

### Варіант 1: Ручне встановлення

1. **Завантажте інтеграцію**
   ```bash
   cd /config
   mkdir -p custom_components
   ```

2. **Скопіюйте файли**
   - Скопіюйте всю папку `custom_components/ecoflow_delta2` в `/config/custom_components/`
   - Структура повинна бути: `/config/custom_components/ecoflow_delta2/`

3. **Перезапустіть Home Assistant**
   - Settings → System → Restart

4. **Додайте інтеграцію**
   - Settings → Devices & Services → Add Integration
   - Знайдіть "EcoFlow Delta 2"
   - Введіть ваші дані:
     - Access Key: `ваш_access_key`
     - Secret Key: `ваш_secret_key`
     - Device SN: `R331XXXXXXXXXX`
     - Region: `eu` або `us`

### Варіант 2: Через HACS (майбутнє)

Після публікації в HACS:
1. Відкрийте HACS → Integrations
2. Натисніть "+" → Search for "EcoFlow Delta 2"
3. Натисніть "Download"
4. Перезапустіть Home Assistant
5. Додайте інтеграцію через UI

---

## Перевірка встановлення

Після успішного додавання інтеграції ви побачите:

### Пристрій
- **Devices & Services** → **EcoFlow Delta 2**
- Інформація про пристрій: модель, серійний номер, виробник

### Сенсори (20+)
- `sensor.ecoflow_delta_2_battery_level` - Рівень заряду батареї
- `sensor.ecoflow_delta_2_battery_temp` - Температура батареї
- `sensor.ecoflow_delta_2_input_watts` - Загальна вхідна потужність
- `sensor.ecoflow_delta_2_output_watts` - Загальна вихідна потужність
- `sensor.ecoflow_delta_2_ac_in_watts` - AC вхідна потужність
- `sensor.ecoflow_delta_2_ac_out_watts` - AC вихідна потужність
- `sensor.ecoflow_delta_2_solar_in_watts` - Сонячна потужність
- І багато інших...

### Перемикачі (4)
- `switch.ecoflow_delta_2_ac_output` - AC вихід
- `switch.ecoflow_delta_2_dc_output` - DC вихід
- `switch.ecoflow_delta_2_xboost_enabled` - X-Boost
- `switch.ecoflow_delta_2_beeper_enabled` - Звуковий сигнал

---

## Налаштування оновлень

За замовчуванням дані оновлюються кожні 30 секунд. Щоб змінити інтервал:

1. Відредагуйте файл `custom_components/ecoflow_delta2/__init__.py`
2. Знайдіть рядок:
   ```python
   update_interval=timedelta(seconds=30),
   ```
3. Змініть значення (наприклад, на 60 секунд):
   ```python
   update_interval=timedelta(seconds=60),
   ```
4. Перезапустіть Home Assistant

---

## Додавання до Lovelace Dashboard

### Приклад картки

```yaml
type: entities
title: EcoFlow Delta 2
entities:
  - entity: sensor.ecoflow_delta_2_battery_level
    name: Заряд батареї
  - entity: sensor.ecoflow_delta_2_battery_temp
    name: Температура
  - entity: sensor.ecoflow_delta_2_input_watts
    name: Вхідна потужність
  - entity: sensor.ecoflow_delta_2_output_watts
    name: Вихідна потужність
  - entity: sensor.ecoflow_delta_2_solar_in_watts
    name: Сонячна потужність
  - entity: switch.ecoflow_delta_2_ac_output
    name: AC вихід
  - entity: switch.ecoflow_delta_2_dc_output
    name: DC вихід
```

### Приклад gauge картки

```yaml
type: gauge
entity: sensor.ecoflow_delta_2_battery_level
name: Батарея Delta 2
min: 0
max: 100
severity:
  green: 50
  yellow: 30
  red: 0
```

---

## Усунення проблем

### Помилка: "Cannot connect to EcoFlow API"

**Причини:**
- Неправильний Access Key або Secret Key
- Неправильний регіон (EU/US)
- Пристрій не підключений до інтернету

**Рішення:**
1. Перевірте правильність ключів на порталі розробників
2. Переконайтеся, що Delta 2 онлайн в додатку EcoFlow
3. Перевірте, що вибрано правильний регіон
4. Перевірте логи: Settings → System → Logs

### Сенсори показують "Unavailable"

**Причини:**
- Пристрій офлайн
- Проблеми з API
- Перше оновлення ще не відбулося

**Рішення:**
1. Зачекайте 30-60 секунд після додавання
2. Перевірте, що Delta 2 онлайн в додатку
3. Перезавантажте інтеграцію: Devices & Services → EcoFlow Delta 2 → Reload
4. Перевірте логи на помилки

### Перемикачі не реагують

**Причини:**
- Пристрій в захищеному режимі
- Низький заряд батареї
- API обмеження

**Рішення:**
1. Перевірте стан пристрою в додатку EcoFlow
2. Переконайтеся, що батарея має достатній заряд
3. Спробуйте керувати через додаток EcoFlow
4. Зачекайте 30 секунд між командами

### Логи показують помилки підпису (signature errors)

**Причини:**
- Неправильний Secret Key
- Проблеми з часом на сервері

**Рішення:**
1. Перевірте Secret Key
2. Переконайтеся, що час на сервері Home Assistant правильний
3. Видаліть та додайте інтеграцію знову

---

## Оновлення інтеграції

1. Завантажте нову версію
2. Замініть файли в `/config/custom_components/ecoflow_delta2/`
3. Перезапустіть Home Assistant
4. Перевірте, що все працює

---

## Видалення інтеграції

1. Settings → Devices & Services
2. Знайдіть "EcoFlow Delta 2"
3. Натисніть "..." → "Delete"
4. Видаліть папку `/config/custom_components/ecoflow_delta2/`
5. Перезапустіть Home Assistant

---

## Підтримка

Якщо у вас виникли проблеми:
1. Перевірте розділ "Усунення проблем" вище
2. Перегляньте логи Home Assistant
3. Переконайтеся, що Delta 2 працює в додатку EcoFlow
4. Створіть issue на GitHub з детальним описом та логами
