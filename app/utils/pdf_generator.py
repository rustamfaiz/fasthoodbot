import fitz  # PyMuPDF
import random

def generate_personal_pdf(input_path: str, output_path: str, full_name: str, phone_number: str):
    doc = fitz.open(input_path)

    for i, page in enumerate(doc):
        # Пропускаем обложку (первая страница)
        if i == 0:
            continue

        # Добавляем ФИО — в правый верхний угол
        page.insert_text(
            (page.rect.width - 120, 20),
            full_name,
            fontsize=8,
            color=(0, 0, 0),
        )

        # Добавляем телефон — в левый нижний угол
        page.insert_text(
            (20, page.rect.height - 20),
            phone_number,
            fontsize=8,
            color=(0, 0, 0),
        )

        # Водяной знак — на каждые 5–10 страниц (рандомно)
        if i % random.randint(5, 10) == 0:
            page.insert_textbox(
                page.rect,
                phone_number,
                fontsize=40,
                color=(0.9, 0.9, 0.9),  # светло-серый
                rotate=45,
                align=1,  # по центру
                overlay=True
            )

    doc.save(output_path)
    doc.close()
    return output_path  # ✅ обязательно вернуть путь к файлу
