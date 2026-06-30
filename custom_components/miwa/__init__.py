"""MIWA integration."""

from __future__ import annotations

import logging
import re

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from requests.exceptions import ConnectionError

from .client import MIWAClient
from .const import COORDINATOR_UPDATE_INTERVAL, DOMAIN, PLATFORMS
from .exceptions import MIWAException, MIWAServiceException
from .models import MIWAItem

_LOGGER = logging.getLogger(__name__)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old config entries."""
    _LOGGER.info("Migrating MIWA integration from version %s", config_entry.version)

    # If version is None or 1, treat as version 1
    if config_entry.version is None or config_entry.version < 2:
        # Migration from version 1 to 2: Remove old individual aanrekening sensors
        _LOGGER.info("Starting migration: Removing old individual aanrekening sensors")

        entity_registry = er.async_get(hass)

        # Pattern to match old aanrekening sensors: sensor.miwa_*_aanrekening_*
        # But exclude the new ones: sensor.miwa_*_aanrekeningen and sensor.miwa_*_laatste_aanrekening
        old_sensor_pattern = re.compile(r"^sensor\.miwa_.*_aanrekening_\d{8}t\d{12}z$")

        entities_to_remove = []

        # Find all MIWA entities
        for entity_id, entry in entity_registry.entities.items():
            if entry.platform == DOMAIN and entity_id.startswith("sensor.miwa_"):
                _LOGGER.debug(f"Found: {entity_id}")
                # Check if this is an old individual aanrekening sensor
                if old_sensor_pattern.match(entity_id):
                    entities_to_remove.append(entity_id)
                    _LOGGER.info(f"Found old aanrekening sensor to remove: {entity_id}")

        # Remove the old entities
        for entity_id in entities_to_remove:
            try:
                entity_registry.async_remove(entity_id)
                _LOGGER.info(f"Successfully removed old sensor: {entity_id}")
            except Exception as e:
                _LOGGER.error(f"Failed to remove sensor {entity_id}: {e}")

        if entities_to_remove:
            _LOGGER.info(
                f"Migration completed: Removed {len(entities_to_remove)} old aanrekening sensors"
            )
        else:
            _LOGGER.info(
                "Migration completed: No old aanrekening sensors found to remove"
            )

        # Update version to 2
        hass.config_entries.async_update_entry(config_entry, version=2)
        _LOGGER.info("Migration to version 2 completed")

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MIWA from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    client = MIWAClient(
        email=entry.data[CONF_EMAIL],
        password=entry.data[CONF_PASSWORD],
    )

    dev_reg = dr.async_get(hass)
    hass.data[DOMAIN][entry.entry_id] = coordinator = MIWADataUpdateCoordinator(
        hass,
        config_entry=entry,
        dev_reg=dev_reg,
        client=client,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class MIWADataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for MIWA."""

    data: list[MIWAItem]
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        dev_reg: dr.DeviceRegistry,
        client: MIWAClient,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=COORDINATOR_UPDATE_INTERVAL,
            config_entry=config_entry,
        )
        self._config_entry_id = config_entry.entry_id
        self._device_registry = dev_reg
        self.client = client
        self.hass = hass

    async def _async_update_data(self) -> dict | None:
        """Update data."""
        try:
            items = await self.hass.async_add_executor_job(self.client.fetch_data)
        except ConnectionError as exception:
            raise UpdateFailed(f"ConnectionError {exception}") from exception
        except MIWAServiceException as exception:
            raise UpdateFailed(f"MIWAServiceException {exception}") from exception
        except MIWAException as exception:
            raise UpdateFailed(f"MIWAException {exception}") from exception
        except Exception as exception:
            raise UpdateFailed(f"Exception {exception}") from exception
        items: list[MIWAItem] = items

        current_items = {
            list(device.identifiers)[0][1]
            for device in dr.async_entries_for_config_entry(
                self._device_registry, self._config_entry_id
            )
        }

        if items and len(items) > 0:
            fetched_items = {str(items[item].device_key) for item in items}
            _LOGGER.debug(
                f"[init|MIWADataUpdateCoordinator|_async_update_data|fetched_items] {fetched_items}"
            )
            if stale_items := current_items - fetched_items:
                for device_key in stale_items:
                    if device := self._device_registry.async_get_device(
                        {(DOMAIN, device_key)}
                    ):
                        _LOGGER.debug(
                            f"[init|MIWADataUpdateCoordinator|_async_update_data|async_remove_device] {device_key}",
                            True,
                        )
                        self._device_registry.async_remove_device(device.id)

            # If there are new items, we should reload the config entry so we can
            # create new devices and entities.
            if self.data and fetched_items - {
                str(self.data[item].device_key) for item in self.data
            }:
                # _LOGGER.debug(f"[init|MIWADataUpdateCoordinator|_async_update_data|async_reload] {product.product_name}")
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self._config_entry_id)
                )
                return None
            return items
        else:
            _LOGGER.critical("AIAIAI")
        return []
