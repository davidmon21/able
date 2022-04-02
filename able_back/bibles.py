from pysword.modules import SwordModules
from pysword.bible import SwordBible



class Bibles:
    bible_collection = None
    sword = None
    def __init__(self, bibles_path):
        self.sword = SwordModules(bibles_path)
        self.bible_collection = self.sword.parse_modules()

    def get_versions(self):
        version_info = {}
        for version in self.bible_collection.keys():
            version_info[version] = self.bible_collection[version]['description']
        return version_info

    def get_books(self,version):
        books = self.sword.get_bible_from_module(version).get_structure().get_books()
        book_dict = {'ot':{},'nt':{}}
        for book in books['ot']:
            book_dict['ot'][book.osis_name] = { "name": book.name }
            book_dict['ot'][book.osis_name]["chapters"] = dict(zip(list(range(1,book.num_chapters+1)),book.chapter_lengths))
        for book in books['nt']:
            book_dict['nt'][book.osis_name] = { "name": book.name}
            book_dict['nt'][book.osis_name]["chapters"] = dict(zip(list(range(1,book.num_chapters+1)),book.chapter_lengths))
        return book_dict

    def acceptable_book(self,version):
        abn = []
        books = self.sword.get_bible_from_module(version).get_structure().get_books()
        for book in books['ot']:
            abn.push(book.osis_name)
            abn.push(book.name)
        for book in books['nt']:
            abn.push(book.osis_name)
            abn.push(book.name)
        return abn
        

    def get_text(self, version, books=None, chapters=None, verses=None):
        if version in self.get_versions().keys():
            version = version
        else:
            version = 'DRC'
        if verses != None:
            verses=list(range(verses[0],verses[1]+1))
            print(verses)
        return_dict = {"version": version}
        return_dict["books"] = books
        return_dict["chapters"] = chapters
        text = {}
        if type(books) == list:
            for book in books:
                for chapter in chapters:
                    text[chapter] = list(self.sword.get_bible_from_module(version).get_iter(book,chapter,verses))
                    if verses == None:
                        addedv = list(range(1,len(rtxt)+1))
                    else:
                        addedv = verses
                    text[chapter] = dict(zip(addedv,rtxt))
                return_dict["text"][book] = text
        elif type(chapters) == list:
            for chapter in chapters:
                rtxt = list(self.sword.get_bible_from_module(version).get_iter(books,chapter,verses))
                if verses == None:
                    addedv = list(range(1,len(rtxt)+1))
                else:
                    addedv = verses
                text[chapter] = dict(zip(addedv,rtxt))
            return_dict["text"] = {}
            return_dict["text"][books] = text
        return return_dict
        