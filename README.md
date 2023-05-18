<img src="https://github.com/geertmeersman/miwa/raw/main/images/brand/logo.png"
     alt="MIWA"
     align="right"
     style="width: 200px;margin-right: 10px;" />

# MIWA for Home Assistant

A Home Assistant integration to monitor Mijn MIWA consumption

### Features

- Emptying sensors
- 📈 Invoice sensors
- 👱 User account information

---

<!-- [START BADGES] -->
<!-- Please keep comment here to allow auto update -->

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20a%20Duvel-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/BTW6S9m3)

[![MIT License](https://img.shields.io/github/license/geertmeersman/miwa?style=flat-square)](https://github.com/geertmeersman/miwa/blob/master/LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=miwa&category=integration)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/miwa)](https://github.com/geertmeersman/miwa/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/miwa.svg)](http://isitmaintained.com/project/geertmeersman/miwa)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/miwa.svg)](http://isitmaintained.com/project/geertmeersman/miwa)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/miwa/pulls)

[![Hacs and Hassfest validation](https://github.com/geertmeersman/miwa/actions/workflows/validate.yml/badge.svg)](https://github.com/geertmeersman/miwa/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/miwa/search?l=python)

[![manifest version](https://img.shields.io/github/manifest-json/v/geertmeersman/miwa/master?filename=custom_components%2Fmiwa%2Fmanifest.json)](https://github.com/geertmeersman/miwa)
[![github release](https://img.shields.io/github/v/release/geertmeersman/miwa?logo=github)](https://github.com/geertmeersman/miwa/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/miwa)](https://github.com/geertmeersman/miwa/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/miwa)](https://github.com/geertmeersman/miwa/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/miwa)](https://github.com/geertmeersman/miwa/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/miwa?logo=github)](https://github.com/geertmeersman/miwa/commits/main)

<!-- [END BADGES] -->

## Installation

The Pull request is still pending merge for the hacs-default repository. So until that time, add my repository as a custom repository in hacs and the integration will show up.

Explanation: https://hacs.xyz/docs/faq/custom_repositories/

```
Repository: geertmeersman/miwa
Category: Integration
```

### Using [HACS](https://hacs.xyz/) (recommended)

1. Simply search for `MIWA` in HACS and install it easily.
2. Restart Home Assistant
3. Add the 'MIWA' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your MIWA username and password

### Manual

1. Copy the `custom_components/miwa` directory of this repository as `config/custom_components/miwa` in your Home Assistant instalation.
2. Restart Home Assistant
3. Add the 'MIWA' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your MIWA username and password

This integration will set up the following platforms.

| Platform | Description                                   |
| -------- | --------------------------------------------- |
| `miwa`   | Home Assistant component for MIWA BE services |

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting

1. You can enable logging for this integration specifically and share your logs, so I can have a deep dive investigation. To enable logging, update your `configuration.yaml` like this, we can get more information in Configuration -> Logs page

```
logger:
  default: warning
  logs:
    custom_components.miwa: debug
```

## Screenshots

## Code origin

The code of this Home Assistant integration has been written by analysing the calls made by the MIWA website. Goal is to automate as much as possible and to monitor usage.

I have no link with MIWA
