from datetime import datetime
import time
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import docx
import json
import boto3
from typing import Union

import pytesseract
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\augusto.lorencatto\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_pdf_to_text(file_path : str) -> Union[str,str]:

    with open(file_path, 'rb') as file:
        reader = PdfReader(file)

        file_name : str = file_path.split("/")[-1]

        conversion_process = "raw_pdf"
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

        if len(text) < 500:
            
            raise Exception("Can't extract text from .pdf with only images")

            # TODO : Implement
            # print("Converting all pages to images...")
            # conversion_process = "pdf_to_image"

            # #
            # poppler_path=r"T:\libs\poppler\Library\bin"

            # #
            # images = convert_from_path(file_path,poppler_path=poppler_path)

            # for i in range(len(images)):

            #     text_extracted = pytesseract.image_to_string(images[i])
            #     text += text_extracted

    return text,conversion_process


def extract_docx_to_text(file_path : str) -> str:
    doc = docx.Document(file_path)

    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)