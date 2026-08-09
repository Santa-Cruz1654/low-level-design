# Document Editor — LLD

A simple document editor designed and implemented in Python as my first Low-Level Design exercise.

## Problem

Design a document editor that supports different types of document elements:

* Text
* Images
* New lines
* Tab spaces

The document should be rendered into a string and saved using a pluggable persistence mechanism.

## Design

The design separates document elements, document management, persistence, and editor coordination.

```text
                    DocumentElement
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
    TextElement     ImageElement     NewLineElement
                                           │
                                     TabSpaceElement


                     Document
                        │
                        ▼
              List[DocumentElement]


                     Persistence
                         │
                 ┌───────┴────────┐
                 ▼                ▼
           FileStorage        DBStorage


                  DocumentEditor
                  /           \
                 ▼             ▼
            Document       Persistence
```

## SOLID Principles

### Single Responsibility Principle

Each class has a focused responsibility.

* `DocumentElement` defines the element contract.
* `TextElement` handles text rendering.
* `ImageElement` handles image rendering.
* `Document` manages document elements.
* `FileStorage` handles file persistence.
* `DBStorage` represents database persistence.
* `DocumentEditor` coordinates editing, rendering, and saving.

### Open/Closed Principle

New document element types or persistence implementations can be added without modifying the existing `Document` and `DocumentEditor` implementations.

For example:

```python
class VideoElement(DocumentElement):
    def render(self) -> str:
        return "[Video]"
```

### Liskov Substitution Principle

Concrete `DocumentElement` implementations can be used wherever a `DocumentElement` is expected.

Similarly, different `Persistence` implementations can be substituted without changing `DocumentEditor`.

### Interface Segregation Principle

The abstractions are small and focused.

```text
DocumentElement
    └── render()

Persistence
    └── save()
```

### Dependency Inversion Principle

`DocumentEditor` depends on the `Persistence` abstraction rather than directly depending on `FileStorage`.

```python
persistence: Persistence = FileStorage()

editor = DocumentEditor(document, persistence)
```

The storage implementation can later be replaced with another `Persistence` implementation.

## Concepts Learned

* Abstract Base Classes
* Abstraction
* Encapsulation
* Inheritance
* Polymorphism
* Composition
* Dependency Injection
* Programming to abstractions
* SOLID principles

## Running the Project

From the `01-document-editor` directory:

```bash
python document_editor.py
```

The application renders the document and saves it to `document.txt`.

## Example Output

```text
Hello, world!
This is a real-world document editor example.
    Indented text after a tab space.
[Image: picture.jpg]

Document saved to document.txt
```

## Possible Future Improvements

* Database persistence
* Markdown rendering
* HTML rendering
* PDF export
* Additional document element types
* Unit tests
* Factory pattern for element creation
* Undo/redo functionality
* Better error handling

## What I Learned

This project is my first step into Low-Level Design. It helped me understand how abstraction, polymorphism, composition, dependency injection, and SOLID principles can be used to build an extensible object-oriented design.
