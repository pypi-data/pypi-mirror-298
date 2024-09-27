import os
import logging
import time

from b3platform.b3integrations.core import AbstractIntegrationCommand

from b3integration_test.apps import B3IntegrationTestConfig


class Command(AbstractIntegrationCommand):

    @property
    def integration_name(self) -> "str":
        return B3IntegrationTestConfig.name

    @property
    def command_name(self):
        s = os.path.basename(__file__).split(".")[0]
        return s

    def get_logger(self) -> "logging.Logger":
        return logging.getLogger("b3")

    def handle(self, *args, **options) -> None:
        log = self.get_logger()
        log.info("Начало работы программы.")
        time.sleep(30)
        log.info("Завершение работы программы.")
