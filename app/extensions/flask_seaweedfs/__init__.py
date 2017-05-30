# encoding: utf-8
"""
SeaweedFS adapter
-----------------
"""
from pyseaweed import WeedFS as BaseWeedFS


class SeaweedFS(BaseWeedFS):

    def init_app(self, app):
        """
        Initilizes SeaweedFS instance with proper addr and port.
        """
        self.master_addr = app.config['SEAWEEDFS_CONFIG']['MASTER_ADDR']
        self.master_port = app.config['SEAWEEDFS_CONFIG']['MASTER_PORT']
