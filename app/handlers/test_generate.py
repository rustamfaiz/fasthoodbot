from utils.pdf_generator import generate_personal_pdf

if __name__ == "__main__":
    input_path = "files/тест книги.pdf"  # оригинальный файл
    output_path = "files/output_test.pdf"  # сгенерированный файл
    full_name = "Иванов Иван"
    phone_number = "+7 900 123-45-67"

    generate_personal_pdf(input_path, output_path, full_name, phone_number)
    print("✅ Генерация завершена. Файл сохранён:", output_path)
