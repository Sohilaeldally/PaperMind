from dataclasses import dataclass

@dataclass
class PdfLine:
    text: str
    size: float
    bold: bool
