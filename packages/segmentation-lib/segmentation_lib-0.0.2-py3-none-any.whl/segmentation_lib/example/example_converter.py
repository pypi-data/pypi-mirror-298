from app.segmentation_lib import (
    delete_background, colored_to_black, black_to_colored
)


images_path = 'COVID'  # Папка с изображениями и цветными масками
result_path = 'result-COVID'

# Удаление фона
delete_background(images_path)

# Преобразование маски в черно-белую и пролучение словаря классов и цветов
colored_to_black(images_path, result_path)

# # Восстановление цветной маски из черно-белой
black_to_colored(result_path)
