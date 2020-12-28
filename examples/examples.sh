# Write all the epub meta in a new line delimited json file
for afile in ~/*.epub; do python -m shobdokutir.ebook.parser --get_meta $afile >> ~/epub_meta.json; done
