from document_editor import (
    Document,
    TextElement,
    ImageElement,
    NewLineElement,
    TabSpaceElement,
)


def test_text_element():
    element = TextElement("Hello")
    assert element.render() == "Hello"


def test_image_element():
    element = ImageElement("picture.jpg")
    assert element.render() == "[Image: picture.jpg]"


def test_new_line_element():
    element = NewLineElement()
    assert element.render() == "\n"


def test_tab_space_element():
    element = TabSpaceElement()
    assert element.render() == "\t"


def test_document_render():
    document = Document()

    document.add_element(TextElement("Hello"))
    document.add_element(NewLineElement())
    document.add_element(TextElement("World"))

    assert document.render() == "Hello\nWorld"