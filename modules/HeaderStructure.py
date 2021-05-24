#!/usr/bin/python3

from modules.HeaderFilter import *

class HeaderStructure:

    header:list
    excelHeader:list
    columnsContent:list
    otherInfoFields:list
    prefixesDB:list

    def __init__(self,filterHeader:list, prefixesDB:list):
        self.header = filterHeader
        self.excelHeader = ["Sample", "IGV", "Gene", "Chr", "Start", "End", "Ref", "Alt", "Genome quality", "Total depth", "Depth > Q30", "Reference depth", "Alt depth", "FREQ", "Function", "Exonic consequence", "AA change & Transcript", "cosmic82", "avsnp144", "SIFT_pred_", "Polyphen2_HDIV_pred_", "Polyphen2_HVAR_pred_", "MutationAssessor_pred_", "SIFT_score", "SIFT_pred", "Polyphen2_HDIV_score", "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score", "Polyphen2_HVAR_pred", "LRT_score", "LRT_pred", "MutationTaster_score", "MutationTaster_pred", "MutationAssessor_score", "MutationAssessor_pred", "FATHMM_score", "FATHMM_pred", "PROVEAN_score", "PROVEAN_pred", "VEST3_score", "CADD_raw", "CADD_phred", "DANN_score", "fathmm-MKL_coding_score", "fathmm-MKL_coding_pred", "MetaSVM_score", "MetaSVM_pred", "MetaLR_score", "MetaLR_pred", "integrated_fitCons_score", "integrated_confidence_value", "GERP++_RS", "phyloP7way_vertebrate", "phyloP20way_mammalian", "phastCons7way_vertebrate", "phastCons20way_mammalian", "SiPhy_29way_logOdds", "Filtre VarScan2", "Transcript (si variant = splicing)", "Genome Type", "VCF", "p-value", "Average quality of reference-supporting bases", "Average quality of variant-supporting bases","Depth of reference-supporting bases on forward strand" ,"Depth of reference-supporting bases on reverse strand", "Depth of variant-supporting bases on forward strand", "Depth of variant-supporting bases on reverse strand"]
        self.renameFields = {"Gene" : "Gene.refGene", "Function" : "Func.refGene", "Exonic consequence" : "ExonicFunc.refGene", "AA change & Transcript" : "AAChange.refGene", "SIFT_pred_" : "SIFT_pred", "Polyphen2_HDIV_pred_" : "Polyphen2_HDIV_pred" ,"Polyphen2_HVAR_pred_" : "Polyphen2_HVAR_pred", "MutationAssessor_pred_" : "MutationAssessor_pred", "Filtre VarScan2" : "Otherinfo", "Transcript (si variant = splicing)" : "GeneDetail.refGene"}
        self.otherInfoFields = {"Genome Type" : "GT", "Genome quality" :"GQ", "Total depth" : "SDP", "Depth > Q30" : "DP", "Reference depth" : "RD","Alt depth" : "AD", "FREQ" : "FREQ", "p-value" : "PVAL","Average quality of reference-supporting bases" : "RBQ", "Average quality of variant-supporting bases" : "ABQ","Depth of reference-supporting bases on forward strand" : "RDF","Depth of reference-supporting bases on reverse strand" : "RDR","Depth of variant-supporting bases on forward strand" : "ADF","Depth of variant-supporting bases on reverse strand" : "ADR"}
        self.prefixesDB = prefixesDB

        self.clinvarField = self.getClinvarField()
        self.excelHeader.insert(self.excelHeader.index("MutationAssessor_pred_")+1, self.clinvarField)

        self.HeaderFilter = HeaderFilter()
       
        
        dbFields = self.HeaderFilter.getDatabasesFields(self.prefixesDB, self.header)
        self.addDBToHeader(dbFields[0], dbFields[1])

    def getClinvarField(self):
        for column in self.header:
            if column.startswith("clinvar_"):
                return column   

    '''
        @input : lista con los nombres de la DB con sufijo all y otra con los demás campos de la DB
        Inserta en la lista del header los campos de las DB en su posición correspondiente
        @output : header final completo
    '''
    def addDBToHeader(self, db_all:list, db_others:list):
        positionDB_all = self.excelHeader.index("avsnp144")+1

        for fieldsDB_all in db_all:
            self.excelHeader.insert(positionDB_all,fieldsDB_all)
            positionDB_all +=1

        positionDB_others = self.excelHeader.index(self.clinvarField)+1
        
        for fieldsDB_others in db_others:
            self.excelHeader.insert(positionDB_others,fieldsDB_others)
            positionDB_others += 1
    
 