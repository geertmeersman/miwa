# MIWA Invoices Table - Lovelace Card Example

## 🔧 Installation Instructions

**⚠️ IMPORTANT: First replace the placeholder with your actual sensor name!**

1. **Find your MIWA invoices sensor** in Home Assistant (Developer Tools > States)
2. **Copy the entity_id** (for example: `sensor.miwa_abc123_aanrekeningen`)
3. **Replace** `YOUR_MIWA_SENSOR_NAME` in the examples below with your entity_id
4. **Add the card** to your Lovelace dashboard

---

## Basic Markdown Card

```yaml
type: markdown
title: MIWA Invoices Overview
content: |
  ## Total Invoices: {{ states('sensor.YOUR_MIWA_SENSOR_NAME') }}

  | Date | Amount | Status | Period | Actions |
  |------|--------|--------|--------|---------|
  {% for aanrekening in state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') -%}
  | {{ (aanrekening.datum | as_datetime | as_local).strftime('%d/%m/%Y') }} | €{{ "%.2f"|format(aanrekening.bedrag) }} | {{ aanrekening.status }} | {{ (aanrekening.originele_data.period_from | as_datetime | as_local).strftime('%m/%Y') }} - {{ (aanrekening.originele_data.period_until | as_datetime | as_local).strftime('%m/%Y') }} | [Download]({{ aanrekening.originele_data.download_link }}) |
  {% endfor %}
```

## Extended example with more details

```yaml
type: markdown
title: MIWA Invoices - Detailed View
content: |
  # 🧾 Invoices Overview

  **Total amount:** {{ states('sensor.YOUR_MIWA_SENSOR_NAME') }}
  **Number of invoices:** {{ state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') | length }}
  **Last update:** {{ state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'last_synced') | as_datetime | as_local | strftime('%d/%m/%Y at %H:%M') }}

  ---

  | 📅 Date | 💰 Amount | 📊 Status | 🗓️ Period | 💳 Payment | 📄 Download |
  |----------|-----------|-----------|-------------|-------------|-------------|
  {% for aanrekening in state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') -%}
  | {{ (aanrekening.datum | as_datetime | as_local).strftime('%d/%m/%Y') }} | {% if aanrekening.bedrag > 0 %}**€{{ "%.2f"|format(aanrekening.bedrag) }}**{% else %}€0.00{% endif %} | {% if aanrekening.status == 'closed' %}✅ Paid{% else %}⏳ {{ aanrekening.status }}{% endif %} | {{ (aanrekening.originele_data.period_from | as_datetime | as_local).strftime('%m/%Y') }}-{{ (aanrekening.originele_data.period_until | as_datetime | as_local).strftime('%m/%Y') }} | {{ aanrekening.betaalmethode }} | [📥 PDF]({{ aanrekening.originele_data.download_link }}) |
  {% endfor %}

  ---

  ### 📈 Statistics
  - **Highest invoice:** €{{ state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') | map(attribute='bedrag') | max }}
  - **Lowest invoice:** €{{ state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') | map(attribute='bedrag') | select('>', 0) | min | default(0) }}
  - **Average:** €{{ "%.2f"|format((state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') | map(attribute='bedrag') | sum) / (state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') | length)) }}
```

## Compact version - only recent invoices

```yaml
type: markdown
title: Recent MIWA Invoices (last 5)
content: |
  ## 🧾 Latest Invoices

  | Date | Amount | Status | Download |
  |------|--------|--------|----------|
  {% for aanrekening in state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen')[:5] -%}
  | {{ (aanrekening.datum | as_datetime | as_local).strftime('%d/%m/%Y') }} | {% if aanrekening.bedrag > 0 %}€{{ "%.2f"|format(aanrekening.bedrag) }}{% else %}-{% endif %} | {{ '✅' if aanrekening.status == 'closed' else '⏳' }} | [📄]({{ aanrekening.originele_data.download_link }}) |
  {% endfor %}

  **Total:** {{ states('sensor.YOUR_MIWA_SENSOR_NAME') }}
```

## Card with conditionals for better display

```yaml
type: markdown
title: MIWA Invoices
content: |
  {% set aanrekeningen = state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') %}
  {% if aanrekeningen %}

  # 💰 Total: {{ states('sensor.YOUR_MIWA_SENSOR_NAME') }}

  | 📅 Invoice | 💰 Amount | 🗓️ Period | 📊 Status | 📄 |
  |------------|-----------|------------|----------|-----|
  {% for aanrekening in aanrekeningen -%}
  | {{ (aanrekening.datum | as_datetime | as_local).strftime('%d %b %Y') }} | {% if aanrekening.bedrag == 0 %}🆓 Free{% else %}€{{ "%.2f"|format(aanrekening.bedrag) }}{% endif %} | {{ (aanrekening.originele_data.period_from | as_datetime | as_local).strftime('%b %Y') }} | {% if aanrekening.status == 'closed' %}✅{% elif aanrekening.status == 'open' %}🔴{% else %}{{ aanrekening.status }}{% endif %} | [📥]({{ aanrekening.originele_data.download_link }}) |
  {% endfor %}

  {% else %}

  ⚠️ No invoices available

  {% endif %}
```

## Using in Dashboard

### Step-by-step:
1. **🔍 Find your sensor name:**
   - Go to **Developer Tools** > **States** in Home Assistant
   - Search for `sensor.*miwa*aanrekeningen`
   - Copy the full entity_id (for example: `sensor.miwa_abc123_aanrekeningen`)

2. **📝 Replace placeholder:**
   - Choose one of the card examples above
   - Replace **ALL** `YOUR_MIWA_SENSOR_NAME` with your sensor name
   - Use Find & Replace (Ctrl+H) for easy replacement

3. **➕ Add card:**
   - Go to your Lovelace dashboard
   - Click **"Edit"**
   - Click **"Add Card"**
   - Choose **"Markdown"**
   - Paste your customized code
   - Click **"Save"**

---

## 💡 Extra Tips:
- **🗂️ Sort by date:** Add `| sort(attribute='datum', reverse=true)` after `'aanrekeningen'`
- **📅 Filter by year:** Add `| selectattr('datum', 'match', '2024.*')` for 2024 only
- **🎨 Customize emojis** to your preference
- **📱 Test on mobile** - tables can be narrow on small screens
- **🔄 Auto-update:** Cards update automatically when sensor data changes

### Example of sorting:
```yaml
{% for aanrekening in state_attr('sensor.YOUR_MIWA_SENSOR_NAME', 'aanrekeningen') | sort(attribute='datum', reverse=true) -%}
```

The table automatically displays all invoices with date, amount, status, period, and download links! 🎯
