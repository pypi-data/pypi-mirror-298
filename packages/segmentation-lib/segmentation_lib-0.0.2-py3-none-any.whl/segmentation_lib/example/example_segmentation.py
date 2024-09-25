from pathlib import Path
from PIL import Image
import os
import torch
import optuna

from app.segmentation_lib import (
    optimization, segm_train, rastr_to_array, segm_test, check_pickling, segm_save_model, segm_load_model, segm_predict
)


# DATA_PATH = Path('car-segmentation-short')
# DATA_PATH = Path('result-road-segmentation')
# DATA_PATH = Path('result-flood_example')
# DATA_PATH = Path('result-my-dataset')
DATA_PATH = Path('result-COVID')

print(torch.cuda.is_available())
print(torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(torch.cuda.get_device_name(i))

"""### Пример запуска обучения(используются не все параметры)"""

path_to_dataset = DATA_PATH
predict_result_path = f'{path_to_dataset}/launch_examples/predict_mode_example'
save_result_path = f'{path_to_dataset}/launch_examples/save_mode_example'

# Создаем директории для сохранения результата
if not os.path.exists(predict_result_path):
    # Создаем папку
    os.makedirs(predict_result_path)
if not os.path.exists(save_result_path):
    # Создаем папку
    os.makedirs(save_result_path)

study = optuna.create_study(direction="maximize")
study.optimize(optimization, n_trials=50)  # n_trials - количество проб

print("Лучшие гиперпараметры: ", study.best_params)
print("Лучшее значение метрики IoU: ", study.best_value)

# Задаем лучшие гиперпараметры для обучения
best_params = study.best_params

train_config = {
    # для корректной работы лучше указывать полный путь
    'path_to_dataset': path_to_dataset,
    'imgsz': 224,
    'device': 'cuda:0',  # cuda:0',
    'num_workers': best_params['num_workers'],  # increase this if need faster training.
    'batch_size': best_params['batch_size'],    #16
    'epochs': best_params['epochs'],            #5
    'metric': 'IoU',
    'lr': best_params['lr'],                    #0.001
    'loss': 'focal',
    'optimizer': best_params['optimizer'],
    'model': 'deeplabv3_resnet50',
    'VerticalFlip': best_params['VerticalFlip'],
    'HorizontalFlip': best_params['HorizontalFlip'],
    'scale_limit': [best_params['scale_limit'], -best_params['scale_limit']],
    'rotate_limit': best_params['rotate_limit'],
    'blur': best_params['blur']
}

# train_config = {
#     # для корректной работы лучше указывать полный путь
#     'path_to_dataset': path_to_dataset,
#     'imgsz': 224,
#     'device': 'cpu',  # cuda:0',
#     'num_workers':0,# increase this if need faster training.
#     'batch_size': 16,#16
#     'epochs': 5,#5,
#     'metric': 'IoU',
#     'lr': 0.001,#0.001
#     'loss': 'focal',
#     'model': 'deeplabv3_resnet50',
#     'scale_limit':[-0.4,0.4]
# }

model, train_results, gui_dict = segm_train(**train_config)

"""### Изображения, показывающие преобразования данных при обучении модели."""

for i in gui_dict['image']:
    pic = i['value']
    pic = rastr_to_array(pic)
    Image.fromarray(pic).show()

"""### Пример запуска тестирования"""

test_config = {
    'imgsz': 224,
    'num_workers': 0,
    'metric': 'IoU',
    'loss': 'focal',
    'device': 'cuda:0',
    'path_to_dataset': path_to_dataset,
}
gd = segm_test(model, **test_config)

"""### Примеры предиктов на тесте"""

for i in gd['image']:
    pic = i['value']
    pic = rastr_to_array(pic)
    Image.fromarray(pic).show()

check_pickling(model,path_to_dataset)#if ended without errors, pickling works

path_to_save_model = f'{save_result_path}/model.pt'
segm_save_model(model, path_to_save_model)

loaded_model = segm_load_model(path_to_save_model)

segm_predict(loaded_model, path_to_images=f"{path_to_dataset}/images", path_to_options=f'{path_to_dataset}/options.json',
             path_to_save_results=predict_result_path, device='cuda:0')
