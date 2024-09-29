from pylatex import Document, Section, Command, NoEscape

class DocumentGenerator:
    """
    A class used to generate a LaTeX document with chapters and compile it into a PDF.

    Attributes
    ----------
    doc : Document
        An instance of the Document class from pylatex, representing the LaTeX document.

    Methods
    -------
    __init__(title, author)
        Initializes the DocumentGenerator with a title and author, sets up the document class, preamble, and title page.
    
    add_chapter(chapter_heading, text)
        Adds a chapter to the document with the given heading and text.
    
    generate_pdf(filename, clean_tex=True)
        Generates a PDF from the LaTeX document and saves it with the given filename.
    """
    def __init__(self, title, author):
        self.doc = Document(lmodern=False)
        self.doc.documentclass = Command(
            'documentclass',
            options=['12pt', 'a4paper'],
            arguments=['article'],
        )
        self.doc.preamble.append(Command('title', title))
        self.doc.preamble.append(Command('author', author))
        self.doc.preamble.append(Command('date', NoEscape(r'\today')))
        self.doc.append(NoEscape(r'\maketitle'))
        self.doc.preamble.append(Command('usepackage', 'bookmark'))
        self.doc.preamble.append(Command('usepackage','libertine'))
        self.doc.append(NoEscape(r'\tableofcontents'))

    def add_chapter(self, chapter_heading, text):
        with self.doc.create(Section(chapter_heading, numbering=True)):
            self.doc.append(text)
        print(f"Chapter {chapter_heading} saved.")

    def generate_pdf(self, filename, clean_tex=True):
        self.doc.generate_pdf(filename, clean_tex=clean_tex)