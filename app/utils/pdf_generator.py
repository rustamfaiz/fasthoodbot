import fitz  # PyMuPDF
import random

def generate_personal_pdf(input_path: str, output_path: str, full_name: str, phone_number: str):
    print(f"🛠️ Генерация PDF: {full_name}, {phone_number}")  # 🔍 Проверка вызова

    doc = fitz.open(input_path)

    for i, page in enumerate(doc):
        if i == 0:
            continue

        page.insert_text(
            (page.rect.width - 120, 20),
            full_name,
            fontsize=8,
            color=(0, 0, 0),
        )

        page.insert_text(
            (20, page.rect.height - 20),
            phone_number,
            fontsize=8,
            color=(0, 0, 0),
        )

        if i % random.randint(5, 10) == 0:
            page.insert_textbox(
                page.rect,
                phone_number,
                fontsize=40,
                color=(0.9, 0.9, 0.9),
                rotate=45,
                align=1,
                overlay=True
            )

    doc.save(output_path)
    doc.close()
    return output_path
