<img src="https://github.com/geertmeersman/miwa/raw/main/images/brand/logo.png"
     alt="MIWA Logo"
     align="right"
     style="width: 200px; margin-right: 10px;" />

# MIWA for Home Assistant

A Home Assistant integration to monitor **Mijn MIWA** consumption.

Make sure you use the credentials from the website https://mijnmiwa.be/login

## Features

- 🗑️ Emptying sensors
- 📈 Invoice sensors
- 👤 User account information

---


[![Maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![Buy me an Omer](https://img.shields.io/badge/Buy%20me%20an%20Omer-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![Discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/BTW6S9m3)

[![MIT License](https://img.shields.io/github/license/geertmeersman/miwa?style=flat-square)](https://github.com/geertmeersman/miwa/blob/master/LICENSE)
[![HACS Default](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=miwa&category=integration)

[![GitHub Issues](https://img.shields.io/github/issues/geertmeersman/miwa)](https://github.com/geertmeersman/miwa/issues)
[![Resolve Time](http://isitmaintained.com/badge/resolution/geertmeersman/miwa.svg)](http://isitmaintained.com/project/geertmeersman/miwa)
[![Open Issues](http://isitmaintained.com/badge/open/geertmeersman/miwa.svg)](http://isitmaintained.com/project/geertmeersman/miwa)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/miwa/pulls)

[![Validation Status](https://github.com/geertmeersman/miwa/actions/workflows/validate.yml/badge.svg)](https://github.com/geertmeersman/miwa/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/miwa/search?l=python)
[![Latest Release](https://img.shields.io/github/v/release/geertmeersman/miwa?logo=github)](https://github.com/geertmeersman/miwa/releases)
[![Last Commit](https://img.shields.io/github/last-commit/geertmeersman/miwa)](https://github.com/geertmeersman/miwa/commits)

---
## Table of contents

- [MIWA for Home Assistant](#miwa-for-home-assistant)
  - [Features](#features)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
    - [Using HACS (recommended)](#using-hacs-recommended)
    - [Manual](#manual)
  - [Contributions are welcome!](#contributions-are-welcome)
  - [Troubleshooting](#troubleshooting)
    - [Enable debug logging](#enable-debug-logging)
    - [Disable debug logging and download logs](#disable-debug-logging-and-download-logs)
  - [Screenshots](#screenshots)
  - [Code origin](#code-origin)
## Installation

### Using [HACS](https://hacs.xyz/) (Recommended)

**Click this button to install:**

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=miwa&category=integration)

Or follow these steps:

1. Open HACS and search for `MIWA`.
2. Install the integration.
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Integrations** and add `MIWA`.
5. Enter your MIWA username and password.

### Manual Installation

1. Copy the `custom_components/miwa` directory to `config/custom_components/miwa` in your Home Assistant setup.
2. Restart Home Assistant.
3. Follow steps 4 and 5 from the HACS installation.

#### Supported Platforms

| Platform | Description |
|----------|-------------|
| `miwa`   | Home Assistant component for MIWA BE services |

---

## Contributions

Contributions are welcome! Please read the [Contribution Guidelines](CONTRIBUTING.md) before submitting a PR.

---

## Troubleshooting

### Enable Debug Logging

1. Go to **Settings > Devices & Services**.
2. Click the three dots for the MIWA integration.
3. Select **Enable Debug Logging**.

![Enable Debug Logging](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/enable-debug-logging.gif)

### Disable Debug Logging & Download Logs

1. Follow the same steps as enabling, but select **Disable Debug Logging**.
2. You will be prompted to download the log file. Please provide this when reporting issues.

![Disable Debug Logging](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/disable-debug-logging.gif)

---

## Code Origin

This integration was developed by analyzing network requests made by the MIWA website. The goal is to automate and monitor MIWA usage efficiently.

🚨 **Disclaimer:** This project is not affiliated with MIWA.
