#!/usr/bin/python3
from modules.Hotspot import *
from modules.Artifacts import *
from modules.VAF import *
from os import path

'''
    Filtra las linea del fichero filtro1.allinfo para crear los diferentes ficheros con las lineas que les corresponden. 
'''

class Filter:

    header:str
    content:list
    filterFiles:list
    indexHeaderList:list

    def __init__(self,header:str,content:list):
        self.header = header
        self.excelHeader = header.split('\t')
        self.excelHeader[-1] = self.excelHeader[-1].strip("\n")
        self.content = content
        self.filterFiles = {}

    '''
        @input : Introduce la lista de posiciones de la base de datos
        Con la lista de posiciones de la base de datos, extraemos los que pasan el filtro VAF. 
        @output: Lineas que pasan el filtro
    '''
    def getLinesToCreateFilterFiles(self,filenameArtifacts:str = "artifactsFile" ,filenameHotspot:str = "hotspotFile"):
        
        addtoFilterFile = []
        hotspotFile = []
        artifactsFile = []
        filter4File = []
        contentOfFilterFiles  = {"filtro5.allInfo" : hotspotFile, "filtro4.allInfo" : filter4File, "filtro3.allInfo" : addtoFilterFile, "filtro2.allInfo" : artifactsFile}

        for filter1Line in self.content:
            columns = filter1Line.split("\t")
            
            #Si existe el fichero hotspot filtra su contenido para añadirlo a filtro5
            if path.exists(filenameHotspot):
                hotspot = Hotspot(filenameHotspot)
                if hotspot.compareLinesWithHotspot(columns):
                    contentOfFilterFiles["filtro5.allInfo"].append(filter1Line)
                    continue

            #Si existe el fichero Artifacts filtra su contenido para añadirlo a filtro2
            if path.exists(filenameArtifacts):
                artifacts = Artifacts(filenameArtifacts)
                if artifacts.compareLinesWithArtifacts(columns):
                    contentOfFilterFiles["filtro2.allInfo"].append(filter1Line)
                    continue
            
            #Filtra los campos de las bases de datos y si cumplen la condición añade la linea al contenido de filtro3
            for fieldPosition in self.indexHeaderList:
                appendToFilter3 = False
                if columns[fieldPosition] == "NA": columns[fieldPosition] = 0

                try:
                    if float(columns[fieldPosition]) > 0.01:
                        appendToFilter3 = True
                        break
                except ValueError:
                    pass
            
            if appendToFilter3:
                contentOfFilterFiles["filtro3.allInfo"].append(filter1Line)
                continue
            
            #Filtra los valores de los campos FREQ y reference depth, y en función de los requisitos que cumpla lo añade al filtro 4, al filtro5, o en ambos
            vaf = VAF(self.excelHeader, columns)
            if vaf.isFrequencingVafMin():
                contentOfFilterFiles["filtro5.allInfo"].append(filter1Line)
                continue
            if vaf.isFrequencingVafMax():
                contentOfFilterFiles["filtro4.allInfo"].append(filter1Line)
                continue
                
        return contentOfFilterFiles

  
            
                

        







