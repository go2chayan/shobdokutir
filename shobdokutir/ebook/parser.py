import os
import sys
import json
import argparse
from typing import Generator, Iterator, List, Dict, BinaryIO
import zipfile as zf

from bs4 import BeautifulSoup
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

from shobdokutir.encoding.utils import file_hash


#TODO: Refactor this function to return a dictionary, not json. jsonification will be done in main
def epub_meta_to_json(epub_file: str) -> str:
    """
    Reads the content.opf file of an epub and produces a json str with the following schema.
    The schema is designed to be stored as a bigquery table.

    ## Metadata Schema
    md5_hash, all_ids, title, creator, epub_filename, manifest, spine, content_str

    ## Manifest Schema
    [ {'id': id, 'item': item, 'media_type': media_type}, ... ]

    ## Spine Schema
    [idref, idref, ...]
    """
    def find_content_file(epub):
        content_file = [a_file for a_file in epub.namelist() if "content.opf" in a_file.lower()]
        if not content_file:
            raise Exception("content.opf file not found in epub")
        return content_file[0]

    def extract_meta(content, epub_file):
        _, epub_filename = os.path.split(epub_file)
        output_blob = {'md5_hash': file_hash(open(epub_file, "rb")), 'epub_filename': epub_filename, 'content_str': content}
        content_parsed = BeautifulSoup(content, "lxml")
        if content_parsed.metadata is None:
            output_blob['all_ids'] = None
            output_blob['title'] = None
            output_blob['creator'] = None
        else:
            all_ids = []
            all_id_tags = content_parsed.find_all("dc:identifier")
            for an_id in all_id_tags:
                an_id_attrs = {a_key.replace(":", "_"): an_id.attrs[a_key] for a_key in an_id.attrs}
                all_ids.append({"value": an_id.text, "attrs": an_id_attrs})
            output_blob['all_ids'] = all_ids
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
            meta_data = clean_xhtml_code(meta_file.read())
            return extract_meta(meta_data, epub_file)


def clean_xhtml_code(xhtml: str) -> str:
    return " ".join(xhtml.decode("utf-8").split('\n'))


def epub_xhtml_iter(epub_file: str) -> str:
    """
    An iterator that yields the xhtml contents of an epub and other info
    """
    meta_data = json.loads(epub_meta_to_json(epub_file))
    if 'spine' not in meta_data or meta_data['spine'] is None or \
            'manifest' not in meta_data or meta_data['manifest'] is None:
        raise Exception(
            "Critical metainfo was not found in: {0}".format(epub_file))
    manifest_map = {
        manifest_item['id']: manifest_item for manifest_item in meta_data['manifest']}
    with zf.ZipFile(epub_file) as epub:
        for i, idref in enumerate(meta_data['spine']):
            if not idref in manifest_map:
                raise Exception(
                    "Spine content was not found in manifest {0}".format(epub_file))
            xhtml = manifest_map[idref]['item']
            with epub.open(xhtml) as epub_page:
                xhtml_md5_hash = file_hash(epub_page)
            with epub.open(xhtml) as epub_page:
                xhtml_content = epub_page.read()
            yield {'xhtml_content': xhtml_content, 'xhtml_md5_hash': xhtml_md5_hash,
                   'epub_md5_hash': meta_data['md5_hash'], 'xhtml_href': xhtml, 'xhtml_index': i}


def parse_xhtml_contents(xhtml: str) -> Dict:
    cleaned_content = clean_xhtml_code(xhtml)
    parsed_content = BeautifulSoup(cleaned_content, "lxml")
    record = {'xhtml_code': cleaned_content, 
              'title': parsed_content.title.get_text() if parsed_content.title else "",
              'text': parsed_content.body.get_text() if parsed_content.body else "",
              'text_split': [a_tag.get_text() for a_tag in parsed_content.body.contents if a_tag.name],
              'text_split_type': [a_tag.name for a_tag in parsed_content.body.contents if a_tag.name]
              }
    return record


def epub_to_json(epub_file: str) -> List[str]:
    """
    Reads the xhtml files of an epub and produces a list of json strings with the following schema.
    The schema is designed to be stored as a bigquery table.

    Metadata Schema
    ---------------
    epub_md5_hash, xhtml_index, xhtml_href, xhtml_md5_hash, title, text, text_split, 
    text_split_type, xhtml_code

    text_split
    ----------
    [ <text 1>, <text 2>, <text 3> ... ]

    text_split_type
    ---------------
    [h1, h2, p, ... ]
    """
    output_records = []
    for a_page in epub_xhtml_iter(epub_file):
        record = {a_key: a_page[a_key] for a_key in a_page if not a_key == 'xhtml_content'}
        parsed_xhtml = parse_xhtml_contents(a_page['xhtml_content'])
        record.update(parsed_xhtml)
        output_records.append(record)
    return output_records


def epub_iter(epub_file: str) -> Iterator[Dict]:
    """
    A python generator that iterates over the html files within an epub file.
    :param epub_file: Full path of the file
    :return: Iterator containing a dictionary of 'title' and body ('text') texts for each html within the epub
    """
    for an_item in epub_xhtml_iter(epub_file):
        text_seg = BeautifulSoup(an_item['xhtml_content'].decode(), 'lxml')
        yield {'title': text_seg.title.get_text() if text_seg.title else "", 'text': text_seg.body.get_text()}


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
    parser.add_argument("--get_meta", action="store", default=None, type=str, nargs="+", help="Extracts the meta for a given epub and outputs to stdout \
        as a newline-delimited json. Please provide the full path of the epub file as an input argument.")
    args = parser.parse_args()

    if args.get_meta:
        filename = " ".join(args.get_meta)
        meta = epub_meta_to_json(filename).decode("utf-8")
        meta = "{0}\n".format(meta).encode("utf8")
        sys.stdout.buffer.write(meta)
