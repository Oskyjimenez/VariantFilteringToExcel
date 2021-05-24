#!/usr/bin/python3

'''
    Filtra las lineas del filtro1.allinfo para añadir las que correspondan al fichero filtro5.allinfo
'''

class Hotspot:
    filename:str
    rowLine:list
    RETURNFILE:list

    def __init__(self,filename):
        self.filename = filename
        self.RETURNFILE = []

    #Lee el fichero hotspot y compara alguno campos concretos de cada línea con algunos campos de la linea que recibe el metodo 
    def compareLinesWithHotspot(self,columnFilter:list):
        
        with open(self.filename,"r") as content:
            for line in content:
                return self.isValidHotspot(line.split("\t"),columnFilter)
                    
    def isValidHotspot(self,columnHotspot:list,columnFilter:list):

        if columnHotspot[0] == columnFilter[6] and columnHotspot[1] == columnFilter[0] and columnHotspot[2] == columnFilter[1] and columnHotspot[3].strip() == columnFilter[2] and columnHotspot[4].strip() == columnFilter[9]:
            
            return True
        
        return False


