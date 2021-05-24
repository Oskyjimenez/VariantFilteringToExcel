#!/usr/bin/python3

'''
Filtra los valores que se le pasan segun el nombre de la columna y el fichero para darle formato a los diferentes campos, y lo escribe en la hoja del excel correspondinte.
'''

class FilterField:

    fieldToFilter:str
    elementToFilter:str
    fileName:str
    freqField:str
    line:int
    column:int
    
    
    def __init__(self, field:str, elementField:str, worksheet, workbook, file:str, line:int, column:int, header:list, fullExcelHeader:list):
        self.elementToFilter = elementField
        self.worksheet = worksheet
        self.workbook = workbook
        self.fileName = file
        self.line = line
        self.column = column
        self.field = field

        
        if fullExcelHeader.index(field) >= fullExcelHeader.index("VEST3_score") and fullExcelHeader.index(field) <= fullExcelHeader.index("SiPhy_29way_logOdds") and field not in ["integrated_confidence_value", "MetaLR_pred", "MetaSVM_pred", "fathmm-MKL_coding_pred"]:
            self.modifyValueFields()
        elif self.field == "Depth of variant-supporting bases on reverse strand":
            self.modifyLastColumn()
        elif self.field == "p-value":
            self.pvalueField()
        elif self.field == "FREQ":
            self.fieldFreq()
        elif self.field == "cosmic82":
            self.cosmic82Field()
        elif self.field.startswith("ExAC_") or self.field.startswith("1000g2015aug_") and not self.field.endswith("_sas") or self.field == "esp6500siv2_all":
            self.exacField()
        elif self.field.startswith("SIFT_pred") or self.field.startswith("Polyphen2_HVAR_pred") or self.field.startswith("Polyphen2_HDIV_pred"):
            self.predField()
        elif self.field == "Depth > Q30":
            self.depthField()
        elif self.field == "Alt depth":
            self.altDepth()
        else:
            self.addField()
    
    def modifyValueFields(self):
        if self.elementToFilter == "NA" or self.elementToFilter == ".": 
            self.worksheet.write(self.line, self.column, self.elementToFilter)
        else:        
            if "." in self.elementToFilter:
                self.elementToFilter = (float(self.elementToFilter))
            else:
                self.elementToFilter = (float(self.elementToFilter) / 1000)
            self.worksheet.write(self.line, self.column, float(self.elementToFilter))
    
    def modifyLastColumn(self):
        self.worksheet.write(self.line, self.column, float(self.elementToFilter.strip("\n")))

    def pvalueField(self):
        if self.elementToFilter != "NA":
            self.elementToFilter = self.elementToFilter.replace(".",",")
        self.worksheet.write(self.line, self.column, self.elementToFilter)

    def fieldFreq(self):
        if self.elementToFilter != "NA":
            freqField = self.elementToFilter.replace("%","")
            
            if self.fileName == "filtro2.allInfo" or self.fileName == "filtro3.allInfo":
                if float(freqField) < 45 or float(freqField) <=95 and float(freqField) > 55:
            
                    self.worksheet.write(self.line, self.column, float(freqField), self.workbook.add_format({'bg_color': '#FF9999'}))
                else:
                    self.worksheet.write(self.line, self.column, float(freqField))
            else:
                self.worksheet.write(self.line, self.column, float(freqField))
        else:
                self.worksheet.write(self.line, self.column, self.elementToFilter)

    def cosmic82Field(self):
        if self.elementToFilter != "NA":
            if "haematopoietic" in self.elementToFilter:
                self.worksheet.write(self.line, self.column, self.elementToFilter, self.workbook.add_format({'bg_color': '#82FA58'}))
            else:
                self.worksheet.write(self.line, self.column, self.elementToFilter)
        else:
            self.worksheet.write(self.line, self.column, self.elementToFilter)

    def exacField(self):

        if self.elementToFilter != "NA" and self.elementToFilter != ".":
            if "," in self.elementToFilter:
                self.elementToFilter = self.elementToFilter.replace(",", ".")
            if self.fileName == "filtro2.allInfo" or self.fileName == "filtro3.allInfo" and float(self.elementToFilter) > 0.01:
                self.worksheet.write(self.line, self.column, float(self.elementToFilter), self.workbook.add_format({'bg_color': '#FF9999'}))
            else:
                self.worksheet.write(self.line, self.column, float(self.elementToFilter))
        else:
            self.worksheet.write(self.line, self.column, self.elementToFilter)

    def predField(self):
       
        if self.elementToFilter == "D" or self.elementToFilter == "P":
            if self.fileName == "filtro2.allInfo" or self.fileName == "filtro3.allInfo" or self.fileName == "filtro4.allInfo" or self.fileName == "filtro5.allInfo":
                self.worksheet.write(self.line, self.column, self.elementToFilter, self.workbook.add_format({'bg_color': '#FFD9B3'}))
            else:
                self.worksheet.write(self.line, self.column, self.elementToFilter)
        else:
            self.worksheet.write(self.line, self.column, self.elementToFilter)

    def depthField(self):
        if self.fileName == "filtro5.allInfo" or self.fileName == "filtro4.allInfo":
            if float(self.elementToFilter) < 100:
                self.worksheet.write(self.line, self.column, float(self.elementToFilter), self.workbook.add_format({'bg_color': '#FFD9B3'}))
            else:
                self.worksheet.write(self.line, self.column, float(self.elementToFilter))
        else:
            self.worksheet.write(self.line, self.column, float(self.elementToFilter))

    def altDepth(self):
        if self.fileName == "filtro5.allInfo" or self.fileName == "filtro4.allInfo":
            if float(self.elementToFilter) < 25:
                self.worksheet.write(self.line, self.column, float(self.elementToFilter), self.workbook.add_format({'bg_color': '#FFD9B3'}))
            else:
                self.worksheet.write(self.line, self.column, float(self.elementToFilter))
        else:
            self.worksheet.write(self.line, self.column, float(self.elementToFilter))

    def addField(self):
        if self.elementToFilter.isdigit():
            self.worksheet.write(self.line, self.column, float(self.elementToFilter))
        else:
            self.worksheet.write(self.line, self.column, self.elementToFilter)


        
            

