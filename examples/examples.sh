# Write all the epub meta in a new line delimited json file
for afile in ~/*.epub; do python -m shobdokutir.ebook.parser --get_epub_meta $afile >> ~/epub_meta.json; done

# Write all the epub contents in a new line delimited json file
for afile in ~/*.epub; do python -m shobdokutir.ebook.parser --get_epub_text $afile >> ~/epub_contents.json; done

# Rename files to their md5 hash
python -m shobdokutir.encoding.utils --rename_md5 ~/epub/