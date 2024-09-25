import plotly
import json
import plotly.graph_objects as go
from PIL import Image
from PIL import ImagePalette

import numpy as np
import os
import io
import base64
import torch
from torch.nn import functional as F
from torch.utils.data import Dataset as torch_dataset
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
from torch import nn
import torchvision
from torchvision.transforms.functional import to_tensor
from torchvision.utils import save_image

import tqdm
from typing import Union, Tuple, List
import albumentations as A
from albumentations import Resize
from warnings import warn
from copy import deepcopy
import glob

import dill
import optuna

def draw_plot(plots: list):
    for plot in plots:

        print(plot['window_title'])

        plot_dict = json.loads(plot['fig'])
        dict_of_fig = dict({
            "data": plot_dict['data'],
            "layout": plot_dict['layout']
        })

        fig = go.Figure(dict_of_fig)

        fig.show()

def rastr_to_array(rastr: str):
    '''
    Конвертирует изображение из растрового формата в массив
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import numpy as np
        from PIL import Image
        import base64
        import io


    '''
    label_bytes = base64.b64decode(rastr)
    label = Image.open(io.BytesIO(label_bytes))
    label = np.array(label)
    return label

def segm_train(path_to_dataset: str,
               save_results_path: str = 'default',
               save_model_path: str = 'default',
               imgsz: int = 224,
               model: str = 'unet',
               device: str = 'cpu',
               metric: str = 'IoU',
               num_workers: int = 5,
               batch_size: int = 16,
               epochs: int = 100,
               loss: str = 'focal',
               optimizer: str = 'AdamW',
               lr: float = 0.001,
               VerticalFlip: float = 0.05,
               HorizontalFlip: float = 0.5,
               GaussNoise:  Union[List[float], Tuple[float]] = [0.0001, 0.001],
               shift_limit: float = 0.1625,
               scale_limit: Union[List[float], Tuple[float]] = [-0.4, 0.4],
               rotate_limit: int = 30,
               blur: float = 0.5,
               OneOf_Sharpen_Emboss_RandomBrightnessContrast: float = 0.5,
               HueSaturationValue: float = 0.5,
               ) -> torch.nn.Module:
    """
    Segmentation training pipeline

    :code_assign: users
    :code_type: Глубокое обучение/Сегментация(обучение)
    :imports: load_classes_dict, create_train_dataloaders, load_params, mask_cvtr, apply_augm_to_sinle_image, ResultsVisualizer, apply_augm_to_batch, get_probabilities


    :packages:
        # Пакеты, используемые в процессе обучения
        import os
        import numpy as np
        import torch
        import tqdm


    :param str path_to_dataset: path to dataset folder. Dataset must contain folders: images, masks. Also in this path must be file options.json
    :param str save_results_path: Path to save train results.  Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру
    :param str save_model_path: Path to save model in process of training. Defaults to 'default'(bin folder in library). Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру
    :param str device: Name of device for training. Possible values 'cpu', 'cuda:0', 'cuda:1', etc. Defaults to 'cpu'. Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру
    :param int num_workers: Num workers in DataLoader. Defaults to 5. Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру

    :param int imgsz: Size of images for model input. Defaults to 224
    :param str model: Name of model to train. Must be one of ['unet', 'segnet']. Defaults to 'unet'.
    :param str metric: Name of metric to score model. Possible values: 'IoU',dice. Defaults to IoU'
    :param int batch_size: Batch size for training. Defaults to 16.
    :param str optimizer: name of optimizer. Possible values: 'AdamW', 'SGD', 'RMSprop', 'Adadelta', 'Adagrad', 'Adam'. Defaults to 'AdamW'.
    :param int epochs: Number of epochs in train. Defaults to 100.
    :param str loss: name of loss function. Possible values: 'dice', 'focal', 'cel'. Defaults to 'focal'.
    :param float lr: learning rate in optimizer. Defaults to 0.001.
    :param float VerticalFlip: Probability of vertical flip augmentation. Defaults to 0.05.
    :param float HorizontalFlip: Probability of horizontal flip augmentation. Defaults to 0.5.
    :param Union[list, tuple] scale_limit: Scale limit parameter in augmentation. Defaults to [-0.4, 0.4].
    :param int rotate_limit: degree in rotation augmentation. Defaults to 30.
    :param int shift_limit: max value for image shifting(fracture). Defaulta to 0.1625,
    :param float blur: Probability of blur augmentation. Defaults to 0.5.
    :param float OneOf_Sharpen_Emboss_RandomBrightnessContrast: Probability of applying one of Sharpen|Emboss|RandomBrightnessContrast augmentation. Defaults to 0.5.
    :param Union[list, tuple] GaussNoise: var_limit in Gaussian noise augmentation. Defaults to [0.0001, 0.001]
    :param float HueSaturationValue: probability of HueSaturationValue augmentation. Defaults to 0.5

    :returns: model, gui_dict
    :rtype: torch.nn.Module, dict
    :semrtype: torch.nn.Module,
    """
    print('Train mode is enabled')
    img_path_to_dataset = os.path.join(path_to_dataset, 'images')
    mask_path_to_dataset = os.path.join(path_to_dataset, 'masks')
    path_to_classes_dict = os.path.join(path_to_dataset, 'options.json')

    config = locals()  # converting all input parameters to dict
    config['mode'] = 'train'

    config['classes_dict'] = load_classes_dict(path_to_classes_dict)

    print("Initializing Dataloaders...")
    data_tr, data_val, dataset = create_train_dataloaders(config)
    config['dataloader'] = data_tr
    tr_len = len(data_tr)
    print('Dataloaders are initialized..')

    train_params = load_params(config)

    epochs = train_params['epochs']
    device = train_params['device']
    loss_fn = train_params['loss']
    model = train_params['model']
    opt = train_params['optimizer']
    augms = train_params['augmentation']

    scheduler = None
    metric = train_params['metric']

    classes_dict = config['classes_dict']
    mask2id_cvtr = dict([(value, i)
                         for i, (key, value) in enumerate(classes_dict.items())])  # dict for converting values. Looks like {'batch_index':'class_id'}

    classes_amount = len(classes_dict.keys())
    loss_name = config['loss']
    metric_name = config['metric']

    save_path = train_params['save_results_path']
    PATH_BEST_MODEL = train_params['save_model_path']+'/best_model.pth'
    visualizer = ResultsVisualizer(config, save_path)

    # make train_examples in format (orig_img, orig_mask,aug_img,aug_mask)
    train_examples = []

    for i in np.random.choice(len(dataset), 5, replace=False):
        pic = dataset[i][0]
        # all pixels values makes in order of 0 1 2 3 4..
        mask = mask_cvtr(dataset[i][1], mask2id_cvtr)
        aug_pic, aug_mask = apply_augm_to_sinle_image(pic, mask, augms)
        train_examples.append([pic, mask, aug_pic, aug_mask])
    train_examples_paths = visualizer.save_train_examples(*train_examples)
    print('Train examples are created.. Format: rows: img,mask. columns: orig,aug ')

    # each verb_period iter update verbose in train pipline
    verb_period = max(1, tr_len // 100)

    train_loss = []
    train_scores = []
    eval_loss = []
    val_scores = []

    model.to(device)
    best_score = -1
    print('Train instruments are created..')

    print("Starting train...")
    for epoch in range(epochs):

        sum_loss = 0
        sum_score = 0

        model.train()  # train mode
        verb_prefix = 'Epoch %d/%d' % (epoch+1, epochs)

        batch_index = 0
        pbar = tqdm.tqdm(data_tr, desc=verb_prefix)
        for X_batch, mask_batch in pbar:

            batch_index += 1
            X_batch, mask_batch = apply_augm_to_batch(
                X_batch, mask_batch, augms)
            X_batch = X_batch.to(device)
            mask_batch = mask_cvtr(mask_batch, mask2id_cvtr)
            mask_batch = mask_batch.to(torch.int64).to(device)

            # set parameter gradients to zero
            opt.zero_grad()

            # forward
            logits = model.forward(X_batch)  # forward-pass
            Y_pred = get_probabilities(logits)
            loss = loss_fn(Y_pred, mask_batch)

            sum_score += metric(Y_pred.argmax(dim=1),
                                mask_batch).detach().cpu().mean()
            loss.backward()  # backward-pass
            opt.step()  # update weights
            # calculate loss to show the user

            sum_loss += loss.detach().cpu()
            current_score = sum_score.item() / batch_index
            if batch_index % verb_period == 0:
                pbar.set_description(
                    f'{verb_prefix} train: loss({loss_name}):{round(sum_loss.item()/batch_index,3)}, score({metric_name}):{round(current_score,3)} ')

        if scheduler is not None:
            scheduler.step()  # update lr

        train_scores.append(current_score)

        # Validation
        model.eval()
        avg_val_loss = 0
        score = 0
        with torch.no_grad():
            for X_val, mask_val in data_val:
                X_val = X_val.to(device)

                # Y_val = mask_to_Y(mask_val, classes_dict,
                #                   classes_amount).to(device)

                mask_val = mask_cvtr(mask_val, mask2id_cvtr)
                mask_val = mask_val.to(torch.int64).to(device)
                logits = model(X_val)
                Y_pred = get_probabilities(logits)

                loss = loss_fn(Y_pred, mask_val)
                avg_val_loss += loss.detach().cpu() / len(data_val)
                # calculate score
                score += metric(Y_pred.argmax(dim=1),
                                mask_val).detach().cpu() / len(data_val)
            print(
                f'     val: loss({loss_name}): {round(avg_val_loss.item(),3)}, score({metric_name}): {round(score.item(),3)}')
            eval_loss.append(avg_val_loss.item())
            val_scores.append(score.item())
        if score.item() > best_score:
            # save best model
            best_score = score.item()
            torch.save(model.state_dict(), PATH_BEST_MODEL)
        train_loss.append(sum_loss.item()/batch_index)  # adding avg train loss

    train_results = {'train_loss': train_loss, 'train_scores': train_scores,
                     'val_loss': eval_loss, 'val_scores': val_scores, "train_examples_paths": train_examples_paths,
                     'class_counter': config['class_counter'],
                     }

    gui_dict = visualizer.get_train_gui_dict(train_results)

    # loading best model
    model.load_state_dict(torch.load(PATH_BEST_MODEL))
    return model, train_results, gui_dict

def mask_cvtr(mask_batch, cvtr):
    """
    Конвертирует набор масок в новый набор масок.
    Маски конвертируются согласно cvtr = {old_pixel_value:new_pixel_value}
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
    """
    for key, to in cvtr.items():
        mask_batch[mask_batch == key] = to
    return mask_batch

def load_classes_dict(file_path: str) -> dict:
    '''
    Load classes dictionary from json

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import json

    :param str filename: json path to classes dictionary

    '''
    with open(file_path) as file:
        classes_dict = json.load(file)
    # Дополниельно отсортируем по значению пикселя
    classes_dict = dict(
        sorted(classes_dict.items(), key=lambda x: x[1]))

    return classes_dict

def create_train_dataloaders(config: dict):
    """
    Создает даталоадеры для обучения.

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :packages:
        import albumentations as A
        from albumentations import Resize
        import numpy as np
        from torch.utils.data import DataLoader
        from torch.utils.data.sampler import SubsetRandomSampler
    :param dict config: конфигурация создания даталоадера.

    """
    num_workers = int(config['num_workers'])
    size = config['imgsz']
    resize = A.Compose([Resize(size, size)])
    batch_size = int(config['batch_size'])

    dataset = SegmDataset(
        config['img_path_to_dataset'], config['mask_path_to_dataset'], config['classes_dict'], augms=resize)
    im_limit = len(dataset)

    # Data splitting
    ix = np.random.choice(im_limit, im_limit, False)
    train_indices, val_indices = ix[:int(
        im_limit*0.9)], ix[int(im_limit*0.9):]

    train_sampler = SubsetRandomSampler(train_indices)
    valid_sampler = SubsetRandomSampler(val_indices)

    train_loader = DataLoader(dataset, batch_size=batch_size,
                              sampler=train_sampler, num_workers=num_workers)
    valid_loader = DataLoader(dataset, batch_size=batch_size,
                              sampler=valid_sampler, num_workers=num_workers)

    return train_loader, valid_loader, dataset

def load_params(config: dict) -> dict:
    """
    get_train_params load train params from config and returns it.
    Config params: optimizer, loss, etc.

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :param dict config: train config


    :packages:
        import torch

    Returns:
        dict: instances of classes like nn.torch.optim, int(for batch_size, for example) etc.

    """

    config['classes_amount'] = len(config['classes_dict'].keys())

    params = config.copy()
    mode = params['mode']  # 'train','test' or 'predict'

    params['device'] = torch.device(config['device'])
    if mode == 'predict':
        return params
    params['save_results_path'] = load_path(config['save_results_path'])

    if mode == 'train' or mode == 'test':  # calculating classes stats in dataset
        pix_stats = DatasetPixelStats(
            config['classes_dict'], config['dataloader'])
        config['classes_freq'] = pix_stats.get_pixels_frequency()
        config['class_counter'] = pix_stats.get_pixels_count()

    params['loss'] = load_loss(
        config['loss'], config['classes_amount'], config['classes_freq'])
    params['batch_size'] = int(config['batch_size'])
    params['metric'] = load_metric(config['metric'], config['classes_amount'])
    params['num_workers'] = int(config['num_workers'])

    if mode == 'train':
        params['save_model_path'] = load_path(config['save_model_path'])
        params['model'] = segm_init_model(config)

        # params['scheduler'] = load_scheduler(
        #     config['scheduler'], params['optimizer'], params['epochs'])
        params['lr'] = float(config['lr'])
        params['epochs'] = int(config['epochs'])
        params['optimizer'] = load_optimizer(
            config['optimizer'], params['lr'], params['model'])
        params['augmentation'] = load_augmentation(config)
    return params

def load_augmentation(aug_config: dict):
    '''
    Returns augmentations from given configuration
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import albumentations as A
    :param dict aug_config: configuration for augmentation

    '''
    heavy_transforms = A.Compose([A.VerticalFlip(p=aug_config['VerticalFlip']),
                                  A.HorizontalFlip(
                                      p=aug_config['HorizontalFlip']),

                                  A.GaussNoise(
                                      var_limit=aug_config['GaussNoise']),
                                  A.ShiftScaleRotate(
        shift_limit=aug_config['shift_limit'], scale_limit=aug_config['scale_limit'], rotate_limit=aug_config['rotate_limit'], p=0.7),  # Если нужно, чтобы пространство заполнялось нулями ставим border_mode=cv2.BORDER_CONSTANT
        A.OneOf([
            A.MotionBlur(blur_limit=3, p=0.1),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
        ], p=aug_config['blur']),
        A.OneOf([
            A.Sharpen(),
            A.Emboss(),
            A.RandomBrightnessContrast(),
        ], p=aug_config['OneOf_Sharpen_Emboss_RandomBrightnessContrast']),
        A.HueSaturationValue(p=aug_config['HueSaturationValue'], hue_shift_limit=0.1,
                             sat_shift_limit=0.1, val_shift_limit=0.1),
        # A.Normalize(),
    ], p=0.99)
    return heavy_transforms

def load_optimizer(optim_name: str, lr: float, model: torch.nn.Module, *args) -> torch.optim:
    '''
    Returns optimizer from given parameters: optimizer name, learning rate, model

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch

    :param str optim_name: name of optimizer
    :param float learning_rate: learning rate
    :param torch.nn.Module model: model

    '''
    if optim_name == 'AdamW':
        return torch.optim.AdamW(model.parameters(), lr=lr)
    elif optim_name == 'SGD':
        return torch.optim.SGD(model.parameters(), lr=lr)
    elif optim_name == 'RMSprop':
        return torch.optim.RMSprop(model.parameters(), lr=lr)
    elif optim_name == 'Adadelta':
        return torch.optim.Adadelta(model.parameters(), lr=lr)
    elif optim_name == 'Adagrad':
        return torch.optim.Adagrad(model.parameters(), lr=lr)
    elif optim_name == 'Adam':
        return torch.optim.Adam(model.parameters(), lr=lr)
    else:
        raise ValueError("Uncorrect optimizer input")

def segm_init_model(config: dict):
    '''
    Returns model from given configuration

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torchvision

    :param dict config: model configuration
    '''
    model_name = config['model'].lower()  # model name
    classes_amount = len(config['classes_dict'].keys())
    if model_name == 'unet':
        return UNet(3, classes_amount)

    elif model_name == 'segnet':
        return SegNet(3, classes_amount)
    elif model_name == 'unet16':
        return UNet16(num_classes=classes_amount, pretrained=True)
    elif model_name in ['deeplabv3_resnet50', 'lraspp_mobilenet_v3_large']:  # torchvision models
        return ModelWrapper(model_name, classes_amount)
    else:
        raise ValueError(f"Uncorrect model_name input: {model_name}")

class ModelWrapper(torch.nn.Module):
    '''
    Wrapper for torchvision models output

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :packages:
        import torch
        import torchvision
    :param torch.nn.Module model: model to wrap
    '''

    def __init__(self, model_name, num_classes):
        super().__init__()
        if model_name == 'deeplabv3_resnet50':
            self.model = torchvision.models.segmentation.deeplabv3_resnet50(
                num_classes=num_classes)
        elif model_name == 'lraspp_mobilenet_v3_large':
            self.model = torchvision.models.segmentation.lraspp_mobilenet_v3_large(
                num_classes=num_classes)

    def forward(self, X):
        return self.model.forward(X)['out']

class UNet16(nn.Module):
    """
    Unet implementation with vgg16 backbone
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: ConvRelu, Interpolate, DecoderBlockV2

    :packages:
        import torchvision
        from torch import nn
        import torch

    """

    def __init__(
        self,
        num_classes: int = 1,
        num_filters: int = 32,
        pretrained: bool = False,
        is_deconv: bool = False,
    ):

        # Args:
        #     num_classes:
        #     num_filters:
        #     pretrained:
        #         False - no pre-trained network used
        #         True - encoder pre-trained with VGG16
        #     is_deconv:
        #         False: bilinear interpolation is used in decoder
        #         True: deconvolution is used in decoder

        super().__init__()
        self.num_classes = num_classes

        self.pool = nn.MaxPool2d(2, 2)

        self.encoder = torchvision.models.vgg16(pretrained=pretrained).features

        self.relu = nn.ReLU(inplace=True)

        self.conv1 = nn.Sequential(
            self.encoder[0], self.relu, self.encoder[2], self.relu
        )

        self.conv2 = nn.Sequential(
            self.encoder[5], self.relu, self.encoder[7], self.relu
        )

        self.conv3 = nn.Sequential(
            self.encoder[10],
            self.relu,
            self.encoder[12],
            self.relu,
            self.encoder[14],
            self.relu,
        )

        self.conv4 = nn.Sequential(
            self.encoder[17],
            self.relu,
            self.encoder[19],
            self.relu,
            self.encoder[21],
            self.relu,
        )

        self.conv5 = nn.Sequential(
            self.encoder[24],
            self.relu,
            self.encoder[26],
            self.relu,
            self.encoder[28],
            self.relu,
        )

        self.center = DecoderBlockV2(
            512, num_filters * 8 * 2, num_filters * 8, is_deconv
        )

        self.dec5 = DecoderBlockV2(
            512 + num_filters * 8, num_filters * 8 * 2, num_filters * 8, is_deconv
        )
        self.dec4 = DecoderBlockV2(
            512 + num_filters * 8, num_filters * 8 * 2, num_filters * 8, is_deconv
        )
        self.dec3 = DecoderBlockV2(
            256 + num_filters * 8, num_filters * 4 * 2, num_filters * 2, is_deconv
        )
        self.dec2 = DecoderBlockV2(
            128 + num_filters * 2, num_filters * 2 * 2, num_filters, is_deconv
        )
        self.dec1 = ConvRelu(64 + num_filters, num_filters)
        self.final = nn.Conv2d(num_filters, num_classes, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        conv1 = self.conv1(x)
        conv2 = self.conv2(self.pool(conv1))
        conv3 = self.conv3(self.pool(conv2))
        conv4 = self.conv4(self.pool(conv3))
        conv5 = self.conv5(self.pool(conv4))

        center = self.center(self.pool(conv5))

        dec5 = self.dec5(torch.cat([center, conv5], 1))

        dec4 = self.dec4(torch.cat([dec5, conv4], 1))
        dec3 = self.dec3(torch.cat([dec4, conv3], 1))
        dec2 = self.dec2(torch.cat([dec3, conv2], 1))
        dec1 = self.dec1(torch.cat([dec2, conv1], 1))
        return self.final(dec1)

class ConvRelu(nn.Module):
    """
    Convolution + ReLU block
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: conv3x3

    :packages:
        import torchvision
        from torch import nn
        import torch

    """

    def __init__(self, in_: int, out: int) -> None:
        super().__init__()
        self.conv = conv3x3(in_, out)
        self.activation = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv(x)
        x = self.activation(x)
        return x

def conv3x3(in_: int, out: int) -> nn.Module:
    '''
    Conv 2d with kernel 3x3 size

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        from torch import nn

    :param str filename: json path to classes dictionary

    '''
    return nn.Conv2d(in_, out, 3, padding=1)

class DecoderBlockV2(nn.Module):
    """
    Sec version for decoder block
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: ConvRelu, Interpolate

    :packages:
        from torch import nn
        import torch

    """

    def __init__(
        self,
        in_channels: int,
        middle_channels: int,
        out_channels: int,
        is_deconv: bool = True,
    ):
        super().__init__()
        self.in_channels = in_channels

        if is_deconv:
            """
            Paramaters for Deconvolution were chosen to avoid artifacts, following
            link https://distill.pub/2016/deconv-checkerboard/
            """

            self.block = nn.Sequential(
                ConvRelu(in_channels, middle_channels),
                nn.ConvTranspose2d(
                    middle_channels, out_channels, kernel_size=4, stride=2, padding=1
                ),
                nn.ReLU(inplace=True),
            )
        else:
            self.block = nn.Sequential(
                Interpolate(scale_factor=2, mode="bilinear"),
                ConvRelu(in_channels, middle_channels),
                ConvRelu(middle_channels, out_channels),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)

class Interpolate(nn.Module):
    """
    Interpolation convolution
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports:

    :packages:
        from torch import nn
        import torch

    """

    def __init__(
        self,
        size: int = None,
        scale_factor: int = None,
        mode: str = "nearest",
        align_corners: bool = False,
    ):
        super().__init__()
        self.interp = nn.functional.interpolate
        self.size = size
        self.mode = mode
        self.scale_factor = scale_factor
        self.align_corners = align_corners

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.interp(
            x,
            size=self.size,
            scale_factor=self.scale_factor,
            mode=self.mode,
            align_corners=self.align_corners,
        )
        return x


class SegNet(nn.Module):
    """
        SegNet model implementation
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports:

        :packages:
            from torch import nn
    """

    def __init__(self, input_channels=3, out_channels=1, features=32):
        super().__init__()

        start_channels = features
        self.enc_conv0 = nn.Sequential(
            nn.Conv2d(input_channels, start_channels,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels, start_channels,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels),  # !
            nn.ReLU(),
        )
        self.pool0 = nn.MaxPool2d(
            kernel_size=2, stride=2, return_indices=True)  # 256 -> 128
        self.enc_conv1 = nn.Sequential(
            nn.Conv2d(start_channels, start_channels*2,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*2),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*2, start_channels*2,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*2),  # !
            nn.ReLU(),
        )
        self.pool1 = nn.MaxPool2d(
            kernel_size=2, stride=2, return_indices=True)  # 128 -> 64
        self.enc_conv2 = nn.Sequential(
            nn.Conv2d(start_channels*2, start_channels*4,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*4),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*4, start_channels*4,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*4),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*4, start_channels*4,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*4),  # !
            nn.ReLU(),
        )
        self.pool2 = nn.MaxPool2d(
            kernel_size=2, stride=2, return_indices=True)  # 64 -> 32
        self.enc_conv3 = nn.Sequential(
            nn.Conv2d(start_channels*4, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
        )
        self.pool3 = nn.MaxPool2d(
            kernel_size=2, stride=2, return_indices=True)  # 32 -> 16

        self.bottle_neck = nn.Sequential(
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
        )

        self.upsample0 = nn.MaxUnpool2d(2, stride=2)  # 16 -> 32
        self.dec_conv0 = nn.Sequential(
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*8, start_channels*8,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*8),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*8, start_channels*4,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*4),  # !
            nn.ReLU(),
        )
        self.upsample1 = nn.MaxUnpool2d(2, stride=2)  # 32 -> 64
        self.dec_conv1 = nn.Sequential(
            nn.Conv2d(start_channels*4, start_channels*4,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*4),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*4, start_channels*4,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*4),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*4, start_channels*2,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*2),  # !
            nn.ReLU(),
        )
        self.upsample2 = nn.MaxUnpool2d(2, stride=2)  # 64 -> 128
        self.dec_conv2 = nn.Sequential(
            nn.Conv2d(start_channels*2, start_channels*2,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels*2),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels*2, start_channels,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels),  # !
            nn.ReLU(),
        )
        self.upsample3 = nn.MaxUnpool2d(2, stride=2)  # 128 -> 256
        self.dec_conv3 = nn.Sequential(
            nn.Conv2d(start_channels, start_channels,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(start_channels),  # !
            nn.ReLU(),
            nn.Conv2d(start_channels, out_channels,
                      kernel_size=3, stride=1, padding=1),
        )

    def forward(self, x):
        # encoder
        x = self.enc_conv0(x)
        x, indices0 = self.pool0(x)
        x = self.enc_conv1(x)
        x, indices1 = self.pool1(x)
        x = self.enc_conv2(x)
        x, indices2 = self.pool2(x)
        x = self.enc_conv3(x)
        x, indices3 = self.pool3(x)

        x = self.bottle_neck(x)
        # decoder
        x = self.upsample0(x, indices=indices3)
        x = self.dec_conv0(x)

        x = self.upsample1(x, indices=indices2)
        x = self.dec_conv1(x)

        x = self.upsample2(x, indices=indices1)
        x = self.dec_conv2(x)

        x = self.upsample3(x, indices=indices0)
        x = self.dec_conv3(x)
        return x


class UNet(nn.Module):
    """
        UNet model implementation
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports: DoubleConv, Down, OutConv, Up

        :packages:
            from torch import nn
            import torch

    """

    def __init__(self, in_channels=3, num_classes=21, bilinear=False, **params):
        super(UNet, self).__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.bilinear = bilinear

        self.inc = DoubleConv(in_channels, 64)
        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        factor = 2 if bilinear else 1
        self.down4 = Down(512, 1024 // factor)
        self.up1 = Up(1024, 512 // factor, bilinear)
        self.up2 = Up(512, 256 // factor, bilinear)
        self.up3 = Up(256, 128 // factor, bilinear)
        self.up4 = Up(128, 64, bilinear)
        self.outc = OutConv(64, num_classes)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        logits = self.outc(x)
        return logits

class OutConv(nn.Module):
    """
    Resulting convolution
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports:

    :packages:
        from torch import nn
        import torch

    """

    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        return self.conv(x)

class Up(nn.Module):
    """
    Upscaling then double conv
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: DoubleConv

    :packages:
        from torch import nn
        import torch

    """

    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()

        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:
            self.up = nn.Upsample(
                scale_factor=2, mode="bilinear", align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)
        else:
            self.up = nn.ConvTranspose2d(
                in_channels, in_channels // 2, kernel_size=2, stride=2
            )
            self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        # input is CHW
        # diffY = x2.size()[2] - x1.size()[2]
        # diffX = x2.size()[3] - x1.size()[3]
        #
        # x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
        #                 diffY // 2, diffY - diffY // 2])
        # if you have padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)

class Down(nn.Module):
    """
    Downscaling with maxpool then double conv
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: DoubleConv

    :packages:
        from torch import nn
        import torch
    """

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2), DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)

class DoubleConv(nn.Module):
    """
        DoubleConv block implementation
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports:

        :packages:
            from torch import nn
            import torch

    """

    def __init__(self, in_channels, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.double_conv(x)

def load_metric(metric_name: str, classes_amount: int):
    '''
    Returns metric from given metric name

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:

    :param str metric_name: metric name
    :param int classes_amount: number of classes

    '''
    if metric_name == 'IoU':

        def iou_pytorch(outputs: torch.Tensor, labels: torch.Tensor, mean=True):
            """
            IoU metric function
            :code_assign: service
            :code_type: Глубокое обучение/Сегментация
            :packages:
            """
            hist = _fast_hist(labels, outputs, classes_amount)
            return jaccard_index(hist, mean=mean)
        return iou_pytorch
    elif metric_name == 'dice':
        def dice_pytorch(outputs: torch.Tensor, labels: torch.Tensor, mean=True):
            """
            Dice metric function
            :code_assign: service
            :code_type: Глубокое обучение/Сегментация
            :packages:
            """

            hist = _fast_hist(labels, outputs, classes_amount)
            return dice_coefficient(hist, mean=mean)
        return dice_pytorch
    else:
        raise ValueError("Uncorrect metric_name input")

def dice_coefficient(hist, mean=True):
    """Computes the Sørensen–Dice coefficient, a.k.a the F1 score.

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch

    :param torch.tensor hist: confusion matrix.


    Returns:
        avg_dice: the average per-class dice coefficient.
    """
    A_inter_B = torch.diag(hist)
    A = hist.sum(dim=1)
    B = hist.sum(dim=0)
    dice = (2 * A_inter_B) / (A + B + 1e-12)
    if mean:
        avg_dice = nanmean(dice)
        return avg_dice
    else:
        return dice

def jaccard_index(hist, mean=True):
    """
    Computes the Jaccard index, a.k.a the Intersection over Union (IoU).
    Returns avg_jacc: the average per-class jaccard index.

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :packages:
        import torch
    :param torch.tensor hist: confusion matrix.

    """
    A_inter_B = torch.diag(hist)
    A = hist.sum(dim=1)
    B = hist.sum(dim=0)
    jaccard = A_inter_B / (A + B - A_inter_B + 1e-12)
    if mean:
        avg_jacc = nanmean(jaccard)
        return avg_jacc
    else:
        return jaccard

def nanmean(x):
    """
    Computes the arithmetic mean ignoring any NaNs.
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch
    """
    return torch.mean(x[x == x])

def _fast_hist(true, pred, num_classes):
    """
    Считает матрицу смежности
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch
    """
    mask = (true >= 0) & (true < num_classes)

    hist = (
        torch.bincount(
            num_classes * true[mask] + pred[mask],
            minlength=num_classes**2,
        )
        .reshape(num_classes, num_classes)
        .float()
    )
    return hist

def load_loss(loss_name: str, num_classes: int, classes_freq: dict):
    '''
    Returns loss from given loss name

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch

    :param str loss_name: name of loss
    :param int num_classes: number of classes
    :param dict classes_freq: classes frequency

    '''
    if loss_name == 'dice':
        dice_loss = DiceLoss()
        return dice_loss
    elif loss_name == 'focal':
        weights = torch.Tensor(list(classes_freq.values()))
        weights = 1/(weights + 0.005)
        weights /= num_classes
        focal_loss = SegmFocalLoss(weights)
        return focal_loss

    elif loss_name == 'cel':
        cel_loss = CELoss()
        return cel_loss

    else:
        raise ValueError("Uncorrect loss_name input")

class _BaseLoss(torch.nn.Module):
    """
    Abstract class which impement different reductions, weighting, generalizing, and filtering

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports:

    :packages:
        import torch
        from typing import Union, Tuple, List
        import torchvision.transforms.functional as F
    attributes:
            reduction: one of ['s','m','n','mc','mb','mbc','sb','sc','sbc']
                in abbreviations:
                    'm': mean
                    's': sum
                    'b': will not reduce batch dimension (must be first dim)
                    'c': will not reduce class dimension (must be second)
                    'n': will not reduce at all
                Note: for Dice loss and Jaccard loss 'n' reducef can't be used. Generally reducef 'n' can be used
                only for pointwise losses. For  CE, or losses mixed with CE reducef 'c' can't be applied,
                because it turns to BCE.
            weights: list or torch.Tensor of classes weights, used to recalibrate loss.
            ignore_idc: class idc, or list of idcs to ignore, use fuzzy indexing. Only 0 or positive indexes
                can be used. For now cant'be used with pseudo ignore_idc
            pseudo_ignore_idc: class idc, or list of idcs to ignore, only 0 or positive indexes can be used.
                Weight in loss will be 0, but it's plane will be used in normalization (in softmax)
                ____________________________________________________________________________________________________
                Note: for this class idc also must have plane in logits C dimensions. If this option used
                    automatically set's use_softmax to True
            use_softmax: flag to use softmax for raw logits, or not to use if softmax was used already


    """

    workdims = "bcwh"

    def create_reduction(self, workdims=None, redefine_rstr=None):

        rstr = self.rstr if redefine_rstr is None else redefine_rstr
        workdims = self.workdims if workdims is None else workdims
        assert (
            rstr[0] in ["s", "m", "n"]
            if len(rstr) == 1
            else all(
                [
                    rstr[0] in ["s", "m", "n"],
                    rstr[1:] in ["c", "b", "bc"],
                    *[char in workdims for char in rstr[1:]],
                ]
            )
        ), (
            f"{rstr} is wrong reducef mode or some"
            f" of dims not in workdims = {workdims}!"
        )
        if rstr == "n":
            return lambda x: x
        else:
            if rstr[0] == "m":
                def reduce_f(x, args): return x.mean(
                    args) if len(args) > 0 else x.mean()
            elif rstr[0] == "s":
                def reduce_f(x, args): return x.sum(
                    args) if len(args) > 0 else x.sum()
            reduce_dims = [i for i, char in enumerate(
                workdims) if char not in rstr]

            def reduce_function(x): return reduce_f(x, reduce_dims)

        return reduce_function

    def __init__(
        self,
        reduction="n",
        weights=None,
        ignore_idc=[],
        pseudo_ignore_idc=[],
        use_softmax=True,
    ):
        super(_BaseLoss, self).__init__()
        # self.reducef = (self,)
        self.rstr = reduction
        self.reducef = self.create_reduction()
        if weights is not None:
            if isinstance(weights, list):
                self.weights = torch.Tensor(
                    weights).reshape(1, len(weights), 1, 1)
            elif isinstance(weights, torch.Tensor):
                assert weights.ndimension() in [1, 2, 4], (
                    "If weights passed like torch.Tensor, "
                    "that tensor must have 1,2 or 4 dimensions"
                )
                if weights.ndimension() == 2:
                    assert weights.shape[0] == 1
                    weights = weights.reshape(weights.shape + (1, 1))
                if weights.ndimension() == 1:
                    weights = weights.reshape(1, len(weights), 1, 1)
                if weights.ndimension() == 4:
                    assert all([weights.shape[i] == 1 for i in [0, 2, 3]])
                self.register_buffer(
                    "weights",
                    weights,
                    persistent=False
                )

        assert (
            isinstance(ignore_idc, (list, int)) and all(
                [x >= 0 for x in ignore_idc])
            if isinstance(ignore_idc, list)
            else ignore_idc >= 0
        )
        ignore_idc = (
            [ignore_idc] if not isinstance(ignore_idc, list) else ignore_idc
        )  # for better slicing

        self.ignore_idc = ignore_idc

        self.use_softmax = use_softmax
        assert (
            isinstance(pseudo_ignore_idc, (list, int))
            and all([x > 0 for x in pseudo_ignore_idc])
            if isinstance(pseudo_ignore_idc, list)
            else pseudo_ignore_idc >= 0
        )
        pseudo_ignore_idc = (
            [pseudo_ignore_idc]
            if not isinstance(pseudo_ignore_idc, list)
            else pseudo_ignore_idc
        )
        self.pseudo_ignore_idc = pseudo_ignore_idc
        if len(pseudo_ignore_idc) > 0:
            warn("Use softmax changed to True, as result of using preudo_ignore_idc!")
            self.use_softmax = True
        else:
            self.use_softmax = use_softmax
        if len(pseudo_ignore_idc) > 0 and len(ignore_idc) > 0:
            raise NotImplementedError

    def apply_weights(
        self,
        *args: Tuple[Union[torch.FloatTensor, torch.LongTensor]],
        weights: torch.FloatTensor = None,
    ):
        """
        Method to statically or dynamically apply weights to tensor or tuple of tensors  if weights exist
        Args:
            tensor or tuple of tensors. Shape [BxCxWxH]
            weights: optional, for dynamic weights calculations.
        Note:
            if weights passed, weights shape can be either [1xCx1x1] or [BxCx1x1].
        """
        if weights is None and hasattr(self, "weights"):
            assert self.weights is not None
            weights = self.weights
            if weights.device != args[0].device:
                weights = weights.to(args[0].device)
            for ii, tensor in enumerate(args):
                assert all(
                    [
                        any(
                            [
                                weights.ndimension() == tensor.ndimension(),
                                weights.ndimension() + 1 == tensor.ndimension(),
                            ]
                        ),
                        weights.shape[1] == tensor.shape[1],
                    ]
                ), f"""
                Weights ndim not as input {ii} ndim or 1 dimenstion didnt match:
                w ndim:{weights.ndimension()}, input ndim: {tensor.ndimension()},
                weights shape: {weights.shape}, input shape: {tensor.shape}
                """
            return (
                tuple([tensor * weights for tensor in args])
                if len(args) != 1
                else tensor * weights
            )
        elif weights is not None:
            for ii, tensor in enumerate(args):
                assert all(
                    [
                        weights.ndimension() == tensor.ndimension(),
                        #                             weights.shape[1] == tensor.shape[1],
                        #                             weights.shape[0] == tenspr.shape[0],
                    ]
                ), f"""
                Weights ndim not as input {ii} ndim or 1 dimenstion didnt match:
                w ndim:{weights.ndimension()}, input ndim: {tensor.ndimension()},
                weights shape: {weights.shape}, input shape: {tensor.shape}
                """
            return (
                tuple([tensor * weights for tensor in args])
                if len(args) != 1
                else tensor * weights
            )
        else:
            return args if len(args) != 1 else args[0]

    def forward(
        self, gt: Union[torch.LongTensor, torch.ByteTensor], pred: torch.FloatTensor
    ) -> torch.FloatTensor:
        """Must be implemented by child class of Losses"""

        raise NotImplementedError

    @staticmethod
    def generalized_weights(
        onehot: Union[torch.ByteTensor, torch.LongTensor, torch.FloatTensor],
        by: str = "bc",
        gamma: float = -2,
        eps: float = 1e-10,
    ):
        """Function to compute weights dynamically
        Args:
            onehot: one hot encoded ground true
            by: one of 'b','c', 'bc'. By which dimension must be generalized.
            eps: added to denominator for numerical stability
            gamma: power of weights, default - 2
        weights = 1 / (reducef(onehot,'s' + by) + eps)^2
        """
        warn(
            f"Note: After generalization by {by} dimeshions sum by this dimension or dimensions allways be equal to 1"
        )
        assert len(onehot.shape) > 2
        assert by in ["c", "bc", "b"]
        if by == "b":
            warn(
                "Generalizing only by batch dimension is Bad practice for segmentation,"
                " but can be good for some gan applications"
            )
        #         weights =  1 / (( onehot.sum([i for i in range(onehot.ndimension()) if i not in [0,1]]) + 1e-10) ** 2)
        # weights = (onehot.sum()) / ((einsum(f"bcwh->{by}", onehot).type(torch.float32) + eps) ** 2)
        weights = (
            einsum(f"bcwh->{by}", onehot).type(torch.float32) + eps) ** gamma
        weights = weights.reshape(
            [onehot.shape[i] if char in by else 1 for i,
                char in enumerate("bcwh")]
        )

        return weights

    def filter_and_2probas(
        self,
        gt: Union[torch.LongTensor, torch.ByteTensor],
        logits: torch.FloatTensor,
        redefine_use_softmax: bool = False,
        positive_filter: bool = True,
    ):
        """
        Method to filter out from raw logits and gt's ingored idcs or pseudo ignored idcs, logits will normalize in
        C dimension by softmax if use_softmax flag passed. GT represnted in 'one hotted' format of shape [BxCxWxH]
         with sparse dimension C (there only one nonzero element that equal 1), where all values can be just 0 or 1.

        :param torch.Tensor gt: ground True of shape [BxHxW]
        :param torch.Tensor logits: raw output of model with shape [BxCxHxW]
        :param bool positive_filter: filter out all classes with negative id
        Returns:
            gt_hot, probas
        """
        use_softmax = (
            self.use_softmax if not redefine_use_softmax else redefine_use_softmax
        )

        assert all([logits.ndimension() == 4, gt.ndimension() == 3])

        assert any([hasattr(self, "num_classes"), logits is not None])
        num_classes = (
            self.num_classes
            if hasattr(self, "num_classes")
            else logits.shape[1] + len(self.ignore_idc)
        )
        # Filter Logits
        if len(self.ignore_idc) > 0:
            # Questionable filtration. Ignore idc need to filter out only from onehotted gt's,
            # but can work if cls_idc on top of gt
            # Edit: Needed to apply ignored mask anyway, that's why lesser computation needed
            logits = logits[
                :,
                [
                    cl_idc
                    for cl_idc in range(num_classes)
                    if cl_idc not in self.ignore_idc
                ],
                ...,
            ]
            probas = F.softmax(logits, dim=1) if use_softmax else logits
        if not positive_filter:
            gt_hot = torch.eye(num_classes + len(self.ignore_idc), device=gt.device)[
                gt.squeeze(1)
            ]
            gt_hot = (
                gt_hot.permute(0, 3, 1, 2).float().type(
                    logits.type()).to(logits.device)
            )

            if len(self.ignore_idc) > 0:
                gt_hot = gt_hot[
                    :,
                    [
                        cl_idc
                        for cl_idc in range(num_classes)
                        if cl_idc not in self.ignore_idc
                    ],
                    ...,
                ]
                # ignored_mask = (gt_hot[:, [self.ignore_idc], ...]).sum(1) == 0
                # gt_hot = gt_hot[:, [cl_idc for cl_idc in range(num_classes) if cl_idc not in self.ignore_idc], ...]
                # probas = F.softmax(logits * ignored_mask.float(), dim=1) if use_softmax else logits * ignored_mask.float()
            elif len(self.pseudo_ignore_idc) > 0:
                gt_hot = gt_hot[
                    :,
                    [
                        cl_idc
                        for cl_idc in range(num_classes)
                        if cl_idc not in self.pseudo_ignore_idc
                    ],
                    ...,
                ]
                probas = F.softmax(logits, dim=1)
                probas = probas[
                    :,
                    [
                        cl_idc
                        for cl_idc in range(num_classes)
                        if cl_idc not in self.pseudo_ignore_idc
                    ],
                    ...,
                ]
            else:
                probas = F.softmax(logits, dim=1) if use_softmax else logits
        else:
            # shifting all to + 1, and filtering out first dim
            gt_hot = torch.eye(num_classes + 1, device=gt.device)[
                gt.squeeze(1) + 1
            ].permute(0, 3, 1, 2)

            # Applying ignored mask
            if not use_softmax:
                probas = logits * (1 - gt_hot[:, 0:1, :, :])
            else:
                probas = F.softmax(logits, dim=1) * (1 - gt_hot[:, 0:1, :, :])
            # filtering shifted dim:
            gt_hot = gt_hot[:, 1:, :, :]
        return gt_hot, probas

class CELoss(_BaseLoss):
    """
    This is a implementation of cross entropy which supports ignoring class


    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: _BaseLoss

    :packages:
        import torch


    attributes:
        weights: (tensor) 3D or 4D the scalar factor for this criterion
        gamma: (float,double) gamma > 0 reduces the relative loss for well-classified examples (p>0.5) putting more
                    focus on hard misclassified example

        size_average: (bool, optional) By default, the losses are averaged over each loss element in the batch.
        Note: ignored class must be in weights with weight 0, :: Maybe we need to adjust dim in pt?

    """
    workdims = "bwh"

    def __init__(
        self,
        weights=None,
        reduction="m",  # main params
        use_softmax=False,
        ignore_idc=[],
        pseudo_ignore_idc=[],  # subclass params
    ):
        super(CELoss, self).__init__(
            reduction=reduction,
            weights=weights,
            ignore_idc=ignore_idc,
            pseudo_ignore_idc=pseudo_ignore_idc,
            use_softmax=use_softmax,
        )
        if weights is not None:
            self.num_classes = len(weights)

        self.eps = 1e-6
        self.reduction = reduction
        self.minreducef = lambda x: x.sum(
            1
        )  # sum by class dimension. If we now want sum we need to use BCELoss for each class

    def forward(self, logit, gt):
        gt_hot, probas = self.filter_and_2probas(gt, logit)

        probas = probas.softmax(1) if self.use_softmax else logit
        # HotFix
        # if probas.shape[1] != self.num_classes:
        #     raise RuntimeError(f"dim 1 of logits: [{probas.shape[1]}] didn't match num classes: {len(self.alpha)}")
        # print(gt.unique())
        probas = (probas + self.eps) * gt_hot
        logpt = (probas + (1 - gt_hot)).log()

        logpt = self.apply_weights(logpt)
        loss = -1 * logpt
        loss = self.minreducef(loss)
        loss = self.reducef(loss)
        return loss

class SegmFocalLoss(_BaseLoss):
    """
    This is a implementation of Focal Loss with smooth label cross entropy supported which is proposed in
    'Focal Loss for Dense Object Detection. (https://arxiv.org/abs/1708.02002)'
        Focal_Loss= -1*weights*(1-pt)*log(pt)


    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: _BaseLoss

    :packages:
        import torch

    attributes:
        weights: (tensor) 3D or 4D the scalar factor for this criterion
        gamma: (float,double) gamma > 0 reduces the relative loss for well-classified examples (p>0.5) putting more
                      focus on hard misclassified example
        smooth: (float,double) smooth value when cross entropy
        size_average: (bool, optional) By default, the losses are averaged over each loss element in the batch.
                Note: ignored class must be in weights with weight 0, :: Maybe we need to adjust dim in pt?

    """
    workdims = "bwh"

    def __init__(
        self,
        weights=None,
        gamma=2,
        reduction="m",  # main params
        use_softmax=False,
        ignore_idc=[],
        pseudo_ignore_idc=[],  # subclass params
    ):
        super(SegmFocalLoss, self).__init__(
            reduction=reduction,
            weights=weights,
            ignore_idc=ignore_idc,
            pseudo_ignore_idc=pseudo_ignore_idc,
            use_softmax=use_softmax,
        )
        if weights is not None:
            self.num_classes = len(weights)

        self.gamma = gamma
        self.eps = 1e-6
        self.reduction = reduction
        self.minreducef = lambda x: x.sum(
            1
        )  # sum by class dimension. If we now want sum we need to use FocalBinaryLoss for each class

    def forward(self, logit, gt):
        gt_hot, probas = self.filter_and_2probas(gt, logit)

        probas = probas.softmax(1) if self.use_softmax else logit
        # HotFix
        # if probas.shape[1] != self.num_classes:
        #     raise RuntimeError(f"dim 1 of logits: [{probas.shape[1]}] didn't match num classes: {len(self.alpha)}")

        probas = (probas + self.eps) * gt_hot
        logpt = (probas + (1 - gt_hot)).log()

        logpt = self.apply_weights(logpt)
        loss = -1 * torch.pow(1.0 - probas, self.gamma) * logpt
        loss = self.minreducef(loss)
        loss = self.reducef(loss)
        return loss


class DiceLoss(_BaseLoss):
    """Computes the Sørensen–Dice loss.

    Note that PyTorch optimizers minimize a loss. In this
    case, we would like to maximize the dice score so we
    return the negated dice score.

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: _BaseLoss

    :packages:
        import torch

    attributes:
        weights: a tensor,List or np.array of shape [ C ].
        generalized_weights: parameter which controls how to compute weights dynamically,
                typically it will reduce one-hotted labels to [B] ,[C],[B x C] dimension, and if passed True,
                static weights didn't be used.
        reduction: one of ['s','m','mc','mb','mbc','sb','sc','sbc']
                in abbreviations:
                                'm': mean
                                's': sum
                                'b': will not reduce batch dimension (must be first dim)
                                'c': will not reduce class dimension (must be second)
                                'n': will not reduce at all (can't be used with this loss)
        ignore_idc: class idc, or list of idcs to ignore, use fuzzy indexing.
                Only 0 or positive indexes can be used. Now cant'be used with pseudo ignore_idc

        pseudo_ignore_idc: class idc, or list of idcs to ignore, only 0 or positive indexes can be used.
                Weight in loss will be 0, but it's plane will be used in normalization (in softmax)
                Note: for this class idc also must have plane in logits C dimensions.
                    If this option used automatically set's use_softmax to True
        eps: added to the denominator for numerical stability. default eps = 1e-9
        smooth: a scalar, which added to numerator and denominator to handle 1 pix case

    """
    workdims = "bc"

    def __init__(
        self,
        weights=None,
        generalized_weights=False,
        reduction="mbc",
        ignore_idc=[],
        eps=1e-2,
        use_softmax=False,
        pseudo_ignore_idc=[],
        smooth=0,
    ):
        self.min_reduction = "sbc"
        self.eps = eps
        super(DiceLoss, self).__init__(
            reduction=reduction,
            weights=weights,
            ignore_idc=ignore_idc,
            pseudo_ignore_idc=pseudo_ignore_idc,
            use_softmax=use_softmax,
        )
        self.minreduce = self.create_reduction(
            redefine_rstr=self.min_reduction, workdims="bcwh"
        )
        self._genwts = generalized_weights
        if reduction[1:] == self.workdims:
            self.reducef = self.create_reduction(redefine_rstr="n")
        assert not all([hasattr(self, "weights"), self._genwts])
        self.smooth = smooth

    def __call__(self, logits, gt):
        """
        :param torch.Tensor gt: a tensor of shape [B, 1, H, W].
        :param torch.Tensor logits: a tensor of shape [B, C, H, W]. Corresponds to the raw output or logits of the model.
        Returns:
            dice_loss: the Sørensen–Dice loss.
        """

        gt_hot, probas = self.filter_and_2probas(gt, logits)
        intersection = probas * gt_hot.float()
        cardinality = probas + gt_hot.float()
        intersection = self.minreduce(intersection)  # [B x C]
        cardinality = self.minreduce(cardinality)
        dice_loss = 1 - (2.0 * intersection + self.smooth) / (
            self.smooth + cardinality + self.eps
        )
        dice_loss = dice_loss.view(*dice_loss.shape, 1, 1)  # [B x C x 1 x 1 ]

        if hasattr(self, "weights") and not self._genwts:
            dice_loss = self.apply_weights(dice_loss)
        elif self._genwts:
            dice_loss = self.apply_weights(
                dice_loss, weights=self.generalized_weights(
                    gt_hot, self._genwts)
            )

        dice_loss = self.reducef(dice_loss)
        dice_loss = dice_loss.mean()
        # dice_loss = self.reducef((2. * intersection + self.eps)/ (cardinality + self.eps))
        return dice_loss

def load_path(path: str) -> str:
    '''
    Converts path from 'default' to 'project/segmentlib/bin' if 'default' is provided

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :packages:

    :param str path: path to save something

    '''
    if path == 'default':
        return load_default_path()
    else:
        return path

def load_default_path():
    '''
    Returns default dir path for saving results
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import os
    '''
    return os.path.join(DATA_PATH, 'bin')

class ResultsVisualizer:
    '''
    Class for results visualization(generally for gui_dict)
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports: get_plot_dict, get_pic_dict,ColorConverter

    :packages:
        import os
        import numpy as np
        import torch
        from torchvision.utils import save_image
        import plotly.graph_objects as go
        import pandas as pd
        from PIL import Image

    '''

    def __init__(self, config={}, path=''):
        if config != {}:
            self.config = config
            self.classes_amount = config['classes_amount']

            self.classes_dict = config['classes_dict']
            self.metric_name = self.config['metric']
            self.loss_name = self.config['loss']
            self.path = path
            if not os.path.exists(self.path):
                os.mkdir(self.path)

        self.color_converter = ColorConverter()

    def get_test_gui_dict(self, test_results: dict):
        '''
        Returns gui_dict for test mode
        :param dict test_results: results of testing
        '''
        gui_dict = {'plot': [], 'text': [], 'table': [], 'image': []}
        # canvases = self.get_test_canvases(
        #     **test_results)
        # gui_dict['plot'].append(
        #     Window(window_title="Test results", canvases=canvases).to_dict())

        # # Saving some examples of test predictions
        # for pic_id, pic_fp in enumerate(test_results['test_examples_paths']):
        #     title = f'Predict test example #{pic_id}'
        #     gui_dict['image'].append(get_pic_dict(
        #         pic_fp, title))
        return gui_dict

    def get_train_gui_dict(self, train_results: dict):
        '''
        Returns gui_dict for train mode
        :param dict train_results: results of training
        '''
        gui_dict = {'plot': [], 'text': [], 'table': [], 'image': []}
        # canvases = ResultsVisualizer.get_train_canvases(
        #     **train_results)
        # gui_dict['plot'].append(
        #     Window(window_title="Train results", canvases=canvases).to_dict().copy())

        # # Saving some examples of augmentation
        # for pic_id, pic_fp in enumerate(train_results['train_examples_paths']):
        #     title = f'Augmentation train example #{pic_id}'
        #     gui_dict['image'].append(get_pic_dict(
        #         pic_fp, title))
        return gui_dict

    def save_test_examples(self, *data):
        """"
        Saves pics in format: |pic|mask|pred_mask|
        :param Union[tuple,list] data: list(tuple) with elemets
         (orig_pic, orig_mask, mask_pred)
        returns paths of saved images
        """
        paths_list = []
        if not os.path.exists(os.path.join(self.path, 'test_examples')):
            os.mkdir(os.path.join(self.path, 'test_examples'))
        for i, (orig_pic, orig_mask, mask_pred) in enumerate(data):
            shape = orig_pic.shape
            mask_pred = mask_pred.squeeze(0)
            mask_pred = self.color_converter.mask2rgb(mask_pred)

            orig_mask = orig_mask.squeeze(0)
            orig_mask = self.color_converter.mask2rgb(orig_mask)

            vbl = torch.zeros((3,  shape[1], 1))  # vertical_black_line
            pic_cat = torch.cat(
                (orig_pic, vbl, orig_mask, vbl, mask_pred), dim=2)
            pic_fp = os.path.join(
                self.path, 'test_examples', f'test_ex{i}.png')
            self.save_pic(pic_cat, pic_fp)
            paths_list.append(pic_fp)
        return paths_list

    def save_train_examples(self, *data):
        """"
        Saves training examples with augmentations in
        shape:
            |orig_pic | aug_pic |
            |orig_mask| aug_mask|
        :param Union[tuple,list] data: list(tuple) with elemets
         (orig_pic, orig_mask, aug_pic, aug_mask)
        returns paths of saved images
        """
        paths_list = []
        if not os.path.exists(os.path.join(self.path, 'train_examples')):
            os.mkdir(os.path.join(self.path, 'train_examples'))
        for i, (orig_pic, orig_mask, aug_pic, aug_mask) in enumerate(data):
            shape = orig_pic.shape
            aug_mask = self.color_converter.mask2rgb(aug_mask)

            orig_mask = self.color_converter.mask2rgb(orig_mask)

            pic_cat = torch.cat(
                (orig_pic, torch.ones((3,  shape[1], 1)), aug_pic), dim=2)
            mask_cat = torch.cat(
                (orig_mask, torch.ones((3, shape[1], 1)), aug_mask), dim=2)

            all_pic = torch.cat((pic_cat, torch.ones(
                (3, 1, 2*shape[2]+1)), mask_cat), dim=1)

            pic_fp = os.path.join(
                self.path, 'train_examples', f'train_ex{i}.png')
            self.save_pic(all_pic, pic_fp)
            paths_list.append(pic_fp)
        return paths_list

    def save_pic(self, pic, filename, using_pillow=False):
        '''Input image has torch shape(3,w,h)'''
        if using_pillow:
            if len(pic.shape) == 3:
                img = Image.fromarray(pic.permute(
                    1, 2, 0).cpu().numpy().astype(np.uint8))
            else:
                img = Image.fromarray(
                    pic.astype(np.uint8), mode='P')
                img.putpalette(self.color_converter.palette)

            # сохранение изображения
            img.save(filename)
        else:
            save_image(pic, filename)

    def set_hist(self, hist):
        self.hist = hist

    @staticmethod
    def get_train_canvases(train_scores: list, val_scores: list, train_loss: list, val_loss: list, class_counter: dict, **params):
        '''
        Returns plotly figures for train mode
        :param dict train_scores: list of train scores(metrics)
        :param Union[list, tuple] val_scores: list of val scores(metrics)
        :param Union[list, tuple] train_loss: list of train losses
        :param Union[list, tuple] val_loss: list of val losses
        :param dict class_counter: count stats for class

        imports:  LinePlot, BarPlot, PiePlot, HeatPlot, Canvas, Window
        packages:
            import numpy as np
        '''
        x = list(range(len(train_scores)))

        fig_class_counter = Canvas(title="Classes amount statistic",
                                   showlegend=True, plots=[PiePlot(labels=list(class_counter.keys()), values=np.array(list(class_counter.values())))])

        fig_loss = Canvas(title="Loss per epoch", x_title='epochs', y_title='loss',
                          showlegend=True, plots=[LinePlot(x=np.array([x, x]).T, y=np.array([train_loss, val_loss]).T, names=['train_loss', "val_loss"])])

        fig_score = Canvas(title="Scores per epoch", x_title='epochs', y_title='score',
                           showlegend=True, plots=[LinePlot(x=np.array([x, x]).T, y=np.array([train_scores, val_scores]).T, names=['train_score', "val_score"])])

        return fig_loss, fig_score, fig_class_counter

    def get_test_canvases(self, conf_matrix: torch.Tensor, loss_all: float, metric_all: float, per_class_pixel_accuracy: list, class_counter: dict, **params):
        '''
        Returns plotly figures for test mode
        :param torch.Tensor conf_matrix: confusion matrix
        :param float loss_all: whole loss of testing
        :param float metric_all: whole metric of testing
        :param list per_class_pixel_accuracy: list of class pixel accuracy
        :param dict class_counter: classes amount stats

        imports:  LinePlot, BarPlot, PiePlot, HeatPlot, Canvas, Window
        packages:
            import numpy as np
        '''
        class_names = list(self.classes_dict.keys())

        fig_cm = Canvas(title="Confusion Matrix", x_title='y_pred', y_title='y_true',
                        showlegend=True, plots=[HeatPlot(z=conf_matrix[:, :, 0], showscale=True, z_text=None, x=class_names, y=class_names)])
        fig_cm_normalized = Canvas(title="Confusion Matrix(normalized)", x_title='y_pred', y_title='y_true',
                                   showlegend=True, plots=[HeatPlot(z=conf_matrix[:, :, 1], showscale=True, z_text=None, x=class_names, y=class_names)])
        fig_acc_per_class = Canvas(title="Per class pixel accuracy", y_title='accuracy',
                                   showlegend=True, plots=[BarPlot(x=np.arange(len(per_class_pixel_accuracy)), names=class_names, y=np.array(per_class_pixel_accuracy))])

        fig_class_counter = Canvas(title="Classes amount statistic",
                                   showlegend=True, plots=[PiePlot(labels=list(class_counter.keys()), values=np.array(list(class_counter.values())))])

        fig_summary = Canvas(title="Test summary", y_title='accuracy',
                                   showlegend=True, plots=[BarPlot(x=np.arange(2), names=[f'Loss({self.loss_name})', f'Score({self.metric_name})'], y=np.array([loss_all, metric_all]))])

        return fig_cm, fig_cm_normalized, fig_acc_per_class, fig_class_counter, fig_summary

    # def get_test_figures(self, conf_matrix: torch.Tensor, loss_all: float, metric_all: float, per_class_pixel_accuracy: list, class_counter: dict, **params):
    #     '''
    #     Returns plotly figures for test mode
    #     :param torch.Tensor conf_matrix: confusion matrix
    #     :param float loss_all: whole loss of testing
    #     :param float metric_all: whole metric of testing
    #     :param list per_class_pixel_accuracy: list of class pixel accuracy
    #     :param dict class_counter: classes amount stats
    #     '''
    #     class_names = list(self.classes_dict.keys())

    #     layout = {
    #         "title": "Confusion Matrix",
    #         "xaxis": {"title": "y_pred"},
    #         "yaxis": {"title": "y_true"}
    #     }
    #     fig_cm = go.Figure(data=go.Heatmap(z=conf_matrix[:, :, 0],
    #                                        x=class_names,
    #                                        y=class_names,
    #                                        hoverongaps=True, colorscale='Blues'),
    #                        layout=layout)
    #     layout["title"] = "Confusion Matrix (normalized)"
    #     fig_cm_normalized = go.Figure(data=go.Heatmap(z=conf_matrix[:, :, 1],
    #                                                   x=class_names,
    #                                                   y=class_names,
    #                                                   hoverongaps=True, colorscale='Blues'),
    #                                   layout=layout)
    #     fig_acc_per_class = go.Figure(
    #         data=[go.Bar(x=class_names, y=per_class_pixel_accuracy)],
    #         layout=go.Layout(title=f"Per class pixel accuracy", yaxis=dict(
    #             title='accuracy', dtick=0.1))
    #     )

    #     fig_class_counter = go.Figure(
    #         data=[go.Pie(labels=list(class_counter.keys()),
    #                      values=list(class_counter.values()))],
    #         layout=go.Layout(title="Classes amount statistic")
    #     )

    #     fig_summary = go.Figure(
    #         data=[go.Bar(
    #             x=[f'Loss({self.loss_name})', f'Score({self.metric_name})'], y=[loss_all, metric_all]),],
    #         layout=go.Layout(title=f"Test summary")
    #     )

    #     return fig_cm.to_json(), fig_cm_normalized.to_json(), fig_acc_per_class.to_json(), fig_class_counter.to_json(), fig_summary.to_json()

    def save_csv(self):
        ''' Saves to csv results of training'''
        results = pd.DataFrame()
        results['epochs'] = range(len(self.hist['train_loss']))
        results['train loss({self.loss_name})'] = self.hist['train_loss']
        results[f'train score({self.metric_name})'] = self.hist['train_scores']
        results[f'val loss({self.loss_name})'] = self.hist['val_loss']
        results[f'val score({self.metric_name})'] = self.hist['val_scores']
        results.to_csv(os.path.join(self.path, 'results.csv'), index=False)

class ColorConverter:
    '''
    Class for converting colors in masks to RGB format
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :imports:

    :packages:
        import os
        import torch
        import numpy as np
        from PIL import Image
        from PIL import ImagePalette
    '''

    def __init__(self):
        self.colormap = torch.Tensor(self.get_colormap())
        self.palette = self.colormap.to(torch.uint8).reshape(-1)

    @staticmethod
    def get_colormap():
        """
        Returns colormap list
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация
        :packages:
            from PIL import ImagePalette
            import torch
        """

        # colormap = list(ImagePalette.ImageColor.colormap.values())
        # # make black color with index 0
        # color = colormap[0]
        # colormap[0] = colormap[7]
        # colormap[7] = color
        # # make 255 colors
        # colormap = (colormap*2)[:256]
        # # convert from hex
        # colormap = [[int(hex_color[1:][:2], base=16), int(hex_color[1:][2:4], base=16), int(
        #     hex_color[1:][4:], base=16)] for hex_color in colormap]
        #
        # new_colormap = [(0, 0, 0), (48, 48, 240), (176, 48, 240), (208, 240, 48), (240, 48, 80), (240, 192, 48)]
        #
        # return new_colormap

        colormap = [
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
                    if color not in colormap:
                        colormap.append(color)
                    if len(colormap) == 256:
                        return colormap

        return colormap

    def mask2rgb(self, mask: torch.Tensor):
        """
        Converts mask to rgb image
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация
        :packages:
            from matplotlib.colors import hsv_to_rgb
        """
        rgb_image = torch.zeros((3, *mask.shape))
        for pix_value in mask.unique():
            rgb_image[:, mask ==
                      pix_value] = self.colormap[pix_value].unsqueeze(dim=1)
        return rgb_image  # rgb in format (3,w,h)

def apply_augm_to_sinle_image(X, mask, augm):
    """
    Применяет аугментации к входному изображению и его маске.
    Особенность маски и изображения в torch формате
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
    """
    mask = mask.unsqueeze(0)
    mask = cvt_torch_image_to_cv2_image(mask)
    X = cvt_torch_image_to_cv2_image(X)

    X, mask = apply_augm(X, mask, augm)
    return cvt_cv2_image_to_torch_image(X), cvt_cv2_image_to_torch_image(mask).squeeze(0)

def apply_augm(pic, mask, augm):
    """
    Применяет аугментации к одиночному изображению и его маске.
    Особенность - изображение и маска - формате opencv
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
    """
    preproc_data = augm(
        image=pic, mask=mask)
    return preproc_data["image"], preproc_data["mask"]

def cvt_torch_image_to_cv2_image(img):
    """
    Конвертирует изображение из формата данных torch в opencv
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
       import torch
    """
    return torch.permute(img, (1, 2, 0)).numpy()

def cvt_cv2_image_to_torch_image(img):
    """
    Конвертирует изображение из формата данных opencv в torch
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch
    """
    return torch.permute(torch.from_numpy(img), (2, 0, 1))

def apply_augm_to_batch(X_batch, mask_batch, augm):
    """
    Применяет аугментации к входному батчу изображений и масок
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
    """
    mask_batch = mask_batch.unsqueeze(1)

    mask_batch = cvt_torch_batch_to_cv2_batch(mask_batch)
    X_batch = cvt_torch_batch_to_cv2_batch(X_batch)
    for i in range(X_batch.shape[0]):
        X_batch[i], mask_batch[i] = apply_augm(X_batch[i], mask_batch[i], augm)
    return cvt_cv2_batch_to_torch_batch(X_batch), cvt_cv2_batch_to_torch_batch(mask_batch).squeeze(1)

def cvt_cv2_batch_to_torch_batch(img_batch):
    """
    Конвертирует набор изображений из формата данных opencv в torch
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch
    """
    return torch.permute(torch.from_numpy(img_batch), (0, 3, 1, 2))

def cvt_torch_batch_to_cv2_batch(img_batch):
    """
    Конвертирует набор изображений из формата данных torch в opencv
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
    """
    return torch.permute(img_batch, (0, 2, 3, 1)).numpy()

def get_probabilities(logits):
    '''
    Returns probabilities from logits

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch
    :param torch.Tensor logits: model output

    '''
    if logits.shape[1] > 2:
        return torch.softmax(logits, dim=1)
    else:  # if binary segmentation
        return torch.sigmoid(logits)

class SegmDataset(torch_dataset):
    """
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports: check_for_dims
        :packages:
            from torch.utils.data import Dataset as torch_dataset
            import glob
            import tqdm
            import os
            import numpy as np
            from torchvision.transforms.functional import to_tensor
            from PIL import Image
    """

    def __init__(self, img_path: str, ann_path: str, classes_dict: dict,
                 augms=None):
        """
        Инициализация класса датасета(train|test).
        :param str img_path: Путь до папки с картинками
        :param str json_path: Путь до разметочный файлов
        :param dict classes_dict: Словарь с описанием пикселей(из .json)
        :param albumentations.core.composition.Compose augms: аугментации,
            которые долны быть применены к каждой картинке в датасете.
            Пример - Resize
        """
        self.augs = augms
        self.classes_dict = classes_dict
        self.img_formats = ['jpg', 'jpeg', 'png']

        self.ann_list = self.get_pics_list(ann_path)
        self.img_list = self.get_img_from_ant_list(
            self.ann_list, img_path)

    def get_pics_list(self, path):
        '''
        Возвращает список изображений с указанными форматами
        :param str path: Путь до папки с изображениями
        '''
        img_list = []
        for img_format in self.img_formats:
            img_format_list = glob.glob(f'{path}/*.{img_format}')
            if len(img_format_list) != 0:
                img_list = img_list + img_format_list
        return img_list

    def get_img_from_ant_list(self, img_list, ann_path):
        """
        Возвращает всю разметку.
        :param str img_list: Путь до папки с картинками
        :param str ann_path: Путь до папки с разметкой
        """
        ants = []
        for img_fp in tqdm.tqdm(img_list, desc='Loading annotaion files'):
            img_name = img_fp.split('/')[-1]
            img_format = img_name.split('.')[-1]

            # имя файла без расширения(но с точкой, например filename.jpg -> filename.)
            img_name_without_format = img_name[:-len(img_format)]
            # ищем разметочный файл по возможным расширениям
            is_ann_file_found = False
            for possible_format in self.img_formats:
                possible_ann_filename = img_name_without_format + possible_format
                ann_fp = os.path.join(ann_path, possible_ann_filename)

                if os.path.exists(ann_fp):
                    ants.append(ann_fp)
                    is_ann_file_found = True
                    break
            if not is_ann_file_found:
                print(f'{img_name} mask file is not found')
        return ants

    def __len__(self):
        return len(self.img_list)

    def __getitem__(self, index):

        image = check_for_dims(np.array(Image.open(self.img_list[index])))
        label = np.array(Image.open(self.ann_list[index]))

        preproc_data = self.augs(
            image=image, mask=label) if self.augs else None
        if self.augs:
            image, label = preproc_data["image"], preproc_data["mask"]

        image = to_tensor(image)
        label = (
            (torch.from_numpy(label)).long()
            if not isinstance(label, torch.Tensor)
            else label
        )
#        label[label == 255] = -1
        return image, label

def check_for_dims(array):
    '''
    Проверяет из скольки каналов состоит изображение.
    Также исправляет ошибки.
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import numpy as np
    :param np.array array:  array to check
    '''
    if len(array.shape) == 3 and array.shape[2] == 4:
        return array[:, :, :3]
    elif len(array.shape) == 2:
        unsq_arr = array[:, :, np.newaxis]
        return np.concatenate([unsq_arr, unsq_arr, unsq_arr], axis=2)
    return array

class DatasetPixelStats:
    """
        Class PixelCounter needs for calcs info about
        pixels in dataset(generally for frequency)

        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports:
        :packages:
            import torch
            import tqdm
            from copy import deepcopy
        attributes:
            classes_dict:dict
                masks description(options.json). Dict like:{class_name:pixel_value}
            class_counter:dict
                classes counter in masks
            pixels_amount: torch.Tensor
                amount of whole pixels
            upd_count: int
                amount of calling function update()
            dataloader: torch.utils.data.DataLoader

    """

    def __init__(self, classes_dict: dict, dataloader: torch.utils.data.DataLoader):
        self.classes_dict = classes_dict
        self.class_counter = dict([(class_name, torch.Tensor(
            [0]).to(torch.int64))
            for class_name in list(classes_dict.keys())])
        self.pixels_amount = torch.Tensor([0]).to(
            torch.int64)  # amount of pixels
        self.upd_count = 0  # Num of calling function update()
        self.dataloader = dataloader
        self.evaluate_dataloader()  # calc dataset stats

    def evaluate_dataloader(self):
        """Подсчитывает статистику классов в даталоадере"""
        for _, mask in tqdm.tqdm(self.dataloader, desc='Calc dataset stats..'):
            self.update(mask, is_batch=True)

    def update(self, mask: torch.Tensor, is_batch=False):
        '''
        Calls each image
        :param torch.Tensor mask: input mask
        :param bool is_batch: is input mask has batch shape
        '''
        if is_batch:
            self.upd_count += mask.shape[0]
        else:
            self.upd_count += 1
        self.pixels_amount += torch.numel(mask)  # elements_amount
        # enumerate(self.classes_dict.keys()):
        for class_name, index in self.classes_dict.items():
            self.class_counter[class_name] += (mask == index).sum()

    def get_pixels_frequency(self):
        '''
        Returns frequency of pixels
        '''
        frequency = deepcopy(self.class_counter)
        for (class_name, count) in frequency.items():
            frequency[class_name] = count.detach().cpu().item() / \
                self.pixels_amount

        return frequency

    def get_pixels_count(self):
        """
        Returns each class pixels count
        """
        counter = deepcopy(self.class_counter)
        for (class_name, count) in counter.items():
            counter[class_name] = count.detach().cpu().item()
        return counter

def segm_test(model: torch.nn.Module,
              path_to_dataset: str,
              save_results_path: str = 'default',
              imgsz: int = 224,
              device='cpu',
              num_workers=5,
              batch_size=16,
              metric='IoU',
              loss='focal'):
    """
    Segmentation testing pipeline

    :code_assign: users
    :code_type: Глубокое обучение/Сегментация(тестирование)
    :imports: load_classes_dict, create_test_dataloader, load_params, mask_cvtr, ResultsVisualizer, Evaluator, get_probabilities

    :packages:
        import os
        import numpy as np
        import torch
        import tqdm


    :param_block torch.nn.Module model Model: model to test.

    :param str path_to_dataset: path to dataset folder. Dataset must contain folders: images, masks. Also in this path must be file options.json

    :param str device: Name of device for training. Possible values 'cpu', 'cuda:0', 'cuda:1', etc. Defaults to 'cpu'. Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру
    :param int num_workers: Num workers in DataLoader. Defaults to 5. Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру


    :param int imgsz: Size of images for model input. Defaults to 224
    :param str metric: Name of metric to score model. Possible values: 'IoU',dice. Defaults to IoU'
    :param int batch_size: Batch size for training. Defaults to 16.
    :param str loss: name of loss function. Possible values: 'dice', 'focal'. Defaults to 'focal'.
    :param str save_results_path: path to save examples. Program will create folder test_examples. Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру.
    :returns: gui_dict
    :rtype:   dict
    :semrtype:
    """

    print('Test mode is enabled..')
    img_path_to_dataset = os.path.join(path_to_dataset, 'images')
    mask_path_to_dataset = os.path.join(path_to_dataset, 'masks')
    path_to_classes_dict = os.path.join(path_to_dataset, 'options.json')

    config = locals()  # converts input arguments to dict
    config['mode'] = 'test'
    config['classes_dict'] = load_classes_dict(path_to_classes_dict)

    print("Initializing Dataloaders...")
    data_ts, dataset = create_test_dataloader(config)

    config['dataloader'] = data_ts
    # dataset.pix_stats_evaluator.get_pixels_frequency()
    test_params = load_params(config)

    ts_len = len(data_ts)
    print('Dataloaders are initialized..')

    device = test_params['device']
    loss_fn = test_params['loss']
    metric = test_params['metric']

    classes_dict = config['classes_dict']
    mask2id_cvtr = dict([(value, i)
                         for i, (key, value) in enumerate(classes_dict.items())])  # dict for converting values. Looks like {'class_id':'index'}

    classes_amount = len(classes_dict.keys())
    loss_name = config['loss']
    metric_name = config['metric']

    save_path = config['save_results_path']

    model.to(device)
    print('Test instruments are created..')

    print("Start testing...")
    model.eval()

    print("Saving model prediction examples")
    test_examples_list = []
    example_indexes = np.random.choice(len(dataset), 5, replace=False)
    for example_idx in example_indexes:
        image, mask_example = dataset[example_idx]
        X_example = image.unsqueeze(0).to(device)

        mask_example = mask_cvtr(mask_example, mask2id_cvtr).to(
            torch.int64).unsqueeze(0)
        logits = model(X_example)
        mask_pred_example = logits.argmax(dim=1)
        test_examples_list.append(
            (image, mask_example, mask_pred_example.to('cpu')))

    save_path = test_params['save_results_path']
    visualizer = ResultsVisualizer(config, save_path)
    test_examples_paths = visualizer.save_test_examples(*test_examples_list)
    print('Test examples are saved')
    # Остановился здесь. Нужно написать по аналогии с трейном  сохранение

    evaluator = Evaluator(loss_fn, metric, classes_amount, classes_dict)
    with torch.no_grad():

        for X_test, mask_test in tqdm.tqdm(data_ts, desc='Testing..'):

            mask_test = mask_cvtr(mask_test, mask2id_cvtr).to(
                torch.int64).to(device)
            X_test = X_test.to(device)

            logits = model(X_test)
            Y_pred = get_probabilities(logits)
            evaluator.update(Y_pred, mask_test)

    results = evaluator.get_result()
    # .get_pixels_frequency()
    results['class_counter'] = config['class_counter']
    score, loss = results['metric_all'], results['loss_all']
    print(
        f'Results of testing. Metric({metric_name}): {score}, loss({loss_name}):{loss}',)
    results["test_examples_paths"] = test_examples_paths
    gui_dict = visualizer.get_test_gui_dict(results)
    return gui_dict

def create_test_dataloader(config: dict):
    """
    Создает даталоадеры для тестирования.
    :code_assign: service
    :code_type: Глубокое обучение/Сегментация

    :packages:
        import albumentations as A
        from albumentations import Resize
        from torch.utils.data import DataLoader
    :param dict config: конфигурация создания даталоадера,
                        параметры аналогичны параметрам
                        segm_test

    """
    num_workers = int(config['num_workers'])
    size = config['imgsz']
    resize = A.Compose([Resize(size, size)])
    batch_size = int(config['batch_size'])

    dataset = SegmDataset(
        config['img_path_to_dataset'], config['mask_path_to_dataset'], config['classes_dict'], augms=resize)

    test_loader = DataLoader(
        dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    return test_loader, dataset

class ConfusionMatrix:
    """
        Класс реализуящий матрицу путаницы
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports:

        :packages:
            import torch
    """

    def __init__(self, num_classes: int):
        """
        Инициализация матрицы.
        :param num_classes: количество классов.
        """
        self.num_classes = num_classes
        self.matrix = torch.zeros(self.num_classes, self.num_classes, 2)
        self.accum_class = torch.zeros(self.num_classes)

    def fasthist(self, true, pred, num_classes):
        """
        Подсчет матрицы путаницы.
        :param true:
        :param pred:
        :param num_classes:
        :return:
        """
        mask = (true >= 0) & (true < num_classes)
        hist = (
            torch.bincount(
                num_classes * true[mask] + pred[mask],
                minlength=num_classes**2,
            )
            .reshape(num_classes, num_classes)
            .float()
        )
        return hist

    def append(self, true: torch.Tensor, pred: torch.Tensor):
        """
        Обновление матрицы путаницы в соответствии с новыми данными.
        :param true: действительные значения;
        :param pred: предсказанные значения.
        """
        true, pred = true.cpu(), pred.cpu()
        size = true.size()
        if len(size) == 1:
            self.matrix[:, :, 0] += self.fasthist(
                true.flatten(), pred.flatten(), self.num_classes
            )
        elif len(size) == 3:
            for t, p in zip(true, pred):
                self.matrix[:, :, 0] += self.fasthist(
                    t.flatten(), p.flatten(), self.num_classes
                )
        else:
            raise NameError("Недопустимая размерность входных тензоров.")

    def get_matrix(self):
        """
        Считает процент входа злементов и возвращает матрицу путаницы.
        Пример вывода матрицы путаницы:

            class_names = ['class1', 'class2', 'class3']
            layout = {
                "title": "Confusion Matrix",
                "xaxis": {"title": "y_pred"},
                "yaxis": {"title": "y_true"}
            }

            fig = go.Figure(data=go.Heatmap(z=cm,
                                            x=class_names,
                                            y=class_names,
                                            hoverongaps=True,colorscale='Blues'),
                            layout=layout)
            fig.show()

        :return: матрица путаницы.
        """
        cm = self.matrix[:, :, 0]
        cm = (cm.T / (cm.sum(axis=1))).T

        self.matrix[:, :, 1] = cm
        return self.matrix

class Evaluator:
    """
        Class Evaluator needs to evaluate the performance
        of the model on each iteration in epoch.

        Advantage of this class is that it optimizes calculations for rating
        model. It's reaches by removing saving all predictions by epoch.
        Each batch calculates separetely

        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports: ConfusionMatrix, per_class_pixel_accuracy

        :packages:
            from copy import deepcopy

    """

    def __init__(self, loss_func, metric_func, classes_amount: int, classes_dict: dict):
        self.loss = loss_func
        self.metric = metric_func
        # self.class_counter = dict([(class_name, 0)
        #                            for class_name in list(classes_dict.keys())])
        self.results = {  # 'confusion_matrix': torch.zeros((classes_amount, classes_amount)),
            'loss_all': 0, 'metric_all': 0}

        self.upd_count = 0
        self.classes_amount = classes_amount
        self.classes_dict = classes_dict
        self.cm = ConfusionMatrix(classes_amount)

    def update(self, Y_pred, true_ind):
        '''
        Calls each eppoch
        :param torch.Tensor Y_pred: prediction tensor
        :param torch.Tensor true_ind: true indexes tensor
        '''
        self.upd_count += 1

        pred_ind = Y_pred.argmax(dim=1)

        # for i, class_name in enumerate(self.classes_dict.keys()):
        #     self.class_counter[class_name] += (true_ind == i).sum()

        self.cm.append(true_ind.flatten(), pred_ind.flatten())

        self.results['loss_all'] += self.loss(Y_pred, true_ind)

        self.results['metric_all'] += self.metric(
            pred_ind, true_ind, mean=True)

    def get_result(self):
        '''
        Returns result of evaluation
        '''
        # self.results['class_counter'] = {}
        # for (class_name, count) in self.class_counter.items():
        #     self.results['class_counter'][class_name] = count.detach().cpu()
        # # values correction
        corrected_results = deepcopy(self.results)

        # [:,:,1] is normalized confusion matrix, [:,:,0] isn't
        corrected_results['conf_matrix'] = self.cm.get_matrix()
        corrected_results['per_class_pixel_accuracy'] = per_class_pixel_accuracy(
            corrected_results['conf_matrix'][:, :, 0], mean=False)

        corrected_results['loss_all'] = corrected_results['loss_all'].to('cpu').item() / \
            self.upd_count
        corrected_results['metric_all'] = corrected_results['metric_all'].to('cpu').item() / \
            self.upd_count

        return corrected_results

def per_class_pixel_accuracy(hist, mean=True):
    """Computes the average per-class pixel accuracy.

    The per-class pixel accuracy is a more fine-grained
    version of the overall pixel accuracy. A model could
    score a relatively high overall pixel accuracy by
    correctly predicting the dominant labels or areas
    in the image whilst incorrectly predicting the
    possibly more important/rare labels. Such a model
    will score a low per-class pixel accuracy.

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch


    :param torch.tensor hist: confusion matrix.

    Returns:
        avg_per_class_acc: the average per-class pixel accuracy.
    """
    correct_per_class = torch.diag(hist)
    total_per_class = hist.sum(dim=1)
    per_class_acc = correct_per_class / (total_per_class + 1e-12)
    if not mean:
        return per_class_acc
    else:
        avg_per_class_acc = nanmean(per_class_acc)
        return avg_per_class_acc

def segm_save_model(model: torch.nn.Module,
                    path: str,
                    onnx: bool = False,
                    imgsz: int = 224):
    """
    Segmentation save mode.
    Function saves a PyTorch model to a file. Availible formats: .pth, .pt, .onnx

    :code_assign: users
    :code_type: Глубокое обучение/Сегментация(сохранение)
    :imports: save_onnx, save_entire_model

    :packages:
        import torch

    :param_block torch.nn.Module model Model: model to save.
    :param str path: Path to save model
    :param bool onnx: True if need in onnx saving. Defaults to False.
    :param int imgsz: Input image size parameter. Uses only for onnx saving. Defaults to 224

    :returns:
    :rtype:
    :semrtype:
    """

    print('Saving model...')
    input_shape = (1, 3, imgsz, imgsz)
    if onnx:
        save_onnx(model, path, input_shape=input_shape)
    else:
        save_entire_model(model, path)

def save_entire_model(model: torch.nn.Module, path: str):
    '''
    Saves whole model

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch

    :param torch.nn.Module model: model for save
    :param str path: path to save model

    '''
    torch.save(model, path)

def save_onnx(model: torch.nn.Module, path: str, input_shape: tuple):
    '''
    Saves whole model to onnx format

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch

    :param torch.nn.Module model: model for save
    :param str path: path to save model
    :param Union[tuple, list] input_shape: shape for input. Needed for onnx saving

    '''
    model.eval()
    dummy_input = torch.randn(*input_shape)
    torch.onnx.export(model.to('cpu'), dummy_input, path, export_params=True)

def segm_predict(
    model: torch.nn.Module,
    path_to_images: str,
    path_to_options: str,
    path_to_save_results: str,
    imgsz: int = 224,
    device='cpu',
):
    """ Segmentation prediction pipeline

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация(предказание)
    :imports: load_classes_dict,load_params,SegmPredictDataset,mask_cvtr,cvt_torch_image_to_cv2_image,cvt_cv2_image_to_torch_image,ResultsVisualizer


    :packages:
        import tqdm
        import albumentations as A
        import os
        from albumentations import Resize
    :param_block torch.nn.Module model Model: model to test.

    :param str path_to_images: path to images folder.
    :param str path_to_options: path to options.json file.
    :param str path_to_save_results: path to save predictions.

    :param str device: Name of device for training. Possible values 'cpu', 'cuda:0', 'cuda:1', etc. Defaults to 'cpu'. Параметр является вспомогательным для настройки проекта. Нежелательно, чтобы конечный пользователь имел доступ к этому параметру

    :param int imgsz: Size of images for model input. Defaults to 224

    :returns:
    :rtype:
    :semrtype:
    """

    print('Predict mode is enabled..')
    config = locals()  # converts input arguments to dict
    config['mode'] = 'predict'
    config['classes_dict'] = load_classes_dict(path_to_options)

    test_params = load_params(config)

    resize_to_model_input = A.Compose([Resize(imgsz, imgsz)])
    dataset = SegmPredictDataset(path_to_images, resize_to_model_input)

    device = test_params['device']

    classes_dict = load_classes_dict(path_to_options)  # config['classes_dict']
    id2mask_cvtr = dict([(i, value)
                         for i, (key, value) in enumerate(classes_dict.items())])  # predict format to dataset format converter

    classes_amount = len(classes_dict.keys())
    visualizer = ResultsVisualizer()
    model.to(device)
    print('Predict instruments are created..')

    print("Start prediction...")
    model.eval()

    for idx in tqdm.tqdm(range(len(dataset))):
        image, info = dataset[idx]
        image_path = dataset.img_list[idx]
        image_name = os.path.basename(image_path)
        save_image_path = os.path.join(path_to_save_results, image_name)
        X_example = image.unsqueeze(0).to(device)
        logits = model(X_example)
        mask_pred = logits.argmax(dim=1)
        mask_pred = mask_pred.detach().to('cpu')
        mask = mask_cvtr(
            mask_pred, id2mask_cvtr)
        resize_to_orig_pic_shape = A.Compose(
            [Resize(info['shape'][0], info['shape'][1])])
        preproc_data = resize_to_orig_pic_shape(
            image=cvt_torch_image_to_cv2_image(image), mask=cvt_torch_image_to_cv2_image(mask))

        mask = preproc_data["mask"].squeeze(2)
       # print(mask.shape)
        # mask = cvt_cv2_image_to_torch_image(mask)
     #   mask_dataset_format = torch.cat(
      #      [mask, mask, mask], dim=0)
        visualizer.save_pic(
            mask, save_image_path, using_pillow=True)

    return

class SegmPredictDataset(torch_dataset):
    """
        class Dataset for predict mode
        :code_assign: service
        :code_type: Глубокое обучение/Сегментация

        :imports: check_for_dims

        :packages:
            from torch.utils.data import Dataset as torch_dataset
            import glob
            import tqdm
            import os
            import numpy as np
            from torchvision.transforms.functional import to_tensor
            from PIL import Image
    """

    def __init__(
        self, img_path: str,
        augms=None
    ):
        """
        Инициализация класса датасета(train|test).
        :param str img_path: Путь до папки с картинками
        :param albumentations.core.composition.Compose augms: аугментации,
            которые долны быть применены к каждой картинке в датасете.
            Пример - Resize
        """
        self.augs = augms
        self.img_formats = ['jpg', 'jpeg', 'png']
        self.img_list = self.get_pics_list(img_path)

    def get_pics_list(self, path):
        '''
        Возвращает список изображений с указанными форматами
        :param str path: Путь до папки с изображениями
        '''
        img_list = []
        for img_format in self.img_formats:
            img_format_list = glob.glob(f'{path}/*.{img_format}')
            if len(img_format_list) != 0:
                img_list = img_list + img_format_list
        return img_list

    def __len__(self):
        return len(self.img_list)

    def __getitem__(self, index):
        orig_image = check_for_dims(np.array(Image.open(self.img_list[index])))
        shape = orig_image.shape
        preproc_data = self.augs(
            image=orig_image) if self.augs else None
        if self.augs:
            image = preproc_data["image"]
        else:
            image = orig_image
        image = to_tensor(image)

        return image, {"shape": shape, "orig_image": orig_image}


def segm_load_model(path: str):
    '''
    Loads whole model

    :code_assign: service
    :code_type: Глубокое обучение/Сегментация
    :packages:
        import torch

    :param str path: path to load model from
    '''
    return torch.load(path)


def optimization(trial):
    """
    Функция для оптимизации гиперпараметров с помощью optuna
    """
    # Пробуем различные значения гиперпараметров
    batch_size = trial.suggest_categorical('batch_size', [8, 16, 32])
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-2)  # 1e-5, 1e-2
    num_workers = trial.suggest_int('num_workers', 0, 4)
    epochs = trial.suggest_int('epochs', 5, 100)         # 5, 20
    # loss = trial.suggest_categorical('loss', ['focal', 'cross_entropy'])
    optimizer = trial.suggest_categorical('optimizer', ['AdamW', 'SGD'])

    # Параметры аугментации
    VerticalFlip = trial.suggest_uniform('VerticalFlip', 0.0, 1.0)
    HorizontalFlip = trial.suggest_uniform('HorizontalFlip', 0.0, 1.0)
    scale_limit = trial.suggest_uniform('scale_limit', -0.5, 0.5)   # -0.5, 0.5
    rotate_limit = trial.suggest_int('rotate_limit', 0, 45)
    blur = trial.suggest_uniform('blur', 0.0, 1.0)

    # Конфигурация для обучения
    train_config = {
        'path_to_dataset': path_to_dataset,
        'imgsz': 224,
        'device': 'cuda:0',
        'num_workers': num_workers,
        'batch_size': batch_size,
        'epochs': epochs,
        'metric': 'IoU',
        'lr': lr,
        'loss': 'focal',
        'optimizer': optimizer,
        'model': 'deeplabv3_resnet50',
        'VerticalFlip': VerticalFlip,
        'HorizontalFlip': HorizontalFlip,
        'scale_limit': [scale_limit, -scale_limit],
        'rotate_limit': rotate_limit,
        'blur': blur
    }

    # Запускаем обучение
    model, train_results, gui_dict = segm_train(**train_config)

    # Получаем значение IoU
    iou = train_results['val_scores'][-1]  # Берем метрику последней эпохи

    return iou

def check_pickling(model, path_to_dataset):
    pickled_object = dill.dumps(model)
    pickled_model = dill.loads(pickled_object)
    test_config = {
        'imgsz': 224,
        'metric': 'IoU',
        'loss': 'focal',
        'device': 'cuda:0',
        'path_to_dataset': path_to_dataset,
        'num_workers': 0,
    }
    pickled_model = dill.loads(pickled_object)

    gd = segm_test(pickled_model, **test_config)

    segm_predict(pickled_model, path_to_images=f"{path_to_dataset}/images", path_to_options=f"{path_to_dataset}/options.json",
                 path_to_save_results=predict_result_path, device='cuda:0')

    segm_save_model(
        pickled_model, f'{save_result_path}/model.pth')
    # segm_save_model(
    #     pickled_model, 'launch_examples/save_mode_example/model.onnx', onnx=True, imgsz=224)
