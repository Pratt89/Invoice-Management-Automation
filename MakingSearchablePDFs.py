# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:23:28 2020

@author: PraTiK ChavhaN aLias </steve_Rogers>
"""
# Import the base64 encoding library.
import base64
# from os import name
# importing the module 
# import img2pdf
from PIL import Image 
import os 
import json
import shutil
import subprocess

class MakingSearchablePDFs:
    def __init__(self):
        pass
        # self.filename = filename
    
    # encode image data to base64 type.
    def encode_image(image):
        b64_string = None
        source = 'input/searchable_pdfs/'
        with open(source + image, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        # image_content = image.read()
        # return base64.b64encode(image_content)
        print(type(b64_string))
        b64_string = str(b64_string)
        with open(source + 'b64_string.txt', 'w') as file:
            file.write(b64_string)
    
    # standardize image to jpg format
    def convert_to_jpg(image):
        # importing the image  
        source = 'input/searchable_pdfs/'
        im = Image.open(source + image) 
        print("The size of the image before conversion : ", end = "") 
        print(os.path.getsize(source + image)) 
    
        # converting to jpg 
        rgb_im = im.convert("RGB") 
        image = image.split('.')
        image = image[:-1]
        image = '.'.join(image)
        
        # exporting the image 
        rgb_im.save(source + image+".jpg") 
        print("The size of the image after conversion : ", end = "") 
        print(os.path.getsize(source + image+".jpg"))
        return image+'.jpg'
    
    # converting normal images to searchable pdfs
    def convert_image_to_searchable_pdf(image):
        # Make Searchable pdf from image to feed yaml template system
        # image='sample3.jpeg'
        source = 'input/uploads/'
        destination = 'input/searchable_pdfs/'
        shutil.move(source + image, destination + image)
        type_of_image = image.split('.')[-1]
        
        # convert any image type to 'jpg' format
        if type_of_image!='jpg': image = MakingSearchablePDFs.convert_to_jpg(image)
        name_of_image = image.split('.')[:-1]
        name_of_image = '.'.join(name_of_image)
        # image='denoised_img.jpg'
        
        # encode image data to base64 type
        MakingSearchablePDFs.encode_image(image)
        with open(destination + 'b64_string.txt', 'r') as file:
            b64_encoded_string = file.read()
        print(type(b64_encoded_string), b64_encoded_string[:2], b64_encoded_string[-1:])
        b64_encoded_string = b64_encoded_string[2:-1]
        # with open('request.json') as file:
        #   data = json.load(file)
        
        # request body for GCV
        data = {
        "requests": [
            {
            "image": {
                "content": b64_encoded_string
            },
            "features": [
                {
                "type": "TEXT_DETECTION"
                }
            ]
            }
        ]
        }
        json_data = json.dumps(data)
        print(type(data), type(json_data))
        with open('request.json', 'w') as file:
            file.write(json_data)
    
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service-account-file.json"
        # Send request to GCV url.
        process=subprocess.Popen(["powershell.exe","./SendingRequest_GCV.ps1"],stdout=subprocess.PIPE);
        result=process.communicate()[0]
        # (out, err) = proc.communicate()
        print (type(result))
        # convert gcv response bytes to string 
        ans = result.decode('utf-8')    
        # json_data = json.dumps(data)
        # write gcv response to json file 
        with open(destination+name_of_image+'_GCVjson.json', 'w') as file:
          file.write(ans)
    
        # convert json response to hocr 
        os.system('python gcv2hocr-master/gcv2hocr.py '+destination+name_of_image+'_GCVjson.json > '+destination+name_of_image+'_hocr.hocr')
        # convert hocr to searchable pdf
        # os.system('python hocr-pdf.py . --savefile '+name_of_image+'.pdf')
        os.system('python hocr-pdf.py --savefile '+destination+name_of_image+'_pdf.pdf '+destination)
    
        
        image = name_of_image+'_pdf.pdf'
        # move pdf from root dir to input/uploads
        shutil.move(destination+image, source + image)
        # shutil.move(destination + image, source + image)
        # return pdf name
        return image        