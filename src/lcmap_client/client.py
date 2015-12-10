"""
The client module provides the base class for interacting with the LCMAP
service.

BaseClient is comprised of components (instances of other objects) assigned to
attributes on the class. Some of these components represent the high-level
architecture of the LCMAP service itself, while others are supporting components.
"""
import logging

from requests import Request

from lcmap_client import auth, http, logger
from lcmap_client.config import Config


log = logging.getLogger(__name__)


class BaseClient(object):
    def __init__(self, base_context="", force_reload=False):
        # Client attributes
        self.base_context = base_context

        # API components
        self.compatibility = None
        self.data = None
        self.jobs = None
        self.models = None
        self.notifications = None
        self.systen = None
        self.users = None

        # Supporting components
        self.cfg = None
        self.auth = None
        self.http = None

        # Initialization
        self.initialize(force_reload=force_reload)

    def initialize(self, force_reload=False):
        log.debug("Initializing client components ...")
        self.configure(force_reload=force_reload)
        self.http = http.HTTP(cfg=self.cfg, base_context=self.base_context)
        self.auth = auth.Auth(cfg=self.cfg, http=self.http)

    def configure(self, force_reload=False):
        self.cfg = Config(force_reload=force_reload)
        logger.configure(self.cfg)


    def reload(self):
        self.configure(force_reload=True)
