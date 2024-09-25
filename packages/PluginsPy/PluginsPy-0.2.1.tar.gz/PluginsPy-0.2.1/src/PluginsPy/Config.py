#!/usr/bin/env python3

import os
import json

class Config:

    def __init__(self):
        self.configPath = 'output/visualLogConfig.txt'
        self.keyValues = self.loadConfig()

    def loadConfig(self):
        if not os.path.exists("output"):
            os.mkdir("output")

        if os.path.exists(self.configPath):
            with open(self.configPath, 'r') as f:
                return json.load(f)
        else:
            return {}
    
    def saveConfig(self):
        if not os.path.exists("output"):
            os.mkdir("output")

        jsonStr = json.dumps(self.keyValues, indent=4)
        with open(self.configPath, 'w') as f:
            f.write(jsonStr)
 
    def setKeyValue(self, key, value):
        self.keyValues[key] = value

    def getValue(self, key):
        if key in self.keyValues.keys():
            return self.keyValues[key]
        else:
            return None

    def setKeyValues(self, keyValues: dict):
        saveConfig = dict(keyValues)
        for key in saveConfig:
            self.keyValues[key] = saveConfig[key]
 