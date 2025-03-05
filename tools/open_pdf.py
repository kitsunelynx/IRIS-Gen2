import PyPDF2
from pathlib import Path
from core.tools.tool_interface import ToolInterface, ToolContext
from typing import List, Callable
import subprocess
import os


def extract_text_from_pdf(pdf_file_path: str, context: ToolContext) -> str:
    """
    Extracts text from a single PDF file or all PDF files within a directory.
    
    Args:
        pdf_file_path (str): The path to a PDF file or a directory containing PDF files.
        context (ToolContext): The tool context for logging.
        
    Returns:
        str: The extracted text. If multiple files are read, each file's content is 
             prefixed with a header indicating the file name.
    """
    text = ""
    path = Path(pdf_file_path)
    
    if path.is_dir():
        # Process all PDF files in the directory
        for pdf in path.glob("*.pdf"):
            try:
                with pdf.open("rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    file_text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            file_text += page_text
                if file_text:
                    text += f"--- Content from: {pdf.name} ---\n{file_text}\n\n"
                    context.success(f"Extracted text from PDF: {pdf.name}")
            except Exception as e:
                context.error(f"Error reading file {pdf.name}: {e}")
                text += f"Error reading file {pdf.name}: {e}\n"
    else:
        # Process a single PDF file
        try:
            with path.open("rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            context.success(f"Extracted text from PDF: {pdf_file_path}")
        except Exception as e:
            context.error(f"Error reading {pdf_file_path}: {e}")
            text = f"Error reading {pdf_file_path}: {e}"
    
    return text

class OpenPDFTool(ToolInterface):
    @property
    def name(self) -> str:
        return "OpenPDFTool"
    
    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering OpenPDFTool tools.")

        def open_pdf(filepath: str) -> str:
            try:
                if os.path.exists(filepath):
                    if os.name == 'nt':
                        os.startfile(filepath)
                    else:
                        subprocess.call(["open", filepath])
                    # Extract text from the PDF using our helper function which logs via context.
                    result = extract_text_from_pdf(filepath, context)
                    return result
                else:
                    context.error("PDF file not found.")
                    return "PDF file not found"
            except Exception as e:
                context.error(f"Error opening PDF: {e}")
                return f"Error opening PDF: {e}"

        return [open_pdf]

def register():
    try:
        return OpenPDFTool()
    except Exception as e:
        from core.utils.logger import get_logger
        get_logger().error(f"Error during open_pdf_tool registration: {e}")
        return None

