#!/usr/bin/python3

from modules.HeaderFilter import *

class SheetContent:
    header:list
    excelHeader:list
    sample:str
    excelContent:dict
    columnsContent:list
    filterFileContent:list
    otherInfoFields:list
    renameFields:dict



    '''
        Agrega al diccionario excelContent los nombres de los campos y una lista con la información de cada columna
        @output : diccionario con el contenido del la hoja VCF
    '''
    def __init__(self, filterFileContent:list, excelHeader:list, filterHeader:list, sampleName:list, renameColumns:dict, otherInfoColumn:dict):

        self.header = filterHeader
        self.header[-1] = self.header[-1].strip("\n")
        self.excelHeader = excelHeader
        self.sample = sampleName
        self.excelContent = {"Sample": ""}
        self.filterFileContent = filterFileContent
        self.renameFields = renameColumns
        self.otherInfoFields = otherInfoColumn
        self.HeaderFilter = HeaderFilter()
        
        for field in self.excelHeader:
    
            if field == "Sample":
                continue
            self.columnsContent = []

            for line in self.filterFileContent:
                contentLine = line.split("\t")
                if field not in self.header:
                    self.fieldsNotInHeader(field, contentLine)
                else:
                    self.columnsContent.append(contentLine[self.HeaderFilter.getIndexColumnsFilter1(field, self.header)])                
            
            self.excelContent[field] = self.columnsContent

    '''
        @output : valores de los campos chr y start
        Genera el contenido de la columa IGV
        @output devuelve el valor del campo IGV 
    '''
    def columnIGV(self, chrField:str, startField:int):
        return "http://localhost:60151/goto?locus=" + chrField + ":" + startField
    
    '''
        @input : linea del filtro1
        @output : devuelve el valor de la antepenultima columna del filtro1
    '''
    def fieldVCF(self, line:list):
        return line[self.header.index("Otherinfo")+1]
        


    '''
        @input :  nombre del campo y una lista con el contenido de la linea de filtro1
        Busca los campos del excel definitivo en el header de filtro1 para añadir la información de la columna al diccionario columnsContent
        @output : diccionario con los nombres de las columnas como clave y un array con el contenido de la columna como valor

    '''
    def fieldsNotInHeader(self, field:str, contentLine:list):

        if field == "IGV":
            self.columnsContent.append(self.columnIGV(contentLine[0], contentLine[1]))
        
        elif field == "VCF":
            self.columnsContent.append(self.fieldVCF(contentLine))

        elif field in self.renameFields.keys():
            renameColumn = self.appendRenameFields(field, contentLine)
            self.columnsContent.append(contentLine[self.HeaderFilter.getIndexColumnsFilter1(renameColumn, self.header)])

        else:
            self.columnsContent.append(self.HeaderFilter.lastFieldOtherInfo(contentLine, field, self.otherInfoFields)[self.otherInfoFields[field]])

        return self.columnsContent
        
        
    '''
        @input : nombre del campo del excel final y contenido de la linea de filtro1
        @output : nombre de la columna del filtro1
    '''
    def appendRenameFields(self, renameField:str, contentLine:list):
        return self.renameFields[renameField]
    