from abc import ABC, abstractmethod
from typing import List

class DocumentElement(ABC):
    """Interface for all document elements"""
    @abstractmethod
    def render(self) -> str:
        """Render the element as a string"""
        return NotImplementedError("Subclasses must implement this method")

class TextElement(DocumentElement):
    """A Plain Text Element"""
    def __init__(self, text: str) -> None:
        self.text = text
    def render(self) -> str:
        return self.text

class ImageElement(DocumentElement):
    """An Image Element"""
    def __init__(self, url: str) -> None:
        self.url = url
    def render(self) -> str:
        return f"[Image: {self.url}]"

class NewLineElement(DocumentElement):
    """A New Line Element"""
    def render(self) -> str:
        return "\n"
class TabSpaceElement(DocumentElement):
    """A Tab Space Element"""
    def render(self) -> str:
        return "\t"

class Document:
    """A Document"""
    def __init__(self) -> None:
        self.elements: List[DocumentElement] = []
    def add_element(self, element: DocumentElement) -> None:
        self.elements.append(element)
    def render(self) -> str:
        return "".join(element.render() for element in self.elements)

class Persistence(ABC):
    """Interface for document persistence"""
    @abstractmethod
    def save(self, data: str) -> None:
        raise NotImplementedError("Subclasses must implement this method")

class FileStorage(Persistence):
    """Persists documents to a file"""
    def __init__(self, filepath: str="document.txt") -> None:
        self._file_path = filepath
    def save(self, data: str) -> None:
        try:
            with open(self._file_path, "w",encoding="utf-8") as out_file:
                out_file.write(data)
            print(f"Document saved to {self._file_path}")
        except IOError:
            print("Error:Unable to open file for writing")

class DBStorage(Persistence):
    """Placeholder for database"""
    def save(self, data: str) -> None:
        return 
class DocumentEditor:
    """Coordinates document editing, rendering, and saving."""
 
    def __init__(self, document: Document, storage: Persistence) -> None:
        self._document = document
        self._storage = storage
        self._rendered_document = ""
 
    def add_text(self, text: str) -> None:
        self._document.add_element(TextElement(text))
 
    def add_image(self, image_path: str) -> None:
        self._document.add_element(ImageElement(image_path))
 
    def add_new_line(self) -> None:
        self._document.add_element(NewLineElement())
 
    def add_tab_space(self) -> None:
        self._document.add_element(TabSpaceElement())
 
    def render_document(self) -> str:
        if not self._rendered_document:
            self._rendered_document = self._document.render()
        return self._rendered_document
 
    def save_document(self) -> None:
        self._storage.save(self.render_document())

def main() -> None:
    document = Document()
    persistence: Persistence = FileStorage()  # swap for DBStorage() with zero changes elsewhere
 
    editor = DocumentEditor(document, persistence)
 
    editor.add_text("Hello, world!")
    editor.add_new_line()
    editor.add_text("This is a real-world document editor example.")
    editor.add_new_line()
    editor.add_tab_space()
    editor.add_text("Indented text after a tab space.")
    editor.add_new_line()
    editor.add_image("picture.jpg")
 
    print(editor.render_document())
    editor.save_document()
 
 
if __name__ == "__main__":
    main()
 