class Book:

    def __init__(self, title, author, release_year, pages, description):
        self.title = title
        self.author = author
        self.release_year = release_year
        self.pages = pages
        self.description = description

    def print_basic_info(self):
        print(f"📚 Book information: \n\
         ✅ title:        {self.title}\n \
        ✅ author:       {self.author}\n \
        ✅ release year: {self.release_year}\n \
        ✅ pages:        {self.pages}")
    
    def print_description(self):
        print(f"📖 Book description:\n{self.description}")
