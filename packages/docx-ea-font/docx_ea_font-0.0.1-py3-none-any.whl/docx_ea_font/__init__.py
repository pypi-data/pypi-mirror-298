from docx.oxml.ns import qn
from docx.text.run import Run


def set_font(run: Run, font_name: str):
    run.font.name = font_name
    if run._element.rPr is None or run._element.rPr.rFonts is None:
        return
    r = run._element.rPr.rFonts
    r.set(qn("w:eastAsia"), font_name)

