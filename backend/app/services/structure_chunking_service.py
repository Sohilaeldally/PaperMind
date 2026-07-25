from pathlib import Path
import re
import fitz
from docx import Document as DocxDocument
from app.models.pdf_line import PdfLine
from app.models.document import DocumentType

def try_docx_style_based(file_path: Path) -> list[tuple[str, str]] | None:
    doc = DocxDocument(file_path)

    sections = []
    current_title = "Preamble"
    current_text = []

    for para in doc.paragraphs:

        if para.style and para.style.name.startswith("Heading"):

            title = para.text.strip()

            if not title:
                continue

            if current_text:
                sections.append(
                    (
                        current_title,
                        "\n".join(current_text),
                    )
                )

            current_title = title
            current_text = []

        else:

            text = para.text.strip()

            if text:
                current_text.append(text)

    if current_text:
        sections.append(
            (
                current_title,
                "\n".join(current_text),
            )
        )

    if len(sections) <= 1:
        return None

    return sections


def try_pdf_font_based(file_path: Path) -> list[tuple[str, str]] | None:

    doc = fitz.open(file_path)

    all_lines: list[PdfLine] = []
    font_sizes = []

    for page in doc:

        blocks = page.get_text("dict")["blocks"]

        for block in blocks:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                spans = line["spans"]

                if not spans:
                    continue

                text = "".join(
                    span["text"]
                    for span in spans
                ).strip()

                if not text:
                    continue

                size = spans[0]["size"]
                bold = "bold" in spans[0]["font"].lower()

                all_lines.append(
                    PdfLine(
                        text=text,
                        size=size,
                        bold=bold,
                    )
                )

                font_sizes.append(size)

    doc.close()

    if not all_lines:
        return None

    average_size = sum(font_sizes) / len(font_sizes)
    heading_threshold = average_size * 1.15

    sections = []
    current_title = "Preamble"
    current_text = []

    for line in all_lines:

        is_heading = (
            (
                line.size >= heading_threshold
                or line.bold
            )
            and len(line.text) < 80
        )

        if is_heading:

            if current_text:
                sections.append(
                    (
                        current_title,
                        "\n".join(current_text),
                    )
                )

            current_title = line.text
            current_text = []

        else:

            current_text.append(line.text)

    if current_text:
        sections.append(
            (
                current_title,
                "\n".join(current_text),
            )
        )

    if len(sections) <= 1:
        return None

    return sections


ACADEMIC_HEADINGS = [
    "abstract","introduction","related work","related works","background","methodology","methods",
    "materials and methods","approach",    "model architecture","architecture","system design",
    "implementation","experimental setup","experiments",    "experimental results","results",
    "evaluation","discussion","analysis","conclusion","conclusions","future work","limitations",
    "acknowledgments","acknowledgements","training","dataset","references","appendix","appendices",
]

KNOWN_HEADING_PATTERN = re.compile(
    r"^\s*(?:\d+(?:\.\d+)?\.?\s*)?("
    + "|".join(ACADEMIC_HEADINGS)
    + r")\s*:?\s*$",
    re.IGNORECASE,
)

NUMBERED_HEADING_PATTERN = re.compile(
    r"^\s*\d+\.?\s+[A-Z][a-zA-Z\-]*(?:\s+[A-Za-z][a-zA-Z\-]*){0,5}\s*$"
)


def is_heading_line(line: str) -> bool:

    stripped = line.strip()

    if not stripped:
        return False

    if len(stripped) > 60:
        return False

    if stripped.endswith((".", ",", ";")):
        return False

    if KNOWN_HEADING_PATTERN.match(stripped):
        return True

    if NUMBERED_HEADING_PATTERN.match(stripped):
        return True

    return False


def try_regex_based(raw_text: str) -> list[tuple[str, str]] | None:

    lines = raw_text.split("\n")

    sections = []
    current_title = "Preamble"
    current_text = []

    for line in lines:

        stripped = line.strip()

        if is_heading_line(stripped):

            if current_text:
                sections.append(
                    (
                        current_title,
                        "\n".join(current_text),
                    )
                )

            current_title = stripped
            current_text = []

        else:

            if stripped:
                current_text.append(stripped)

    if current_text:
        sections.append(
            (
                current_title,
                "\n".join(current_text),
            )
        )

    if len(sections) <= 1:
        return None

    return sections



def detect_sections(
    file_path: Path,
    raw_text: str,
    content_type: str,
) -> list[tuple[str, str]] | None:

    try:
        doc_type = DocumentType(content_type)
    except ValueError:
        doc_type = None

    if doc_type == DocumentType.DOCX:
        sections = try_docx_style_based(file_path)
        if sections:
            return sections

    if doc_type == DocumentType.PDF:
        sections = try_pdf_font_based(file_path)
        if sections:
            return sections

    sections = try_regex_based(raw_text)

    if sections:
        return sections

    return None