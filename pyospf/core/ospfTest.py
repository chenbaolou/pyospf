# !/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from pyospf.protocols.exchange import ExchangeProtocol

LOG = logging.getLogger(__name__)


class OspfTest(object):
    """
    A global skeleton OSPF statistics
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OspfTest, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.total_received_packet_count = 0
        self.total_handled_packet_count = 0
        self.recv_hello_count = 0
        self.recv_dd_count = 0
        self.recv_lsr_count = 0
        self.recv_lsu_count = 0
        self.recv_lsack_count = 0
        self.total_send_packet_count = 0
        self.send_hello_count = 0
        self.send_dd_count = 0
        self.send_lsr_count = 0
        self.send_lsu_count = 0
        self.send_lsack_count = 0

    def send_lsu(self):
        pass
