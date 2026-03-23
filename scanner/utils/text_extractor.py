import pdfplumber
import docx
import os
import nltk


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


def extract_text_from_docx(file_path):

    document = docx.Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text_from_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text



def split_into_sentences(text):

    sentences = nltk.sent_tokenize(text)

    return sentences



def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        return "Unsupported file format"