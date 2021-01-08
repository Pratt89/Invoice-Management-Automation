# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:16:34 2020

@author: PraTiK ChavhaN aLias </steve_Rogers>
"""
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
import json
from MakingSearchablePDFs import MakingSearchablePDFs

def extract_invoice_details(filename):
    if filename!='':
        filename_splitted = filename.split('.')
        # 1.Case for images
        if filename_splitted[-1]!='pdf':
            # makingSearchablePDF = MakingSearchablePDFs()
            filename = MakingSearchablePDFs.convert_image_to_searchable_pdf(filename)
            # filename = convert_image_to_searchable_pdf(filename)
        # 2.Case for pdfs
        elif filename_splitted[-1]=='pdf':
            pass

        # YAML Template System
        source = 'input/uploads/'+filename
        templates = read_templates('Templates/')    
        result = extract_data(source, templates=templates)
        print('\n', type(result))
        print('\n',result)

        # from json import dumps
        # print(dumps(datetime.now(), default=json_serial))
        if result!=False:
            destination = 'output/processed/'+filename
            json_data = json.dumps(result, indent=4, sort_keys=True, default=str)
            print(type(json_data), json_data)
            # shutil.move(source, destination)
        else:
            destination = 'output/failed/'+filename
            print('Failed for Processing of Invoice!!!')

        # Move processed file to respective actioned folder.
        # shutil.move(source, destination)
        # json_data = json.dumps(result)
        # print('\n', type(json_data))
        with open(destination+name_of_image+'_json.json', 'w') as file:
          file.write(result)


# main program
# filename = 'sample2.pdf'
filename = 'hitesh.jpg'
# filename = 'sample3.pdf'
# filename = 'sample3.jpeg'
# filename = 'SwaraVyanjan2.pdf'
# filename = 'test.pdf'
extract_invoice_details(filename)