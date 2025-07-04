import fitz  # PyMuPDF
import random
import os

def generate_marked_pdf(input_path: str, output_path: str, full_name: str, phone: str):
    doc = fitz.open(input_path)

    # Настройки шрифта и координат
    font_size = 10
    margin = 30

    for i, page in enumerate(doc):
        # Пропускаем первую страницу (обложку)
        if i == 0:
            continue

        # Верхний правый угол — фамилия
        page.insert_text(
            (page.rect.width - margin * 5, margin),
            full_name,
            fontsize=font_size,
            color=(0.5, 0.5, 0.5),
            overlay=True
        )

        # Нижний левый угол — номер телефона
        page.insert_text(
            (margin, page.rect.height - margin),
            phone,
            fontsize=font_size,
            color=(0.5, 0.5, 0.5),
            overlay=True
        )

        # Каждая 5–10 страница — водяной знак на весь лист
        if (i % random.randint(5, 10)) == 0:
            text = f"Тел: {phone}"
            rect = page.rect
            page.insert_textbox(
                rect,
                text,
                fontsize=60,
                color=(0.9, 0.9, 0.9),
                rotate=45,
                align=1,  # центр
                overlay=True
            )

    # Сохраняем файл
    doc.save(output_path)
    doc.close()
