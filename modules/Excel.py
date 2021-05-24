#!/usr/bin/python3

import sys
import os
import xlsxwriter
from modules.File import *
from modules.FilterField import *
from modules.SheetContent import *
from modules.Filter import *

'''
    Alberga los diferentes métodos para crear y modificar el fichero excel
'''

class Excel:

    sampleName:str
    content:dict
    header:list
    filterFilesAndSufixesForNameSheet:dict


    def __init__(self, workbook, sampleName:str, parameterFiles:list, excelHeader:list):
        self.workbook = workbook
        self.sampleName = sampleName
        self.parameterFiles = parameterFiles
        self.excelHeader = excelHeader
        
    
    def createStructureIntoExcel(self, fieldsToWrite:list, renameFields:dict, otherInfoFields:dict):
        filterFilesAndSufixesForNameSheet={"empty1"  : "_Report", "empty2" : "_Filter","filtro5.allInfo" : "_CAND", "filtro4.allInfo" : "_REV", "filtro3.allInfo" : "_SNP", "filtro2.allInfo" : "_Artef"}
        filterFilesAndSufixesForNameSheet[self.parameterFiles[1]] = "_conseq"
        filterFilesAndSufixesForNameSheet[self.parameterFiles[0]] = "_vcf"

        for file in list(filterFilesAndSufixesForNameSheet.keys()):
            
            #Crea las dos hojas vacias en el excel
            if not os.path.isfile(file):
                self.ifnotExistsFile(file, filterFilesAndSufixesForNameSheet)
                continue
                
            self.preparingContentToWrite(file, filterFilesAndSufixesForNameSheet, fieldsToWrite, renameFields, otherInfoFields)
              
    
    def preparingContentToWrite(self, file:str, filterFilesAndSufixesForNameSheet:dict, fieldsToWrite:list, renameFields:list, otherInfoFields:dict):
        fileFilter = File(file)
        print('\033[93m' + "\nLOG: Generating content of " + self.sampleName + filterFilesAndSufixesForNameSheet[file]  + '\033[0m')
        sheetContent = SheetContent(fileFilter.readLines, self.excelHeader, fileFilter.HEADER ,self.sampleName, renameFields, otherInfoFields)
        #Si la lista fieldsToWrite esta vacia escribe todos los campos en el excel, sino escribe solo los que le pida el usuario
        if len(fieldsToWrite) == 0:	
            self.writeIntoExcel(file, filterFilesAndSufixesForNameSheet[file], sheetContent.excelContent, sheetContent.excelHeader)
            print('\033[92m' + "LOG: Content added into spreedsheet" + '\033[0m')
        else:
            columnsContent = self.checkAndWriteSpecificFields(fieldsToWrite, sheetContent.excelHeader, sheetContent.excelContent)
            self.writeIntoExcel(file, filterFilesAndSufixesForNameSheet[file], columnsContent, fieldsToWrite)

    def ifnotExistsFile(self, file, filterFilesAndSufixesForNameSheet:dict):
        worksheet = self.createSheet(filterFilesAndSufixesForNameSheet[file])
        if filterFilesAndSufixesForNameSheet[file] != "_Filter" and filterFilesAndSufixesForNameSheet[file] != "_Report":
            worksheet.set_tab_color('red')
        self.writeHeader(worksheet, self.excelHeader)

    def checkAndWriteSpecificFields(self, fieldsToWrite:list, excelHeader, excelContent):
        columnsContent = {}
        for column in fieldsToWrite:
            if column not in excelHeader:
                print('\033[91m' + "LOG: La columna " + column + " no se encuentra en el fichero" + '\033[0m')
            else:
                columnsContent[column] = excelContent[column]
        
        return columnsContent
                 
    '''
        @input : sufijo de la hoja de del excel
        Crea una hoja en el excel con el nombre de la nombre y el sufijo que se le pasa
        @output : nueva hoja del excel
    '''
    def createSheet(self, sufixSheet:str):       
        worksheet= self.workbook.add_worksheet(self.sampleName + sufixSheet)
        print('\033[92m' + "LOG: " + self.sampleName + sufixSheet + " created" + '\033[0m')
        return worksheet

    '''
        @input : nombre del fichero donde recoge la información, el sufijo de la hoja del excel, el contenido del fichero y el header del excel
        Recorre las listas con la información de las direntes columnas y envía el contenido de cada campos a la clase FilterField para filtrarlo
    '''
    def writeIntoExcel(self, file:str, sufixSheet:str, content:dict, header:list):
        worksheet = self.createSheet(sufixSheet)
        worksheet.set_tab_color('red')
        if sufixSheet == "_CAND":
            worksheet.activate()
        
        print('\033[93m' + "LOG: Writting header" + '\033[0m')
        self.writeHeader(worksheet, header)

        print('\033[93m' + "LOG: Writting into " + self.sampleName + sufixSheet + '\033[0m')
        column=0
        for field in header:
            line = 1
            for fieldColumn in content[field]:
                if field != "Sample":
                    worksheet.write(line, 0, self.sampleName)
                    FilterField(field, fieldColumn, worksheet, self.workbook, file, line, column, header, self.excelHeader) 
                line += 1
            column += 1
    
    '''
        @input :  variable con la hoja del excel y el header del excel final
        Escribe en la hoja el header final con su respectivo formato
    '''
    def writeHeader(self, worksheetName, header):
        column = 0
        for field in header:
            worksheetName.write(0, column, field, self.workbook.add_format({'bold': True, 'align': 'center', 'border': 1, 'bg_color':  '#B3E6FF'}))
            column += 1      

    def save(self):
        print('\033[94m'+"\nLOG: Excel file generated correctly" + '\033[0m' + "\n")
        self.workbook.close()

    
        
            





       