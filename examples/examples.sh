# Write all the epub meta in a new line delimited json file
for afile in ~/*.epub; do python -m shobdokutir.ebook.parser --get_epub_meta $afile >> ~/epub_meta.json; done

# Write all the epub contents in a new line delimited json file
for afile in ~/*.epub; do python -m shobdokutir.ebook.parser --get_epub_text $afile >> ~/epub_contents.json; done