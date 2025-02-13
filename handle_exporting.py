import streamlit as st
from xhtml2pdf import pisa
import io


def convert_html_to_pdf(html_content):
    output = io.BytesIO()

    pisa.CreatePDF(html_content, dest=output)
    return output