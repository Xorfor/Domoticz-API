#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess
from datetime import datetime

################################################################################
# Server                                                                       #
################################################################################
class Server:
    # Responses
    _return_ok = "OK"
    _return_error = "ERR"

    __type_command = "command"
    __type_devices = "devices"
    __type_hardware = "hardware"
    __type_create_virtual_sensor = "createvirtualsensor"
    __type_set_used = "setused"

    # History
    __type_lightlog = "lightlog"  # Switch
    __type_graph_sensor = "graph&sensor"  # Temperature

    # Param
    _param = "param={}"
    __param_light = "getlightswitches"
    _param_shutdown = "system_shutdown"
    _param_reboot = "system_reboot"
    _param_sun = "getSunRiseSet"
    _param_log = "addlogmessage"
    __param_notification = "sendnotification"

    __param_switch_light = "switchlight"
    __param_color_brightness = "setcolbrightnessvalue"
    __param_kelvin_level = "setkelvinlevel"

    # Scenes / Groups
    __type_scenes = "scenes"
    __type_add_scene = "addscene"
    __type_delete_scene = "deletescene"
    __type_scene_timers = "scenetimers"
    __param_switch_scene = "switchscene"
    __param_get_scene_devices = "getscenedevices"
    __param_add_scene_device = "addscenedevice"
    __param_delete_scene_device = "deletescenedevice"
    __param_add_scene_timer = "addscenetimer"

    __type_create_device = "createdevice"
    __param_update_device = "udevice"

    # User variables
    __param_get_user_variables = "getuservariables"

    # Room Plans
    __type_plans = "plans"
    __param_get_plan_devices = "getplandevices"

    # Device Timer Schedules
    __type_schedules = "schedules"
    __param_enable_timer = "enabletimer"
    __param_disable_timer = "disabletimer"
    __param_delete_timer = "deletetimer"
    __param_update_timer = "updatetimer"
    __param_add_timer = "addtimer"
    __param_clear_timers = "cleartimers"

    # Filters
    __filter_all = "all"  # Get all devices
    __filter_light = "light"  # Get all lights / switches
    __filter_weather = "weather"  # Get all weather devices
    __filter_temp = "temp"  # Get all temperature devices
    __filter_utility = "utility"  # Get all utility devices
    #
    __filter_device = "device"  #
    __filter_scene = "scene"
    __filter_thermostat = "thermostat"

    _url_command = "type=" + __type_command + "&"
    # _url_sunrise_set = _url_command + "param=" + _param_sun
    # _url_log_message = _url_command + "param=" + _param_log + "&message="

    def __init__(self, address="localhost", port="8080"):
        self._address = address
        self._port = port
        self._status = ""
        self._url = "http://" + self._address + ":" + self._port + "/json.htm?"
        # No need to initialize all time properties. Next procedure will do that.
        self._getSunRiseSet()

    def __str__(self):
        txt = "{0}(\"{1}\", \"{2}\")".format(self.__class__.__name__, self._address, self._port)
        return txt

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def AstrTwilightEnd(self):
        self._getSunRiseSet()
        return self._AstrTwilightEnd

    @property
    def AstrTwilightStart(self):
        self._getSunRiseSet()
        return self._AstrTwilightStart

    @property
    def CivTwilightEnd(self):
        self._getSunRiseSet()
        return self._CivTwilightEnd

    @property
    def CivTwilightStart(self):
        self._getSunRiseSet()
        return self._CivTwilightStart

    @property
    def NautTwilightEnd(self):
        self._getSunRiseSet()
        return self._NautTwilightEnd

    @property
    def NautTwilightStart(self):
        self._getSunRiseSet()
        return self._NautTwilightStart

    @property
    def Sunrise(self):
        self._getSunRiseSet()
        return self._Sunrise

    @property
    def Sunset(self):
        self._getSunRiseSet()
        return self._Sunset

    @property
    def SunAtSouth(self):
        self._getSunRiseSet()
        return self._SunAtSouth

    @property
    def DayLength(self):
        self._getSunRiseSet()
        return self._DayLength

    @property
    def ServerTime(self):
        self._getSunRiseSet()
        return self._ServerTime

    @property
    def Status(self):
        return self._status

    # ..........................................................................
    # Global methods
    # ..........................................................................
    def logmessage(self, text):
        message = self._param.format(self._param_log) + "&message={}".format(text)
        res = self._call_command(message)
        self._status = res["status"]

    def reboot(self):
        message = self._param.format(self._param_reboot)
        res = self._call_command(message)

    def shutdown(self):
        message = self._param.format(self._param_shutdown)
        res = self._call_command(message)

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _getSunRiseSet(self):
        message = self._param.format(self._param_sun)
        res = self._call_command(message)
        # Used one line if ... then ... else for more compact code
        self._AstrTwilightEnd = res["AstrTwilightEnd"] if res.get("AstrTwilightEnd") else ""
        self._AstrTwilightStart = res["AstrTwilightStart"] if res.get("AstrTwilightStart") else ""
        self._CivTwilightEnd = res["CivTwilightEnd"] if res.get("CivTwilightEnd") else ""
        self._CivTwilightStart = res["CivTwilightStart"] if res.get("CivTwilightStart") else ""
        self._NautTwilightEnd = res["NautTwilightEnd"] if res.get("NautTwilightEnd") else ""
        self._NautTwilightStart = res["NautTwilightStart"] if res.get("NautTwilightStart") else ""
        self._Sunrise = res["Sunrise"] if res.get("Sunrise") else ""
        self._Sunset = res["Sunset"] if res.get("Sunset") else ""
        self._SunAtSouth = res["SunAtSouth"] if res.get("SunAtSouth") else ""
        self._DayLength = res["DayLength"] if res.get("DayLength") else ""
        self._ServerTime = res["ServerTime"] if res.get("ServerTime") else ""

    def _call_command(self, text):
        return self._call_api(self._url_command + text)

    def _call_api(self, text):
        return self.__call_url(self._url + str(text), "", "")

    # def __call_url(self, url, username, password):
    #     print("__call_url: "+ url)
    #     # request = urllib.request(url)
    #     # if len(username) != 0 and len(password) != 0:
    #     #	base64string = base64.encodestring("%s:%s" % (username, password)).replace("\n", "")
    #     #	request.add_header("Authorization", "Basic %s" % base64string)
    #     req = urllib.request.urlopen(url)
    #     #res = req.read()
    #     res = json.loads(req.read().decode("utf-8", "ignore"))
    #     return res

    def __call_url(self, url, username="", password=""):
        command = "curl -s "
        options = "'" + url + "'"
        p = subprocess.Popen(command + " " + options, shell=True, stdout=subprocess.PIPE)
        p.wait()
        data, errors = p.communicate()
        if p.returncode != 0:
            pass
        res = json.loads(data.decode("utf-8", "ignore"))
        return res
