import subprocess
import os

def convert_markdown_to_pdf(markdown_path, pdf_path):
    """Converts a Markdown file to PDF using manus-md-to-pdf utility.

    Args:
        markdown_path (str): Path to the input Markdown file.
        pdf_path (str): Path to save the output PDF file.
    """
    try:
        command = ["manus-md-to-pdf", markdown_path, pdf_path]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully converted \'{markdown_path}\' to \'{pdf_path}\'")
    except subprocess.CalledProcessError as e:
        print(f"Error converting Markdown to PDF: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
    except FileNotFoundError:
        print(f"Error: manus-md-to-pdf utility not found. Please ensure it is installed and in your PATH.")

if __name__ == "__main__":
    # Create a dummy markdown file for testing
    dummy_md_content = "# Test Guide\n\nThis is a test markdown file to be converted to PDF.\n\n## Section 1\n\n- Item 1\n- Item 2\n\n### Subsection\n\nSome more text here."
    dummy_md_path = "dummy_guide.md"
    dummy_pdf_path = "dummy_guide.pdf"

    with open(dummy_md_path, "w") as f:
        f.write(dummy_md_content)
    print(f"Created dummy markdown file: {dummy_md_path}")

    # Convert the dummy markdown to PDF
    convert_markdown_to_pdf(dummy_md_path, dummy_pdf_path)

    # Clean up dummy files
    if os.path.exists(dummy_md_path):
        os.remove(dummy_md_path)
    if os.path.exists(dummy_pdf_path):
        os.remove(dummy_pdf_path)


