# docx-ea-font
Fix the problem that the setting of East Asian fonts in python-docx is invalid or incorrect.

修正 python-docx 中东亚字体设置无效、不正确的问题。

## Installation

```
pip install docx-ea-font
```

## Example

```Python
from docx import Document
import docx_ea_font


doc = Document("tests/test.docx")
for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        docx_ea_font.set_font(run, "楷体")  # 传入一个 run 对象以及字体名称

doc.save('font-changed.docx')
```
