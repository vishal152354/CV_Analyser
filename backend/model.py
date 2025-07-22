from pathlib import Path
import os
import io
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import re 
import csv
import shutil
import datetime

class Applicant :
    def __init__(self,name,mobile,email):
        self.name = name
        self.mobile = mobile
        self.email = email
    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Phone: {self.mobile}"

def check_folder(folder_path):
    folder = Path(folder_path)

    if folder.is_dir():
        return next(folder.iterdir())
    else :
        return False

def number_of_files(folder_path):
    count = 0 
    try:
        for folder_path, _, files in os.walk(folder_path):
            count += len(files)
    except FileNotFoundError:
        print("file not found")
    except Exception as e :
        print("error",e)
    return count

def find_paths_files(folder_path,recursive = False):
    file_paths = []
    folder = Path(folder_path)
    for item in folder.rglob('*'):
        if item.is_file():
            file_paths.append(item)
    return file_paths

def extract_text_from_single_pdf(pdf_file_path):
    pdf_path = Path(pdf_file_path)

    if not pdf_path.is_file():
        print(f"Error: PDF file not found at path: '{pdf_path}'. Skipping extraction.")
        return []

    laparams = LAParams(
        char_margin=2.0,
        line_margin=0.5,
        word_margin=0.1,
        boxes_flow=0.5,
        detect_vertical=True
    )

    rsrcmgr = PDFResourceManager()
    
    extracted_pages_text = []

    try:
        with open(pdf_path, 'rb') as fp:
            for page_num, page in enumerate(PDFPage.get_pages(fp)):
                output_string = io.StringIO()
                device = TextConverter(rsrcmgr, output_string, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                
                interpreter.process_page(page)
                page_text = output_string.getvalue()
                extracted_pages_text.append(page_text)
                
                device.close()
                output_string.close()
                
        return extracted_pages_text
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during PDF extraction for '{pdf_path}': {e}")
        return []

def extract_text(list_of_pdf_paths):
    all_pdfs_pages_content = []

    if not list_of_pdf_paths:
        print("No PDF paths provided. Returning empty list.")
        return []

    for i, pdf_path in enumerate(list_of_pdf_paths):
        print(f"Processing PDF {i+1}/{len(list_of_pdf_paths)}: {pdf_path}")
        extracted_content_for_one_pdf = extract_text_from_single_pdf(pdf_path)
        all_pdfs_pages_content.append(extracted_content_for_one_pdf)

    return all_pdfs_pages_content

def get_email(documents):
    emails = []
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    for resume_text in documents:
        lines = resume_text.split('\n')
        for line in lines:
            found_emails = email_pattern.findall(line)
            for email in found_emails:
                emails.append(email)

    return emails

def get_mobile(documents):
 
    mobile = []
    
    mobile_pattern = re.compile(r'(?:\(?\d{3}\)?[\s.-]*\d{3}[\s.-]*\d{3,4}|\+?\d{1,3}[\s.-]*\d{7,14})')
    
    for resume_text in documents:
        found_mobiles = mobile_pattern.findall(resume_text) 
        for num in found_mobiles:
            
            
            clean_num = re.sub(r'[\s().-]', '', num)
            
            
            if 7 <= len(clean_num) <= 15:
                if num.startswith('+') and not clean_num.startswith('+'):
                    clean_num = '+' + clean_num
                mobile.append(clean_num)

    return mobile

import re

def get_name(documents):
    name_lst = []
    name_pattern = re.compile(r'\b[A-Z][a-z\'-]+\s(?:[A-Z][a-z\'-]*\s)?[A-Z][a-z\'-]+\b')
    name_with_initial_pattern = re.compile(r'\b[A-Z][a-z\'-]+\s(?:[A-Z]\.\s)?[A-Z][a-z\'-]+\b')

    for doc_content in documents:
        lines = doc_content.split('\n')
        found_name = "Unknown" 

        for i in range(min(len(lines), 5)): 
            line = lines[i].strip()
            
            if not (5 <= len(line) <= 50) or any(char.isdigit() for char in line):
                continue

            match = name_pattern.search(line)
            if match:
                found_name = match.group(0)
                break 
            
            match_initial = name_with_initial_pattern.search(line)
            if match_initial:
                found_name = match_initial.group(0)
                break
        
        name_lst.append(found_name)
    return name_lst
def get_file():
    af = int(input("how many files do you want to add :"))
    if af == 0:
        print("done!")
    else:
        folder_path = r""
        for i in range(af):
            src_path = input("enter the file path of pdf: ")
            abs_path = src_path       
            try:
                shutil.copy(abs_path, folder_path)
                print(f"Successfully copied: {abs_path} to {folder_path}")
            except FileNotFoundError:
                print(f"Error: File not found at '{abs_path}'. Please check the path.")
            except Exception as e:
                print(f"An unexpected error occurred while copying '{abs_path}': {e}")


