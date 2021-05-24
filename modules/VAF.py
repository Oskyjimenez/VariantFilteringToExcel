#!/usr/bin/python3

class VAF:

    header:list
    positionFrequencing:int
    frequencyField:int
    fileFilter5:list
    fileFilter4:list
    columns:list


    def __init__(self,header:list,columns:list):
        self.header = header
        if "Otherinfo" in header:
            self.positionFrequencing = header.index("Otherinfo")+3
        else:
            self.positionFrequencing = len(header)+2
        self.columns = columns
        self.getValueFrequencing()
        self.getValueReferenceDepth()
        self.fileFilter4 = []
        self.fileFilter5 = []

    '''
        Consigue el valor de la frecuencia del ultimo campo de cada linea
    '''
    def getValueFrequencing(self):
        self.frequencyField = float(self.columns[self.positionFrequencing].split(":")[6].replace(",",".")[0:-1])
        return self.frequencyField

    '''
        Consigue el valor reference depth del ultimo campo de cada linea
    '''
    def getValueReferenceDepth(self):
        self.adp = float(self.columns[self.positionFrequencing].split(":")[5])
        return self.adp
    
    '''
        Comprueba si la frecuencia y la reference depth cumplen los requisios en funcion de los valores vafMin(0.1), vafMax(5) y depthMax(20) 
    '''
    def isFrequencingVafMax(self):
        if self.frequencyField > 5 and self.adp <= 20 or self.frequencyField < 5 and self.frequencyField >= 0.1:
            return True

    '''
        Comprueba si la frecuencia y la reference depth cumplen los requisios en funcion de los valores vafMax(5) y depthMax(20)
    '''
    def isFrequencingVafMin(self):
        if  self.frequencyField > 5 and self.adp > 20:
            return True

