from pathlib import Path
import random
import fitz  # PyMuPDF

# Путь к шаблону PDF-книги
TEMPLATE_PATH = Path("files/book.pdf")
OUTPUT_DIR = Path("files/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_personal_pdf(name: str, phone: str) -> str:
    # Загружаем шаблон книги
    doc = fitz.open(TEMPLATE_PATH)

    # Настройки текста
    font_size = 10
    font_name = "helv"

    # Вставка ФИО в правый верхний угол каждой страницы (кроме обложки)
    for i, page in enumerate(doc):
        if i == 0:
            continue  # Пропускаем обложку
        text = name
        x = page.rect.width - 100
        y = 20
        page.insert_text((x, y), text, fontsize=font_size, fontname=font_name, color=(0, 0, 0), morph=None)

        # Вставка телефона в левый нижний угол
        phone_x = 20
        phone_y = page.rect.height - 20
        page.insert_text((phone_x, phone_y), phone, fontsize=font_size, fontname=font_name, color=(0, 0, 0), morph=None)

    # Водяной знак на каждой 5–10-й странице
    for i, page in enumerate(doc):
        if i < 1:
            continue
        if i % random.randint(5, 10) == 0:
            text = f"@{phone}"
            rect = page.rect
            x = rect.width / 4
            y = rect.height / 2
            page.insert_text(
                (x, y),
                text,
                fontsize=40,
                fontname=font_name,
                color=(0.85, 0.85, 0.85),  # светло-серый
                rotate=30,
                morph=None
            )

    # Генерация имени файла
    output_path = OUTPUT_DIR / f"{phone.replace('+', '')}_{name.replace(' ', '_')}.pdf"
    doc.save(output_path)
    doc.close()

    return str(output_path)
