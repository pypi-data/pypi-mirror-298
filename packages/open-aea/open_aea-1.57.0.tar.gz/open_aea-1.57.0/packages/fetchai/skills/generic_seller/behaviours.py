# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains the behaviour of a generic seller AEA."""

from typing import Any, Optional, cast

from aea.helpers.search.models import Description
from aea.skills.behaviours import TickerBehaviour

from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.generic_seller.dialogues import (
    LedgerApiDialogues,
    OefSearchDialogues,
)
from packages.fetchai.skills.generic_seller.strategy import GenericStrategy
from packages.valory.connections.ledger.connection import (
    PUBLIC_ID as LEDGER_CONNECTION_PUBLIC_ID,
)
from packages.valory.protocols.ledger_api.message import LedgerApiMessage


DEFAULT_SERVICES_INTERVAL = 60.0
DEFAULT_MAX_SOEF_REGISTRATION_RETRIES = 5
LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)


class GenericServiceRegistrationBehaviour(TickerBehaviour):
    """This class implements a behaviour."""

    def __init__(self, **kwargs: Any):
        """Initialise the behaviour."""
        services_interval = kwargs.pop(
            "services_interval", DEFAULT_SERVICES_INTERVAL
        )  # type: int
        self._max_soef_registration_retries = kwargs.pop(
            "max_soef_registration_retries", DEFAULT_MAX_SOEF_REGISTRATION_RETRIES
        )  # type: int
        super().__init__(tick_interval=services_interval, **kwargs)

        self.failed_registration_msg = None  # type: Optional[OefSearchMessage]
        self._nb_retries = 0

    def setup(self) -> None:
        """Implement the setup."""
        strategy = cast(GenericStrategy, self.context.strategy)
        if strategy.is_ledger_tx:
            ledger_api_dialogues = cast(
                LedgerApiDialogues, self.context.ledger_api_dialogues
            )
            ledger_api_msg, _ = ledger_api_dialogues.create(
                counterparty=LEDGER_API_ADDRESS,
                performative=LedgerApiMessage.Performative.GET_BALANCE,
                ledger_id=strategy.ledger_id,
                address=cast(str, self.context.agent_addresses.get(strategy.ledger_id)),
            )
            self.context.outbox.put_message(message=ledger_api_msg)
        self._register_agent()

    def act(self) -> None:
        """Implement the act."""
        self._retry_failed_registration()

    def teardown(self) -> None:
        """Implement the task teardown."""
        self._unregister_service()
        self._unregister_agent()

    def _retry_failed_registration(self) -> None:
        """Retry a failed registration."""
        if self.failed_registration_msg is not None:
            self._nb_retries += 1
            if self._nb_retries > self._max_soef_registration_retries:
                self.context.is_active = False
                return

            oef_search_dialogues = cast(
                OefSearchDialogues, self.context.oef_search_dialogues
            )
            oef_search_msg, _ = oef_search_dialogues.create(
                counterparty=self.failed_registration_msg.to,
                performative=self.failed_registration_msg.performative,
                service_description=self.failed_registration_msg.service_description,
            )
            self.context.outbox.put_message(message=oef_search_msg)
            self.context.logger.info(
                f"Retrying registration on SOEF. Retry {self._nb_retries} out of {self._max_soef_registration_retries}."
            )

            self.failed_registration_msg = None

    def _register(self, description: Description, logger_msg: str) -> None:
        """
        Register something on the SOEF.

        :param description: the description of what is being registered
        :param logger_msg: the logger message to print after the registration
        """
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info(logger_msg)

    def _register_agent(self) -> None:
        """Register the agent's location."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_location_description()
        self._register(description, "registering agent on SOEF.")

    def register_service(self) -> None:
        """Register the agent's service."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_register_service_description()
        self._register(description, "registering agent's service on the SOEF.")

    def register_genus(self) -> None:
        """Register the agent's personality genus."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_register_personality_description()
        self._register(
            description, "registering agent's personality genus on the SOEF."
        )

    def register_classification(self) -> None:
        """Register the agent's personality classification."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_register_classification_description()
        self._register(
            description, "registering agent's personality classification on the SOEF."
        )

    def _unregister_service(self) -> None:
        """Unregister service from the SOEF."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_unregister_service_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering service from SOEF.")

    def _unregister_agent(self) -> None:
        """Unregister agent from the SOEF."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_location_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering agent from SOEF.")
