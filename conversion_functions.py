import markdown
from pygments.formatters import HtmlFormatter

def markdown_to_html(md_content):
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])

    # Add custom CSS for styling
    css = HtmlFormatter().get_style_defs('.codehilite')
    styled_html = f'<style>{css}</style>\n{html_content}'

    return styled_html