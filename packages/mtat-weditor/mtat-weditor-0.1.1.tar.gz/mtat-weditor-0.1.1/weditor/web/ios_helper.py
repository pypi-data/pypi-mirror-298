import os
import subprocess
import time

from tidevice import Device
from logzero import logger


class IOSDeviceHelper:

    def __init__(self, udid):
        self._udid = udid
        self._tid = Device(udid)

    def get_version(self) -> str:
        try:
            return self._tid.get_value("ProductVersion")
        except:
            return ""

    def is_version_ge_17(self) -> bool:
        version = self.get_version()
        if version == "":
            return False
        big_version = int(version.split(".")[0])
        return big_version > 16

    def launch_wda_for_17(self):
        try:
            logger.info("ios init go-ios image: " + self._udid)
            process = self.__get_go_ios_process("image", "auto", "--basedir", os.path.expanduser("~/.devimages/"))
            self.__print_process_output(process)
            value = process.wait()
            if value != 0:
                logger.warning("ios init image error")
            time.sleep(1)
            logger.info("ios start wda by go-ios: " + self._udid)
            process = self.__get_go_ios_process("launch", "com.facebook.WebDriverAgentRunner.xctrunner")
            self.__print_process_output(process)
            value = process.wait()
            time.sleep(2)
            if value != 0:
                logger.warning("ios launch wda error")
        except Exception as e:
            logger.warning("ios launch wda by go-ios error:" + str(e))

    def __print_process_output(self, process):
        stdout_data, stderr_data = process.communicate()
        stdout_text = stdout_data.decode('utf-8')
        if stdout_text:
            logger.info(stdout_text.strip().replace("'", "\""))
        stderr_text = stderr_data.decode('utf-8')
        if stderr_text:
            logger.info(stderr_text.strip().replace("'", "\""))

    def __get_go_ios_process(self, *args):
        combine_args = ["/usr/local/bin/ios", "--udid", self._udid] + list(args) + ["--nojson"]
        process = subprocess.Popen(combine_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process

