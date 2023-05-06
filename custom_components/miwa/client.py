"""MIWA API Client."""
from __future__ import annotations

import json
import urllib

from bs4 import BeautifulSoup
from requests import (
    Session,
)

from .const import BASE_HEADERS
from .const import CONNECTION_RETRY
from .const import DEFAULT_MIWA_ENVIRONMENT
from .const import REQUEST_TIMEOUT
from .exceptions import BadCredentialsException
from .exceptions import MIWAServiceException
from .models import MIWAEnvironment
from .models import MIWAItem
from .utils import format_entity_name
from .utils import log_debug


class MIWAClient:
    """MIWA client."""

    session: Session
    environment: MIWAEnvironment

    def __init__(
        self,
        session: Session | None = None,
        email: str | None = None,
        password: str | None = None,
        headers: dict | None = BASE_HEADERS,
        environment: MIWAEnvironment = DEFAULT_MIWA_ENVIRONMENT,
    ) -> None:
        """Initialize MIWAClient."""
        self.session = session if session else Session()
        self.email = email
        self.password = password
        self.environment = environment
        self.session.headers = headers
        self.request_error = {}

    def request(
        self,
        url,
        caller="Not set",
        data=None,
        expected="200",
        parse=False,
        log=False,
        retrying=False,
        connection_retry_left=CONNECTION_RETRY,
    ) -> dict:
        """Send a request to MIWA."""
        if data is None:
            log_debug(f"{caller} Calling GET {url}")
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
        else:
            log_debug(f"{caller} Calling POST {url} with {data}")
            response = self.session.post(url, data, timeout=REQUEST_TIMEOUT)
        self.session.headers["x-xsrf-token"] = urllib.parse.unquote(
            self.session.cookies.get("XSRF-TOKEN"), encoding="utf-8", errors="replace"
        )

        log_debug(
            f"{caller} http status code = {response.status_code} (expecting {expected})"
        )
        if log:
            log_debug(f"{caller} response:\n{response.text}")
        if expected is not None and response.status_code != expected:
            if response.status_code == 404:
                self.request_error = response.json()
                return False
            if response.status_code == 401:
                raise BadCredentialsException(response.text)
            if (
                response.status_code != 403
                and response.status_code != 500
                and connection_retry_left > 0
                and not retrying
            ):
                raise MIWAServiceException(
                    f"[{caller}] Expecting HTTP {expected} | response HTTP {response.status_code}, response: {response.text}, Url: {response.url}"
                )
            log_debug(
                f"[MIWAClient|request] Received a HTTP {response.status_code}, nothing to worry about! We give it another try :-)"
            )
            self.login()
            response = self.request(
                url, caller, data, expected, parse, log, True, connection_retry_left - 1
            )
        if parse:
            soup = BeautifulSoup(response.text, "html.parser")
            tag = soup.find("div", {"id": "app"})
            return json.loads(tag.get("data-page")).get("props")
        return response

    def login(self) -> dict:
        """Start a new MIWA session with a user & password."""

        log_debug("[MIWAClient|login|start]")
        """Login process"""
        if self.email is None or self.password is None:
            return False
        response = self.request(
            f"{self.environment.api_endpoint}/login",
            "[MIWAClient|login|get csrf]",
            None,
            200,
        )
        response = self.request(
            f"{self.environment.api_endpoint}/login",
            "[MIWAClient|login|authenticate]",
            {"email": self.email, "password": self.password},
            200,
            parse=True,
        )
        return response.get("auth").get("user")

    def mijn_adressen(self):
        """Get adressen."""
        response = self.request(
            f"{self.environment.api_endpoint}/mijn-adressen",
            "[MIWAClient|mijn_adressen]",
            None,
            200,
            parse=True,
        )
        return response.get("addresses")

    def ledigingen(self, address_path):
        """Get ledigingen."""
        response = self.request(
            f"{self.environment.api_endpoint}/{address_path}/mijn-verbruik/ledigingen?fromDate=01%2F01%2F2010",
            f"[MIWAClient|{address_path}|ledigingen]",
            None,
            200,
            parse=True,
        )
        return response

    def mijn_aanrekeningen(self, address_path):
        """Get aanrekeningen."""
        response = self.request(
            f"{self.environment.api_endpoint}/{address_path}/mijn-aanrekeningen/overzicht",
            f"[MIWAClient|{address_path}|mijn_aanrekeningen]",
            None,
            200,
            parse=True,
        )
        return response.get("invoices")

    def facturatie_instellingen(self, address_path):
        """Get facturatie instellingen."""
        response = self.request(
            f"{self.environment.api_endpoint}/{address_path}/mijn-aanrekeningen/facturatie-instellingen",
            f"[MIWAClient|{address_path}|facturatie_instellingen]",
            None,
            200,
            parse=True,
        )
        return response

    def mijn_producten(self, address_path):
        """Get aanrekeningen."""
        response = self.request(
            f"{self.environment.api_endpoint}/{address_path}/mijn-producten",
            f"[MIWAClient|{address_path}|mijn_producten]",
            None,
            200,
            parse=True,
        )
        return response.get("products")

    def fetch_data(self):
        """Fetch MIWA data."""
        data = {}
        user_info = self.login()
        if not user_info:
            return False
        email = user_info.get("email")
        device_key = format_entity_name(f"user {email}")
        device_name = f"Account {email}"
        device_model = "User"
        key = format_entity_name(f"{email} email")
        data[key] = MIWAItem(
            name="Email",
            key=key,
            type="email",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=email,
            extra_attributes=user_info,
        )
        key = format_entity_name(f"{email} first_name")
        data[key] = MIWAItem(
            name="Voornaam",
            key=key,
            type="info",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=user_info.get("first_name"),
            extra_attributes=user_info,
        )
        key = format_entity_name(f"{email} last_name")
        data[key] = MIWAItem(
            name="Achternaam",
            key=key,
            type="info",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=user_info.get("last_name"),
            extra_attributes=user_info,
        )
        key = format_entity_name(f"{email} telephone")
        data[key] = MIWAItem(
            name="Telefoon- of gsm-nummer",
            key=key,
            type="info",
            device_key=device_key,
            device_name=device_name,
            device_model=device_model,
            state=user_info.get("telephone"),
            extra_attributes=user_info,
        )

        for address in self.mijn_adressen():
            log_debug(
                f"Adres: {address.get('street_name')} {address.get('house_number')}, {address.get('zipcode')} {address.get('city')}"
            )
            address_id = address.get("id")
            device_key = format_entity_name(f"address_id {address_id}")
            device_name = (
                f"Adres {address.get('street_name')} {address.get('house_number')}"
            )
            device_model = "Adres"
            key = format_entity_name(f"{address_id} adres")
            data[key] = MIWAItem(
                name=f"{address.get('street_name')} {address.get('house_number')}, {address.get('zipcode')} {address.get('city')}",
                key=key,
                type="address",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=address.get("inhabitant_category"),
                extra_attributes=address,
            )
            address_path = "mijn-adressen/" + address_id
            ledigingen = self.ledigingen(address_path)
            log_debug(
                f"Huidige balans: {ledigingen.get('linkedAddress').get('current_balance')} EUR"
            )
            key = format_entity_name(f"{address_id} huidige balans")
            data[key] = MIWAItem(
                name="Huidige balans",
                key=key,
                type="euro",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=ledigingen.get("linkedAddress").get("current_balance"),
            )
            key = format_entity_name(f"{address_id} totaal ledigingen gewicht")
            data[key] = MIWAItem(
                name="Totaal gewicht ledigingen",
                key=key,
                type="gewicht",
                device_key=device_key,
                device_name=device_name,
                device_model=device_model,
                state=ledigingen.get("totalWeightOfEmptyings") / 1000,
            )
            log_debug(
                f"Ledigingen van {ledigingen.get('fromDate')} tot heden ({ledigingen.get('totalWeightOfEmptyings')/1000} kg)"
            )

            for emptying in ledigingen.get("emptyings"):
                key = format_entity_name(
                    f"{address_id} lediging {emptying.get('emptied_on')}"
                )
                data[key] = MIWAItem(
                    name=f"Lediging {emptying.get('emptied_on')[0:10]} {emptying.get('fraction')} {emptying.get('type')} {emptying.get('volume')}L",
                    key=key,
                    type="gewicht",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state=emptying.get("weight") / 1000,
                    extra_attributes=emptying,
                )
                log_debug(
                    f"  - {emptying.get('emptied_on')}, {emptying.get('fraction')} {emptying.get('type')} {emptying.get('volume')}L: {emptying.get('weight')/1000} kg"
                )
            for invoice in self.mijn_aanrekeningen(address_path):
                key = format_entity_name(
                    f"{address_id} aanrekening {invoice.get('invoiced_on')}"
                )
                data[key] = MIWAItem(
                    name=f"Aanrekening {invoice.get('invoiced_on')[0:10]}",
                    key=key,
                    type="euro",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state=invoice.get("amount_invoiced") / 100,
                    extra_attributes=invoice,
                )
                log_debug(
                    f"  - {invoice.get('invoiced_on')}: {invoice.get('amount_invoiced')/100} EUR [{invoice.get('status')}|{invoice.get('billing_method')}]"
                )
            facturatie_instellingen = self.facturatie_instellingen(address_path)
            log_debug("Verzend- en betaalmethoden:")
            log_debug(f"  Methode: {facturatie_instellingen.get('deliveryMethod')}")
            key = format_entity_name(f"{address_id} aanrekening methode")
            if facturatie_instellingen.get("deliveryMethod") == "e-mail":
                data[key] = MIWAItem(
                    name="Verzendmethode aanrekening",
                    key=key,
                    type="euro",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state="Per email",
                    extra_attributes=facturatie_instellingen,
                )
                log_debug(f"  Ontvanger: {facturatie_instellingen.get('email')}")
                log_debug(
                    f"  Verzender: {facturatie_instellingen.get('invoiceSenderEmail')}"
                )
            else:
                data[key] = MIWAItem(
                    name="Verzendmethode aanrekening",
                    key=key,
                    type="euro",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state="Per post",
                    extra_attributes=facturatie_instellingen,
                )
                address = facturatie_instellingen.get("invoiceAddress")
                log_debug(
                    f"  Adres: {address.get('address_line')}, {address.get('postal_code')} {address.get('city')}"
                )
            log_debug("Producten:")
            for product in self.mijn_producten(address_path):
                log_debug(
                    f"  - {product.get('name')} [sinds {product.get('active_since')}]"
                )
                key = format_entity_name(f"{address_id} product {product.get('name')}")
                data[key] = MIWAItem(
                    name=f"{product.get('name')}",
                    key=key,
                    type="product",
                    device_key=device_key,
                    device_name=device_name,
                    device_model=device_model,
                    state=product.get("status"),
                    extra_attributes=product,
                )
        return data
