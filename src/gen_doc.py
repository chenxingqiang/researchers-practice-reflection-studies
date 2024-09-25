import os
import re
from PIL import Image
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mermaid_to_image import mermaid_to_image
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def set_font_style(paragraph, font_name="Times New Roman", font_size=12):
    """ Set font to Times New Roman and size for all runs in a paragraph. """
    for run in paragraph.runs:
        run.font.name = font_name
        run.font.size = Pt(font_size)
        # This is necessary for non-ASCII characters to work properly
        r = run._element
        rPr = r.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)
        rPr.append(rFonts)


def insert_image_to_docx(doc, img_path, width=None):
    try:
        # Insert the image into the document
        if width:
            doc.add_picture(img_path, width=Inches(width))
        else:
            doc.add_picture(img_path)
        return True
    except Exception as e:
        logging.error(f"Error inserting image {img_path}: {e}")
        return False


def mermaid_to_base64_image(mermaid_code, lesson_num, diagram_count, output_path):
    try:
        # Generate file name for SVG image
        file_name = f"lesson_{lesson_num}_mermaid_{diagram_count}.svg"
        output_file = os.path.join(
            output_path, f"lesson_{lesson_num}", file_name)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Use mermaid_to_image function to generate SVG
        if mermaid_to_image(mermaid_code, output_file, format="svg"):
            return output_file  # Return the path to the generated SVG
        else:
            raise Exception("Mermaid image generation failed")
    except Exception as e:
        logging.error(f"Error generating Mermaid diagram: {e}")
        return None


def convert_markdown_to_docx(content, doc, lesson_num):
    # Regex to find Markdown patterns
    header_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    bold_pattern = re.compile(r"\*\*(.*?)\*\*")
    italic_pattern = re.compile(r"\*(.*?)\*")
    code_pattern = re.compile(r"`([^`]*)`")

    # Define regex pattern to match code blocks and non-code parts
    block_code_pattern = re.compile(r"```(.*?)\n(.*?)```", re.DOTALL)

    last_pos = 0
    mermaid_count = 0  # Count Mermaid diagrams

    # Handling block code like ```python``` or ```mermaid```
    for match in block_code_pattern.finditer(content):
        markdown_text = content[last_pos:match.start()].strip()
        process_markdown_text(markdown_text, doc)

        # Handle code block
        # Get code type (e.g., 'python', 'mermaid')
        code_type = match.group(1).strip()
        code_text = match.group(2).strip()

        if code_type.lower() == "python":
            # Add Python code block as plain text
            code_paragraph = doc.add_paragraph(code_text)
            # Using monospace font for code
            set_font_style(
                code_paragraph, font_name="Courier New", font_size=10)
        elif code_type.lower() == "mermaid":
            # Handle Mermaid diagram
            mermaid_count += 1
            svg_file = mermaid_to_base64_image(
                code_text, lesson_num, mermaid_count, output_path)
            if svg_file:
                try:
                    png_file = svg_file.replace(".svg", ".png")
                    img = Image.open(svg_file)
                    img.save(png_file)
                    insert_image_to_docx(doc, png_file, width=4.0)
                except Exception as e:
                    doc.add_paragraph(
                        f"Mermaid diagram {mermaid_count} could not be inserted.")
            else:
                doc.add_paragraph(f"```mermaid\n{code_text}\n```")
        else:
            # Insert other code blocks as plain text
            doc.add_paragraph(f"```{code_type}\n{code_text}\n```")

        last_pos = match.end()

    # Process remaining text after the last code block
    remaining_text = content[last_pos:].strip()
    process_markdown_text(remaining_text, doc)


def process_markdown_text(text, doc):
    """Process markdown text for headers, bold, italics, and inline code."""
    header_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    bold_pattern = re.compile(r"\*\*(.*?)\*\*")
    italic_pattern = re.compile(r"\*(.*?)\*")
    code_pattern = re.compile(r"`([^`]*)`")

    lines = text.split("\n")
    for line in lines:
        # Check if it's a header
        header_match = header_pattern.match(line)
        if header_match:
            header_level = len(header_match.group(1))
            header_text = header_match.group(2)
            paragraph = doc.add_heading(header_text, level=header_level)
            set_font_style(paragraph)
            continue

        # Handle inline bold, italic, and code formatting
        line = bold_pattern.sub(r"\1", line)
        line = italic_pattern.sub(r"\1", line)
        line = code_pattern.sub(r"\1", line)

        paragraph = doc.add_paragraph(line)
        set_font_style(paragraph)


def text_to_docx(input_file, output_file, lesson_num):
    # Read the input Markdown file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Create a new Document (docx)
    doc = Document()

    # Convert the Markdown content to docx
    convert_markdown_to_docx(content, doc, lesson_num)

    # Save the document as a .docx file
    doc.save(output_file)
    logging.info(f"Document created: {output_file}")


# Main program
input_files = [
    "Reflective Practice as a Strategy for Early Career Academics.md",
    # Add more files as needed
]

input_path = "./"
output_base_path = "./docx/"
output_path = os.path.join(output_base_path, "docx_output")

# Create the output path if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

for name in input_files:
    lesson_num = name.split('.')[0]
    lesson_folder = os.path.join(output_path, f"doc_{lesson_num}")
    if not os.path.exists(lesson_folder):
        os.makedirs(lesson_folder)

    input_file = os.path.join(input_path, name)
    output_file = os.path.join(lesson_folder, name.replace(".md", ".docx"))

    text_to_docx(input_file, output_file, lesson_num)
    logging.info(f"Document has been created: {output_file}")
