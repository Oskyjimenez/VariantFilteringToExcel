#!/usr/bin/python3
import os
import sys
from os.path import isfile
from modules.File import *
from modules.Filter import *
import argparse

class Parameters:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("filtro0", type=str, help="filter0.allInfo File")
        self.parser.add_argument("filtro1", type=str, help="filter1.allInfo File")
        self.parser.add_argument("-a", "--artifacts", type=str, help="Artifacts File", default="NONE")
        self.parser.add_argument("-ht", "--hotspot", type=str, help="Hotspot File", default="NONE")
        self.parser.add_argument("Samplename", type=str, help="Samplename")

        self.arguments = vars(self.parser.parse_args())

        #Convert Namespace to List
        self.args = list(self.arguments.values())
        self.sampleName = self.args.pop(-1)

    '''
        @input : lista con los parametros
        Valida si se han añadido los parametros bien y comprueba si existen los diferentes ficheros
    '''
    def isNumberArgumenValid(self):
        if len(self.args) < 2 and len(self.args) <= 6:
            raise Exception("Arguments are necesary filtro0.allinfo filtro1.allinfo {-a artifacts.txt} {-ht hotspot.txt} sample_name")
        else:
            return True

    '''
        Comprueba si existen los ficheros que se pasan por parametros
    '''
    def isExists(self):
        for i in self.args:
            if not isfile(i):
                if i == "NONE": continue
                raise Exception('\033[91m' + "Error: File " + i + " not found" + '\033[0m')
                exit(1)

        return True

    def orderParams(self):
        if "filtro0.allInfo" in self.args[0] and "filtro1.allInfo" in self.args[1]:
            return True
        elif "filtro1.allInfo" in self.args[0] and "filtro0.allInfo" in self.args[1]:
            self.args[0] = self.arguments["filtro1"]
            self.args[1] = self.arguments["filtro0"] 
            return True
       
        return False

    '''
        Comprueba si existe el parametro -ht hotspot
    '''
    def isHotspotExist(self):
        hotspotFile = ""
        if self.arguments["hotspot"]:
            hotspotFile = self.arguments["hotspot"]
            return hotspotFile

        return hotspotFile

    '''
        Comprueba si existe el parametros -a o artifacts
    '''
    def isArtifactsExists(self):
        artifactsFile = ""
        if self.arguments["artifacts"]:
            hotspotFile = self.arguments["artifacts"]
            return hotspotFile

        return artifactsFile









