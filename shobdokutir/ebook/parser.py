import os
import sys
import json
import argparse
from typing import Iterator, List, Dict
import zipfile as zf

from bs4 import BeautifulSoup
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal


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


def epub_meta_to_json(epub_file):
    """
    Reads the content.opf file of an epub and produces a json blob with the following schema.
    The schema is designed to be stored as a bigquery table.

    ## Metadata Schema
    uuid, all_ids, title, creator, epub_filename, manifest, spine, content_str

    ## Manifest Schema
    [ [id, item, media_type], ... ]

    ## Spine Schema
    [idref, idref, ...]
    """
    def find_content_file(epub):
        content_file = [a_file for a_file in epub.namelist() if "content.opf" in a_file.lower()]
        if not content_file:
            raise Exception("content.opf file not found in epub")
        return content_file[0]

    def extract_meta(content, epub_file):
        epub_path, epub_filename = os.path.split(epub_file)
        output_blob = {'epub_filename': epub_filename, 'content_str': content}
        content_parsed = BeautifulSoup(content, "lxml")
        if content_parsed.metadata is None:
            output_blob['uuid'] = None
            output_blob['all_ids'] = None
            output_blob['title'] = None
            output_blob['creator'] = None
        else:
            uuid = content_parsed.find("dc:identifier", id="uuid_id")
            output_blob['uuid'] = uuid.text if uuid is not None else None
            output_blob['all_ids'] = [an_id.text for an_id in content_parsed.find_all("dc:identifier")]
            title = content_parsed.find("dc:title")
            output_blob['title'] = title.text if title is not None else None
            creator = content_parsed.find("dc:creator")
            output_blob['creator'] = creator.text if creator is not None else None

        if content_parsed.manifest is None:
            output_blob['manifest'] = None
        else:
            output_blob['manifest'] = [{'id':an_item['id'], 'item':an_item['href'], 'media_type':an_item['media-type']} 
                                                for an_item in content_parsed.manifest.find_all("item")]
        if content_parsed.spine is None:
            output_blob['spine'] = None
        else:
            output_blob['spine'] = [an_itemref['idref'] for an_itemref in content_parsed.spine.find_all('itemref')]

        return json.dumps(output_blob, ensure_ascii=False).encode("utf-8")

    with zf.ZipFile(epub_file) as epub:
        content_file = find_content_file(epub)
        with epub.open(content_file) as meta_file:
            meta_data = " ".join(meta_file.read().decode("utf-8").split('\n'))
            return extract_meta(meta_data, epub_file)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bangla Ebook Parser")
    parser.add_argument("--get_meta", action="store", default=None, type=str, nargs="+", help="Extracts the meta for a given epub. Please provide the full path of the epub file")
    args = parser.parse_args()

    if args.get_meta:
        filename = " ".join(args.get_meta)
        meta = epub_meta_to_json(filename).decode("utf-8")
        meta = "{0}\n".format(meta).encode("utf8")
        sys.stdout.buffer.write(meta)
