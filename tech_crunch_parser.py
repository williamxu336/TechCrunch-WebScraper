from html.parser import HTMLParser

class TechCrushParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.author = ''
        self.paragraphs = []
        self.current_paragraph = ''
        self.published_time = ''
        self.modified_time = ''
        self.type = ''
        self.featured = False
    
    # Handles the starting tag
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            # Retrieve the title of the article
            if attrs[0][1] == 'og:title':
                self.title = attrs[1][1]
            
            # Retrieve the author of the article
            if attrs[0][1] == 'author':
                self.author = attrs[1][1]

            # Retrieve the author of the article
            if attrs[0][1] == 'article:published_time':
                self.published_time = attrs[1][1]

            # Retrieve the author of the article
            if attrs[0][1] == 'article:modified_time':
                self.modified_time = attrs[1][1]

            # Retrieve the type/category of the article
            if attrs[0][1] == 'mrf:tags':
                if attrs[1][1].split(';')[1].split(':')[0] == 'TC Plus':
                    self.type = f'TechCrunch+ {attrs[1][1].split(";")[1].split(":")[1]}'
                else:
                    self.type = attrs[1][1].split(';')[2].split(':')[1]

        # Check if the article is featured or not
        if tag == 'header':
            if attrs[0][1] == 'article__header article-featured__header':
                self.featured = True

        if tag == 'p':
            # Build the current Paragraph
            self.current_paragraph = ''

    # Handles the endtag
    def handle_endtag(self, tag):
        # Build the all the paragraphs
        if tag == 'p':
            self.paragraphs.append(self.current_paragraph.strip())
            self.current_paragraph = ''

    # Handles the data
    def handle_data(self, data):
        # Build the current paragraphs
        self.current_paragraph += data
