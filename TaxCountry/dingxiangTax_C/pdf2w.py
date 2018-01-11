import pypandoc
output = pypandoc.convert_file('file.html', 'docx',outputfile="file1.docx")
assert output == ""