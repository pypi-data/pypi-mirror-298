from PIL import Image
from PIL import ImagePalette
import numpy as np
import os
import json
import shutil


def generate_colors():
    """
    Функция для генерации списка цветов
    """
    initial_colors = [
        [0, 0, 0], [255, 255, 255], [255, 0, 0], [0, 255, 0], [0, 0, 255],
        [255, 255, 0], [255, 0, 255], [0, 255, 255], [128, 128, 128],
        [128, 0, 0], [0, 128, 0], [0, 0, 128], [128, 128, 0], [128, 0, 128],
        [0, 128, 128]
    ]

    # Генерация недостающих цветов
    step = 32
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                color = [r, g, b]
                if color not in initial_colors:
                    initial_colors.append(color)
                if len(initial_colors) == 256:
                    return initial_colors

    return initial_colors

def delete_background(images_path):
    images_dir = os.path.join(images_path, 'images')
    masks_dir = os.path.join(images_path, 'masks')
    save_dir = os.path.join(images_path, 'masks-no-background')

    # Создание папки для новых масок, если она не существует
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Проход по всем изображениям в папке
    for image_name in os.listdir(images_dir):
        # Полные пути к изображению и соответствующей маске
        image_path = os.path.join(images_dir, image_name)
        mask_path = os.path.join(masks_dir, image_name)

        # Проверка, что файл маски существует
        if not os.path.exists(mask_path):
            print(f"Маска для изображения {image_name} не найдена")
            continue

        # Открытие изображения и маски
        image = Image.open(image_path).convert('RGB')
        mask = Image.open(mask_path).convert('RGB')

        # Преобразование изображений в пиксельные массивы
        image_pixels = image.load()
        mask_pixels = mask.load()

        # Создание нового изображения для сохранения маски без фона
        mask_no_bg = Image.new('RGB', mask.size)
        mask_no_bg_pixels = mask_no_bg.load()

        # Проход по всем пикселям маски
        for y in range(mask.size[1]):
            for x in range(mask.size[0]):
                # Если пиксель маски отличается от пикселя изображения, сохраняем его
                if mask_pixels[x, y] != image_pixels[x, y]:
                    mask_no_bg_pixels[x, y] = mask_pixels[x, y]

        # Сохранение новой маски
        mask_no_bg.save(os.path.join(save_dir, image_name))


def resize_image_and_mask(image, mask, size=(512, 512)):
    """
    Сервисная функция для изменения размера изображения и маски до заданного размера.
    Используем метод NEAREST для маски, чтобы сохранить значения классов.
    """
    resized_image = image.resize(size,
                                 Image.Resampling.LANCZOS)  # Используем LANCZOS для улучшения качества изображения
    resized_mask = mask.resize(size,
                               Image.Resampling.NEAREST)  # Используем NEAREST для маски, чтобы сохранить значения классов
    return resized_image, resized_mask


def colored_to_black(images_path, save_path, target_size=(512, 512)):
    """
    Функция для перевода цветной маски в черно-белую и получения словаря цветов.
    Также изменяет размер изображений и масок до одного размера.
    """
    masks_dir = os.path.join(images_path, 'masks-no-background')  # Папка с масками без фона
    result_dir = os.path.join(save_path, 'masks')  # Папка для сохранения результата

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Копирование исходных изображений в папку с результатом
    images_source = os.path.join(images_path, 'images')
    images_destination = os.path.join(save_path, 'images')

    os.makedirs(images_destination, exist_ok=True)

    for filename in os.listdir(images_source):
        source_file = os.path.join(images_source, filename)
        destination_file = os.path.join(images_destination, filename)

        if os.path.isfile(source_file):  # Проверка является ли объект файлом
            image = Image.open(source_file)

            # Проверка на наличие маски с таким же именем
            mask_file = os.path.join(masks_dir, filename)
            if os.path.isfile(mask_file):
                mask = Image.open(mask_file)
            else:
                print(f"Mask for {filename} not found in {masks_dir}")
                continue

            # Изменение размера изображения и маски
            image, mask = resize_image_and_mask(image, mask, size=target_size)

            # Сохранение измененного изображения
            image.save(destination_file)

            # Сохранение измененной маски в папку result_dir
            mask_save_path = os.path.join(result_dir, filename)
            mask.save(mask_save_path)

    # Грубое квантование для округления цветов
    def quantize_color(color, factor=16):
        return tuple(
            (np.array(color)[:3] // factor * factor).astype(int))  # Используем только первые три канала (R, G, B)

    # Словарь для хранения цветов и их классов
    color_to_class = {}

    # Переменная для отслеживания следующего доступного индекса класса
    next_class_index = 0

    # Преобразуем изображения в черно-белые маски и сохраняем их
    for filename in os.listdir(masks_dir):
        mask_save_path = os.path.join(result_dir, filename)
        if not os.path.isfile(mask_save_path):
            print(f"Resized mask for {filename} not found, skipping.")
            continue

        color_image = Image.open(mask_save_path)

        # Убираем альфа-канал, если он существует
        if color_image.mode == 'RGBA':
            color_image = color_image.convert('RGB')

        color_image = np.array(color_image)

        # Применяем квантование цветов
        quantized_image = np.apply_along_axis(quantize_color, 2, color_image)

        # Собираем уникальные квантованные цвета и назначаем им классы
        colormap = np.unique(quantized_image.reshape(-1, quantized_image.shape[2]), axis=0)

        for color in colormap:
            color_tuple = tuple(color)
            if color_tuple not in color_to_class:
                color_to_class[color_tuple] = next_class_index
                next_class_index += 1

        # Пустое изображение для записи черно-белой маски
        mask = np.zeros((quantized_image.shape[0], quantized_image.shape[1]), dtype=np.uint8)

        # Применяем классы к маске
        for color, class_value in color_to_class.items():
            mask[(quantized_image == color).all(axis=2)] = class_value

        # Преобразуем обратно в изображение и сохраняем
        result = Image.fromarray(mask)
        result.save(mask_save_path)

    # Запись в options.json
    options_dict = {"background": 0}
    for value in color_to_class.values():
        if value != 0:
            options_dict[str(value)] = value

    options_file_path = os.path.join(save_path, "options.json")
    with open(options_file_path, 'w') as json_file:
        json.dump(options_dict, json_file, indent=4)


# def colored_to_black(images_path, save_path):
#     """
#     Функция для перевода цветной маски в черно-белую и получения словаря цветов
#     """
#     masks_dir = os.path.join(images_path, 'masks-no-background')   # Папка с масками без фона
#     result_dir = os.path.join(save_path, 'masks')         # Папка для сохранения результата
#
#     if not os.path.exists(result_dir):
#         os.makedirs(result_dir)
#
#     # Копирование исходных ихображений в папку с результатом
#     images_source = os.path.join(images_path, 'images')
#     images_destination = os.path.join(save_path, 'images')
#
#     os.makedirs(images_destination, exist_ok=True)
#
#     for filename in os.listdir(images_source):
#         source_file = os.path.join(images_source, filename)
#         destination_file = os.path.join(images_destination, filename)
#
#         if os.path.isfile(source_file):  # Проверка является ли объект файлом
#             shutil.copy2(source_file, destination_file)
#
#     # Грубое квантование для округления цветов
#     def quantize_color(color, factor=16):
#         return tuple((np.array(color)[:3] // factor * factor).astype(int))  # Используем только первые три канала (R, G, B)
#
#
#     # Словарь для хранения цветов и их классов
#     color_to_class = {}
#
#     # Переменная для отслеживания следующего доступного индекса класса
#     next_class_index = 0
#
#     for filename in os.listdir(masks_dir):
#         image_path = os.path.join(masks_dir, filename)
#         color_image = Image.open(image_path)
#
#         # Убираем альфа-канал, если он существует
#         if color_image.mode == 'RGBA':
#             color_image = color_image.convert('RGB')
#
#         color_image = np.array(color_image)
#
#         # Применяем квантование цветов
#         quantized_image = np.apply_along_axis(quantize_color, 2, color_image)
#
#         # Собираем уникальные квантованные цвета и назначаем им классы
#         colormap = np.unique(quantized_image.reshape(-1, quantized_image.shape[2]), axis=0)
#
#         for color in colormap:
#             color_tuple = tuple(color)
#             if color_tuple not in color_to_class:
#                 color_to_class[color_tuple] = next_class_index
#                 next_class_index += 1
#
#     # Преобразуем изображения обратно в черно-белые маски
#     for filename in os.listdir(masks_dir):
#         image_path = os.path.join(masks_dir, filename)
#         image_save_path = os.path.join(result_dir, filename)
#
#         color_image = Image.open(image_path)
#
#         # Убираем альфа-канал, если он существует
#         if color_image.mode == 'RGBA':
#             color_image = color_image.convert('RGB')
#
#         color_image = np.array(color_image)
#
#         # Применяем квантование к изображению
#         quantized_image = np.apply_along_axis(quantize_color, 2, color_image)
#
#         # Пустое изображение для записи черно-белой маски
#         mask = np.zeros((quantized_image.shape[0], quantized_image.shape[1]), dtype=np.uint8)
#
#         # Применяем классы к маске
#         for color, class_value in color_to_class.items():
#             mask[(quantized_image == color).all(axis=2)] = class_value
#
#         # Преобразуем обратно в изображение и сохраняем
#         result = Image.fromarray(mask)
#         result.save(image_save_path)
#
#     # Запись в options.json
#     options_dict = {"background": 0}
#     for value in color_to_class.values():
#         if value != 0:
#             options_dict[str(value)] = value
#
#     options_file_path = os.path.join(save_path, "options.json")
#     with open(options_file_path, 'w') as json_file:
#         json.dump(options_dict, json_file, indent=4)



def black_to_colored(images_path):
    """
    Функция для перевода цветной маски в черно-белую и получения словаря цветов
    """
    masks_dir = os.path.join(images_path, 'masks')  # Папка с черными масками

    # Генерируем список уникальных цветов
    colormap = generate_colors()

    # Создаем словарь цветов
    unique_values = set()   # Множество для хранения уникальных значений пикселей
    for filename in os.listdir(masks_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            filepath = os.path.join(masks_dir, filename)
            with Image.open(filepath) as img:
                img = img.convert('L')
                pixels = img.getdata()
                unique_values.update(pixels)

    # Создаем словарь colormap
    class_dict = {value: colormap[value] for value in unique_values}

    print('class_dict:')
    print(class_dict)

    # Создаем директорию для сохранения результата
    result_dir = os.path.join(images_path, 'masks-colored')     # Папка для сохранения результата
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for filename in os.listdir(masks_dir):
        image_path = os.path.join(masks_dir, filename)
        save_path = os.path.join(result_dir, filename)

        mask = Image.open(image_path)
        mask = np.array(mask)

        # Пустое изображение для записи
        color_image = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

        # Применяем цвета к маске
        for class_value, color in class_dict.items():
            color_image[mask == class_value] = color

        # Преобразуем обратно в изображение и сохраняем
        result = Image.fromarray(color_image)
        result.save(save_path)
