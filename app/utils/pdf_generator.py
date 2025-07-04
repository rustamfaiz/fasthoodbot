import fitz  # PyMuPDF
import random

def generate_personal_pdf(input_path: str, output_path: str, full_name: str, phone_number: str):
    print("📄 Запущен генератор PDF")  # лог
    print(f"📥 Входной файл: {input_path}")
    print(f"📤 Выходной файл: {output_path}")
    print(f"👤 Имя: {full_name}")
    print(f"📞 Телефон: {phone_number}")

    try:
        doc = fitz.open(input_path)

        for i, page in enumerate(doc):
            # Пропускаем обложку
            if i == 0:
                continue

            # ФИО — правый верхний угол
            page.insert_text(
                (page.rect.width - 120, 20),
                full_name,
                fontsize=8,
                color=(0, 0, 0),
            )

            # Телефон — левый нижний угол
            page.insert_text(
                (20, page.rect.height - 20),
                phone_number,
                fontsize=8,
                color=(0, 0, 0),
            )

            # Водяной знак — раз в 5–10 страниц
            if i % random.randint(5, 10) == 0:
                page.insert_textbox(
                    page.rect,
                    phone_number,
                    fontsize=40,
                    color=(0.9, 0.9, 0.9),
                    rotate=90,  # 🔧 исправлено
                    align=1,
                    overlay=True
                )

        doc.save(output_path)
        doc.close()
        print("✅ PDF успешно сохранён")
        return output_path

    except Exception as e:
        print(f"❌ Ошибка в генерации PDF: {e}")
        return None
