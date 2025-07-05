from pathlib import Path
import fitz  # PyMuPDF
import random
import time

def generate_personal_pdf(name: str, phone: str) -> str:
    # Оригинал книги
    source_file = Path("files/book.pdf")

    # Уникальное имя файла
    timestamp = int(time.time())
    output_file = Path(f"files/generated_{phone}_{timestamp}.pdf")

    # Открываем PDF
    doc = fitz.open(source_file)

    # Добавляем ФИО и телефон на каждую страницу (кроме обложки)
    for i, page in enumerate(doc):
        if i == 0:
            continue  # пропускаем обложку

        # Вставка фамилии (в правый верхний угол)
        try:
            page.insert_text((400, 30), name, fontsize=8)
        except Exception as e:
            print(f"Ошибка вставки имени на стр. {i + 1}: {e}")

        # Вставка телефона (в левый нижний угол)
        try:
            page.insert_text((30, 800), phone, fontsize=8)
        except Exception as e:
            print(f"Ошибка вставки телефона на стр. {i + 1}: {e}")

    # Вставка водяного знака на каждую 5–10 страницу
    for i, page in enumerate(doc):
        if i == 0:
            continue
        if i % random.randint(5, 10) == 0:
            try:
                page.insert_text(
                    (150, 400),
                    f"📱 {phone}",
                    fontsize=20,
                    rotate=30,
                    color=(0.8, 0.8, 0.8),
                    render_mode=3,
                    morph=None,
                    overlay=True,
                )
            except Exception as e:
                print(f"Ошибка вставки водяного знака на стр. {i + 1}: {e}")

    doc.save(output_file)
    doc.close()

    return str(output_file)
