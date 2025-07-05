import fitz  # PyMuPDF
import os
from datetime import datetime
from pathlib import Path

def generate_personal_pdf(name: str, phone: str) -> str:
    template_path = "files/book.pdf"
    output_dir = "files/generated"
    os.makedirs(output_dir, exist_ok=True)

    # Уникальное имя файла
    safe_name = name.replace(" ", "_")
    filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join(output_dir, filename)

    # Открываем шаблон
    doc = fitz.open(template_path)

    for page_number, page in enumerate(doc, start=1):
        width, height = page.rect.width, page.rect.height

        # Пропускаем первую страницу (обложку)
        if page_number != 1:
            # ФИО — в правом верхнем углу
            page.insert_text(
                (width - 150, 40),
                name,
                fontsize=8,
                color=(0, 0, 0),
                fontname="helv",
            )

            # Телефон — в левом нижнем углу
            page.insert_text(
                (40, height - 30),
                phone,
                fontsize=8,
                color=(0, 0, 0),
                fontname="helv",
            )

        # Водяной знак на каждой 5-й странице
        if page_number % 5 == 0:
            page.insert_textbox(
                page.rect,
                phone,
                fontsize=30,
                rotate=45,
                fontname="helv",
                color=(0.8, 0.8, 0.8),
                align=1,
                overlay=True,
                fill_opacity=0.1,
            )

    # Сохраняем
    doc.save(output_path)
    doc.close()

    return output_path
