from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

import zipfile as zf
from bs4 import BeautifulSoup
from typing import Iterator, List, Dict


def epub_iter(epub_file: str) -> Iterator[Dict]:
    """
    A python generator that iterates over the html files within an epub file.
    :param epub_file: Full path of the file
    :return: Iterator containing a dictionary of 'title' and body ('text') texts for each html within the epub
    """
    with zf.ZipFile(epub_file) as epub:
        for a_file in epub.namelist():
            if a_file.endswith('.html') or a_file.endswith('.htm'):
                with epub.open(a_file) as an_html:
                    text_seg = BeautifulSoup(an_html.read().decode(), 'lxml')
                    if text_seg.title:
                        yield {'title': text_seg.title.get_text(), 'text': text_seg.body.get_text()}
                    else:
                        yield {'title': "", 'text': text_seg.body.get_text()}


def read_epub(epub_file: str) -> List[Dict]:
    """
    Reads an entire epub file as a list of strings
    :param epub_file: Full path of the file
    :return: List of strings
    """
    full_text = []
    for a_text in epub_iter(epub_file):
        full_text.append(a_text)
    return full_text


def pdf_iter(pdf_file: str, accumulate_per_page: bool = True) -> Iterator[Dict]:
    """
    Extracts text blobs from a pdf file
    :param pdf_file: full path of the pdf file
    :param accumulate_per_page: if true, texts within a page are merged together
    :return: yields a dictionary containing the 'text' blobs as stipulated by accumulate_per_page
    """
    document = open(pdf_file, 'rb')
    # Create resource manager
    resource_manager = PDFResourceManager()
    # Set parameters for analysis
    layout_params = LAParams()
    # Create a PDF page aggregator object
    device = PDFPageAggregator(resource_manager, laparams=layout_params)
    interpreter = PDFPageInterpreter(resource_manager, device)
    for page in PDFPage.get_pages(document):
        texts_per_page = []
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                extracted_text = element.get_text()
                if accumulate_per_page:
                    texts_per_page.append(extracted_text)
                else:
                    yield {'text': extracted_text}
        if accumulate_per_page:
            yield {'text': "\n".join(texts_per_page)}
