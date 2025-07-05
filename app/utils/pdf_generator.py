import fitz  # PyMuPDF
import os


def generate_personal_pdf(name: str, phone: str) -> str:
    template_path = "files/book.pdf"
    output_path = f"files/generated_{phone}.pdf"

    doc = fitz.open(template_path)

    for page_number in range(len(doc)):
        page = doc[page_number]
        width, height = page.rect.width, page.rect.height

        # Вставка имени в правом верхнем углу (кроме первой страницы)
        if page_number != 0:
            page.insert_text(
                fitz.Point(width - 150, 40),
                name,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
            )

        # Вставка номера телефона в левый нижний угол (на всех страницах)
        page.insert_text(
            fitz.Point(40, height - 40),
            phone,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
        )

        # Вставка водяного знака на каждой 5–10 странице
        if page_number % 5 == 0:
            center = fitz.Point(width / 2, height / 2)
            matrix = fitz.Matrix(1, 1).prerotate(45)
            morph = [matrix, matrix]  # двойной — от и до

            page.insert_text(
                center,
                phone,
                fontsize=30,
                fontname="helv",
                color=(0.8, 0.8, 0.8),
                rotate=0,
                render_mode=0,
                morph=morph,
                fill_opacity=0.1
            )

    doc.save(output_path)
    doc.close()

    return output_path
