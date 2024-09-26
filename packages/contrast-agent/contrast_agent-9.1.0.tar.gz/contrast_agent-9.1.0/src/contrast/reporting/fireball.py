# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.reporting.reporting_client import ReportingClient


class Client(ReportingClient):
    """
    A client for reporting to the Contrast UI using the Fireball library.
    Fireball docs: https://fireball.prod.dotnet.contsec.com/fireball/index.html

    The client will fallback to directly reporting for endpoints that do not
    have Python bindings yet.
    """

    ...
