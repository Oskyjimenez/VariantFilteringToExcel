#!/usr/bin/python3
import sys
import os
from modules.Parameters import *
from modules.Excel import *
from modules.File import *
from modules.Filter import *
from modules.HeaderFilter import *
from modules.SheetContent import *
from modules.HeaderStructure import *


if __name__ == '__main__':

	params = Parameters()

	if params.isNumberArgumenValid():
		if params.isExists():
			print('\033[92m' + "LOG: Arguments are correct\n" + '\033[0m')
		if params.orderParams():
			pass

	artifactsFile = params.isArtifactsExists()
	hotspotFile = params.isHotspotExist()

	prefixesDB = ["1000g2015aug_", "esp6500siv2_",  "ExAC_"]
	
	#Para mostrar en las hojas del excel algun/os campos concretos los añadimos a esta lista.
	#Ejemplo: ["Chr", "IGV", "Function"]
	specificFieldsToWriteIntoExcel = []

	newSheetWithSpecificFields={"_prr" : ["Chr", "IGV", "ExAC_ALL"]}

	fileFilter1 = File(params.args[1])
	filterFile = Filter(fileFilter1.HEADERORIGINAL, fileFilter1.readLines)

	#Filtra las lineas del fichero filtro1 para crear un diccionario con el nombre y el contenido de los ficheros
	filterFile.indexHeaderList  = fileFilter1.getColumnsIntoFilter(prefixesDB)
	contentFilterFiles = filterFile.getLinesToCreateFilterFiles(artifactsFile, hotspotFile)

	#Crea los ficheros con los diferentes filtros
	for file in list(contentFilterFiles.keys()):
		print('\033[93m' + "LOG: Generating file " + file  + '\033[0m')
		fileFilter1.createFile(file,contentFilterFiles[file], fileFilter1.HEADERORIGINAL)
		if not isfile(file):
			print('\033[91m' + "Error: File " + file + " was not created correctly" + '\033[0m')
			exit(1)
		print('\033[92m' + "LOG: File generated" + '\033[0m')

			
	
	#Genera una lista con el header completo del excel
	print('\033[93m' + "\nLOG: Generating excel header" + '\033[0m')
	headerStructure = HeaderStructure(fileFilter1.HEADER, prefixesDB)
	print('\033[92m' + "LOG: Excel structure created correctly" + '\033[0m')

	#Crea el fichero excel con el nombre de la muestra
	print('\033[93m' + "\nLOG: Creating excel file" + '\033[0m')
	workbook = xlsxwriter.Workbook(params.sampleName+'.xlsx')
	if not isfile(params.sampleName+'.xlsx'):
		print('\033[91m' + "Error: Excel file " + file + " was not created correctly" + '\033[0m')
	print('\033[92m' + "LOG: Excel file has been created correctly" + '\033[0m')

	outputExcel = Excel(workbook, params.sampleName, params.args, headerStructure.excelHeader)

	#Crea un diccionario con el contenido y lo escribe en el excel
	outputExcel.createStructureIntoExcel(specificFieldsToWriteIntoExcel, headerStructure.renameFields, headerStructure.otherInfoFields)	

	#Guarda y cierra el fichero excel
	outputExcel.save()
	
