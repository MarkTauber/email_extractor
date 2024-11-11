import os
import re
import codecs
from sys import argv
import threading
import datetime

time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
LOG_FILE = f"[{time}]_LOG.log"  # Имя файла логов
output_filename = f"[{time}]_FOUND.txt"

def extract_emails(fpath, extensions):
    if extensions and not any(fpath.endswith(ext) for ext in extensions):
        return
    
    encodings = ["utf-8", "latin-1", "koi8-r", "windows-1251", "ascii", "cp1251", "utf-16", "utf-32", "iso-8859-1"] # Пробуем разные кодировки

    for encoding in encodings:
        try:
            with open(fpath, 'r', encoding=encoding) as f:
                with codecs.open(output_filename, "a", encoding="utf-8") as mail_file:
                    for line in f:
                        emails = re.findall(
                            r'(?:\.?)([\w\-_+#~!$&\'\.]+(?<!\.)(@|[ ]\(?[ ]?(at|AT)[ ]?\)?[ ])(?<!\.)[\w]+[\w\-\.]*\.[a-zA-Z-]{2,5})(?:[^\w])',
                            line,
                        )
                        if emails:
                            for email in emails:
                                cleaned_email = re.sub(r'[><;\'"%?&]', '', email[0])
                                print(f"{fpath}: {cleaned_email}")
                                mail_file.write(cleaned_email + "\n")
                                
                                # Запись в лог-файл
                                with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                                    log_file.write(f"Найден email: {cleaned_email} в файле: {fpath}\n")
            return  

        except UnicodeDecodeError:
            pass  # Пропускаем кодировку, если декодировка не удалась

    print(f"Не удалось определить кодировку файла {fpath}.")

def process_path(path, extensions):
    if os.path.isdir(path):
        print(f"Обработка папки: {path}")
        for root, _, files in os.walk(path):
            for filename in files:
                fpath = os.path.join(root, filename)
                process_file(fpath, extensions)
    elif os.path.isfile(path):
        print(f"Обработка файла: {path}")
        extract_emails(path, extensions)
    else:
        print(f"Неверный путь: {path}")

def process_file(fpath, extensions):
    print(f"Обработка файла: {fpath}")
    extract_emails(fpath, extensions)

if __name__ == "__main__":
    if len(argv) < 2:
        print("Необходимо указать путь к файлу или папке.")
        exit()

    path = argv[1]
    extensions = argv[2:] if len(argv) > 2 else None

    # Очистка лог-файла перед запуском
    with open(LOG_FILE, "w", encoding="utf-8") as log_file:
        log_file.write("")  # Очистка содержимого

    process_path(path, extensions)

    os.system("pause")