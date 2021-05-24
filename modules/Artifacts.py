#!/usr/bin/python3

class Artifacts:

    filename:str
    returnlistArtifacts:list

    def __init__(self, filename:str):
        self.filename = filename
        self.returnlistArtifacts = []

    #Lee el fichero artifacts y compara alguno campos concretos de cada línea con algunos campos de la linea que recibe el metodo 
    def compareLinesWithArtifacts(self, filterColumn):
        with open(self.filename, "r") as content:
            for line in content:
                return self.isValidArtifacts(filterColumn,line.split("\t"))
    
    def isValidArtifacts(self, filterColumn, artefactosLine):
        if artefactosLine[0] == filterColumn[6] and artefactosLine[1] == filterColumn[0] and artefactosLine[2] == filterColumn[1] and artefactosLine[3].strip() == filterColumn[2]:
            return True
        return False

