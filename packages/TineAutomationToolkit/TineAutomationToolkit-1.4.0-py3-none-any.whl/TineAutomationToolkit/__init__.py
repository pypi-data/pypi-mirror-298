# -*- coding: utf-8 -*-
from TineAutomationToolkit.keywords import *

class TineAutomationToolkit(
    ToolkitsTest,
    WaitingElement,
    ConnectionManagement,
    ControlElement,
    Scroll,
    CaptureScreenShot,
    KeyEvent,
    Touch,
    ConvertObject,
    ImageProcessing,
    Mongodbcrud
    ):

    def __init__(self):
        self._screenshot_indexs = 0     #index capture appium (Native)
        self._status_mode = 'FLUTTER'
        #Mongodb
        self._dbconnection = None


    def main(self):
        print("This Main นี้คือ เมน")