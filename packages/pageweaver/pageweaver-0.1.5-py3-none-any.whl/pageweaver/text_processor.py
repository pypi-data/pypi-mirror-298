import re

class TextProcessor:
    """
    A utility class for processing text, specifically for LaTeX document preparation.

    Methods
    -------
    escape_latex_special_characters(text: str) -> str
        Escapes special characters in a given text to make it LaTeX compatible.

    remove_non_utf8_characters(text: str) -> str
        Removes non-UTF-8 characters from the text and escapes LaTeX special characters.
    """
    @staticmethod
    def escape_latex_special_characters(text):
        latex_special_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        for char, escaped_char in latex_special_chars.items():
            text = text.replace(char, escaped_char)
        return text

    @staticmethod
    def remove_non_utf8_characters(text):
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = TextProcessor.escape_latex_special_characters(text)
        return text