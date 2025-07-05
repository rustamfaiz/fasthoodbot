import fitz  # PyMuPDF
import os
import re
from datetime import datetime
from pathlib import Path
from unidecode import unidecode  # pip install Unidecode

def sanitize_filename(text: str) -> str:
    # Удаляем все символы кроме латинских букв, цифр и подчёркиваний
    text = unidecode(text)
    text = re.sub(r"[^\w]", "_", text)
    return text

def generate_personal_pdf(name: str, phone: str) -> str:
    template_path = "files/book.pdf"
    output_dir = "files/generated"
    os.makedirs(output_dir, exist_ok=True)

    # Создаём безопасное имя файла
    safe_name = sanitize_filename(name)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{safe_name}_{timestamp}.pdf"
    output_path = os.path.join(output_dir, filename)

    # Загружаем шаблон PDF
    doc = fitz.open(template_path)

    for page_number, page in enumerate(doc, start=1):
        width, height = page.rect.width, page.rect.height

        # Метки на всех страницах, кроме первой
        if page_number != 1:
            # ФИО — правый верхний угол
            page.insert_text(
                (width - 150, 40),
                name,
                fontsize=8,
                fontname="helv",
                color=(0, 0, 0)
            )

            # Телефон — левый нижний угол
            page.insert_text(
                (40, height - 30),
                phone,
                fontsize=8,
                fontname="helv",
                color=(0, 0, 0)
            )

        # Водяной знак на каждой 5-й странице
        if page_number % 5 == 0:
            center = fitz.Point(width / 2, height / 2)
            matrix = fitz.Matrix(1, 1).prerotate(45)

            page.insert_text(
                center,
                phone,
                fontsize=30,
                fontname="helv",
                color=(0.8, 0.8, 0.8),
                rotate=0,
                render_mode=0,
                morph=matrix,
                fill_opacity=0.1
            )

    doc.save(output_path)
    doc.close()
    return output_path
