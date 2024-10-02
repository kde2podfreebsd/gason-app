import requests
from amzqr import amzqr
import os

# def download_gif(url, save_path="temp.gif"):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(save_path, "wb") as f:
#             f.write(response.content)
#         print(f"GIF успешно загружен: {save_path}")
#     else:
#         raise Exception(f"Ошибка при загрузке GIF: {response.status_code}")

# gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3Z4eG4xbGp6ZjFxNW0za2thODdncWRpbmZ6OGVpMDRtcnlxMmdqcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT0BKiaM2VGJ553P9K/giphy.gif"
# local_gif = "temp.gif"
# data = "https://example.com"
# output_file = "output.gif"
# download_gif(gif_url, local_gif)
#
# amzqr.run(
#     data,
#     version=5,
#     level='H',
#     picture=local_gif,
#     colorized=True,
#     contrast=1.0,
#     brightness=1.0,
#     save_name=output_file,
#     save_dir="."
# )
#
# os.remove(local_gif)


def generate_qr_with_background(data, background_image, output_file):
    """
    Функция для создания QR-кода с фоновым изображением.

    :param data: Данные для кодирования в QR-код.
    :param background_image: Путь к локальному изображению для фона (png, jpg и т.д.).
    :param output_file: Путь для сохранения выходного QR-кода.
    """
    try:
        # Генерация QR-кода с фоновым изображением
        amzqr.run(
            data,
            version=20,               # Оптимальная версия QR-кода
            level='H',                # H = 30% коррекции ошибок
            picture=background_image, # Фон (путь к локальному изображению)
            colorized=True,           # Цветной QR-код
            contrast=1.0,             # Контрастность
            brightness=1.0,           # Яркость
            save_name=output_file,    # Имя файла для сохранения
            save_dir=".."  # Директория для сохранения
        )
        print(f"QR-код успешно создан и сохранён в {output_file}")
    except Exception as e:
        print(f"Ошибка при создании QR-кода: {e}")

# Пример использования функции
data = "https://example.com"
background_image = "bot/static/gason.jpg"  # Укажите путь к вашему локальному изображению
output_file = "qr_with_background.png"

generate_qr_with_background(data, background_image, output_file)

