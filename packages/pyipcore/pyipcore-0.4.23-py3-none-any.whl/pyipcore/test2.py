from docx2pdf import convert

# 使用函数转换文档
doc_path = 'test.docx'  # Word文档路径
pdf_path = 'test.pdf'  # 输出PDF路径
convert(doc_path, pdf_path)