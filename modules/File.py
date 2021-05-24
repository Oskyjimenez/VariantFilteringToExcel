#!/usr/bin/python3

import sys
import os
from os import path

class File:
    
    file:str
    readLines:list
    countReadLines:int
    HEADER : list
    HEADERORIGINAL:str
    
    '''
        Validar si existe el fichero y sacar los atributos anteriores
    '''
    def __init__(self,filepath:str):
        try:
            self.file = filepath
            with open(self.file, "r") as fi:
                self.readLines = fi.readlines() 
                self.countReadLines = len(fi.readlines()) 
                self.HEADERORIGINAL = self.readLines[0]
                self.HEADER = self.readLines[0].split("\t")
                self.otherinfoFieldNotInHeader()
                self.readLines.pop(0)


        except OSError:
            print('\033[91m' + "LOG: Not read file %s " % self.file + '\033[0m')

    ''' 
        @input : 
        Quitar un elemento de una lista y almacenarlo en una variable 
    '''
    def dropAndGetAnEspecificElement(self, listToDropAndExtractElement:list, position:int):
        extractedElement =  listToDropAndExtractElement.pop(position)
        return extractedElement
    
    '''
        @input : Lista con los prefijos de las base de datos
        Extraer la posicion de las columnas , que  pertenecen a una base de datos
        @output: Lista con las posiciones dentro del fichero 
    '''
    def getColumnsIntoFilter(self, prefixesDB:str):
        fieldPositionsHeader = []
        for prefixDB in prefixesDB:
            for column in self.HEADER:
                if column.startswith(prefixDB):
                    fieldPositionsHeader.append(self.HEADER.index(column))
        
        return fieldPositionsHeader       

    '''
        @input : Nombre del fichero y contenido
        Crea los ficheros de filtros, con el contenido que le pasamos 
        @output: Lineas que pasan el filtro
    '''
    def createFile(self, filename:str, content:list, header:str):
        try:
            with open(filename,"w") as file :
                # Write HEADER into File
                file.write(header)
                # Write content into File
                for line in content:
                    file.write(line)
        except OSError as error:
            print("The file  " + filename + " could not be created")
            print(error)

    '''
        Añade al header el campo otherinfo si no lo encuentra en el header del fichero filtro0.allinfo
    '''
    def otherinfoFieldNotInHeader(self):
        if "Otherinfo" not in self.HEADER:
            for column in self.HEADER:
                if column.startswith("SiPhy_29way_logOdds"):
                    positionSyPhy= self.HEADER.index(column)   
            self.HEADER[positionSyPhy] = self.HEADER[positionSyPhy].replace("\n", "")
            self.HEADER.insert(self.HEADER.index("SiPhy_29way_logOdds")+1, "Otherinfo")
  
