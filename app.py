#!/usr/bin/python3
# -*- coding":" utf-8 -*-

# ------------------------------------------------------------------
# HA MQTT Discovery Item Builder
# ------------------------------------------------------------------
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Distribution License
# which accompanies this distribution.
#
# Contributors:
#    Peter Siebler - initial implementation
#
# Copyright (c) 2022 Peter Siebler
# All rights reserved.
# ------------------------------------------------------------------


from lib import logger
from conf import *
from lib.ha_discoveryitems import *

log = logger.Log(__name__, LOG_LEVEL)

if __name__ == "__main__":
    """simple testcase to create and publish ha mqtt discovery items"""
    for device in DEVICES:
        print(device["device"])
        hadis = haDiscoveryItems(devicename=device["device"], folder=device["source"])
        n  = hadis.publish()
        log.info("HA Discovery {} Items: {}".format(device["device"], n))


