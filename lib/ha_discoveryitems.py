#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, os.path, sys
import paho.mqtt.publish as publish
import yaml
import json

from lib import logger
from conf import *

# register the application logger
log = logger.Log(name=__name__, level=LOG_LEVEL)


class haDiscoveryItems():
    """ generate homeassistant mqtt discovery items"""

    def __init__(self, devicename: str = "hadevice", folder: str = 'devices'):
        """constructor haDiscoveryItems"""
        self.devicename = devicename
        self.source = folder

    def __loadYaml__(self, filename: str = "") -> dict:
        """simple load the yaml"""
        if filename:
            with open(filename, 'r', encoding='utf8') as f:
                try:
                    return yaml.safe_load(f)
                except yaml.YAMLError as exc:
                    print(exc)
                    return None

    def publish(self) -> int:
        """publish all ha discovery items for the gasmeter values based on the configuration settings"""
        try:
            file_items = "{}/discovery.yaml".format(self.source)
            file_payloads = "{}/schemalist.yaml".format(self.source)
            intCounter = 1
            # optional attributtes
            attr = ["ic", "device_class", "unit_of_meas", "state_class"]
            if os.path.isfile(file_items) and os.path.isfile(file_payloads):
                # valid setting found, open the file
                data = self.__loadYaml__(file_items)
                payloads = self.__loadYaml__(file_payloads)
                if data == None or payloads == None:
                    log.debug("{}: No data found for files {}, {}".format(sys._getframe().f_code.co_name, file_items, file_payloads))
                    return intCounter-1
                log.debug("{}: Loaded files {}, {}".format(sys._getframe().f_code.co_name, file_items, file_payloads))
                items = data["items"]
                for item in items:
                    if(int(item["enabled"] == 1)):
                        name = "{} {}".format(payloads["settings"]["name_prefix"], item["name"])
                        uniq_id = "{}-{}".format(payloads["settings"]["deviceid"], item["field"].replace("_", "."))
                        val_tpl = "{{{{value_json.{}}}}}".format(item["field"])
                        if "val_tpl" in item:
                            val_tpl = item["val_tpl"]
                        itemType = item["type"]
                        if "schema" in item:
                            payload = payloads[item["schema"]]
                            # update the fields
                            payload["name"] = name
                            payload["uniq_id"] = uniq_id
                            payload["val_tpl"] = val_tpl
                            for tag in attr:
                                if tag in item:
                                    payload[tag] = item[tag]
                                else:
                                    if tag in payload:
                                        del payload[tag]
                            topic_name = "{}".format(item["field"].replace(".", "_").lower())
                            log.debug("Publish Task {}, {}:{}".format(intCounter, itemType, name))
                            if payloads["settings"]["discovery_prefix"]:
                                # publish item
                                topic = "{}/{}/{}/{}/config".format(payloads["settings"]["discovery_prefix"], itemType, payloads["settings"]["section"], topic_name)
                                # mqtt brocker defined, send LWT Topic
                                if payloads["settings"]["mode"] == 'developer':
                                    log.debug("Publish discovery item:{}, {}".format(topic_name, topic))
                                publish.single(topic,
                                               payload=json.dumps(payload, ensure_ascii=False),
                                               qos=0, retain=True,
                                               hostname=payloads["settings"]["mqtt"]["hostname"],
                                               port=payloads["settings"]["mqtt"]["port"],
                                               client_id="hadis.{}.{}".format(payloads["settings"]["name_prefix"], os.uname().nodename),
                                               keepalive=60,
                                               auth=payloads["settings"]["mqtt"]["auth"])
                            if payloads["settings"]["mode"] == 'developer':
                                path = "{}ha/{}/{}".format(payloads["settings"]["datadir"], self.devicename, itemType)
                                if not os.path.exists(path): os.makedirs(path)
                                ha_file = "{}ha/{}/{}/{}-{}.json".format(payloads["settings"]["datadir"], self.devicename, itemType, intCounter, topic_name)
                                log.debug("Save ha-discovery item:{}".format(ha_file))
                                with open(ha_file, 'w', encoding='utf-8') as f:
                                    json.dump(payload, f, indent=4, ensure_ascii=False)

                            intCounter += 1

            return intCounter - 1

        except BaseException as e:
            log.error(f"Error {sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
            return False
