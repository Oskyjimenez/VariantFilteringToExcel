#!/usr/bin/python3

class HeaderFilter:


    '''
        @input : nombre del campo del filtro1
        Busca el indice de la columna donde se encuentra el nombre del campo
        @output : indice del campo insertado
    '''
    def getIndexColumnsFilter1(self, columnName:str, header:list):
            if "Otherinfo" not in (header):
                return len(header)-1
            else:
                return header.index(columnName)
  
    '''
        @input : linea del fichero filtro1  y el nombre de la columna
        Crea un diccionario usando la información de la penúltima columna de filtro1 como clave y la última columna como valores.
        @output : diccionarios con la información de las últimas dos columnas
    '''
    def lastFieldOtherInfo(self, line:list, fieldName:str, otherInfoFields:dict):
        fieldOtherInfo = {}
        contFields=0
        while contFields < len(list(otherInfoFields.values())):
            
            fieldOtherInfo[list(otherInfoFields.values())[contFields]] = line[-1].split(":")[contFields]
            contFields += 1
        
        
        return fieldOtherInfo
 
    '''
        Busca los prefijos de las DB en los nombre de las columnas de filtro1 
        @output : 2 listas, una con el nombre de las columnas que tengan el prefijo de la DB y y sufijo all y otra que contenga los demás campos que contiene el prefijo de la DB
    '''
    def getDatabasesFields(self, prefixesDB, header):
        DB_all = []
        DB_others = [] 
        ExAC_Position = 5
        for prefixDB in prefixesDB:
            for field in header:
                if field.startswith(prefixDB) and field.endswith("all") or field.startswith(prefixDB) and field.endswith("ALL"):
                   DB_all.append(field)
                elif field.startswith(prefixDB):
                    #Change position fields to get the correct order in header
                    if prefixDB == "ExAC_":
                        DB_others.insert(ExAC_Position, field)
                        ExAC_Position += 1
                    else:
                        DB_others.append(field)
        
        return [DB_all, DB_others]     





