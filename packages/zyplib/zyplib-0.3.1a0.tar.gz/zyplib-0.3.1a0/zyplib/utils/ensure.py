from functools import singledispatch
from typing import Union

import numpy as np
import torch

__all__ = [
    "ensure_3dims",
    "ensure_2dims",
    "ensure_npy",
    "ensure_tensor"
]


def ensure_npy(data: Union[np.ndarray, torch.Tensor, list]):
    """确保 data 是 np.ndarray 格式
    
        Parameters
        ----------
            - `data` : Union[np.ndarray, torch.Tensor, list]
                - 输入的数据
    
        Returns
        ----------
            - `np.ndarray`
                - 将输入的数据转换为 np.ndarray 格式
    """
    if isinstance(data, np.ndarray):
        return data
    elif isinstance(data, torch.Tensor):
        return data.detach().cpu().numpy()
    elif isinstance(data, list):
        return np.array(data)
    else:
        raise TypeError(
            f"signals should be np.ndarray or torch.Tensor, but got {type(data)}"
        )


def ensure_tensor(data: Union[np.ndarray, torch.Tensor, list]):
    """确保 data 是 torch.Tensor 格式
    
        Parameters
        ----------
            - `data` : Union[np.ndarray, torch.Tensor, list]
                - 输入的数据
    
        Returns
        ----------
            - `torch.Tensor`
                - 将输入的数据转换为 torch.Tensor 格式
    """
    if isinstance(data, np.ndarray):
        return torch.from_numpy(data)
    elif isinstance(data, torch.Tensor):
        return data.detach().cpu()
    elif isinstance(data, list):
        return torch.tensor(data)
    else:
        raise TypeError(
            f"signals should be np.ndarray or torch.Tensor, but got {type(data)}"
        )


@singledispatch
def ensure_3dims(signals: Union[np.ndarray, torch.Tensor], batch_first: bool = True):
    """把数据转换为标准的 [Batch, C, T] 格式
    
        Parameters:
        ----------
            - `signals`: np.ndarray | torch.Tensor, 信号张量, shape 可以为 [T] 或者 [N, T]
            - `batch_first`: bool;
                当 `signals` 为  [N, T] 时
                如果 为 True, 则把 N 看作 batch_size; 否则看作 channel
    """
    ...


@ensure_3dims.register(np.ndarray)
def _ensure_3dims_npy(signals: np.ndarray, batch_first: bool = True):

    if signals.ndim != 3:
        if signals.ndim == 1:
            signals = signals[np.newaxis, np.newaxis, :]
        elif signals.ndim == 2:
            if batch_first:
                signals = signals[:, np.newaxis, :]
            else:
                signals = signals[np.newaxis, :, :]
        else:
            raise ValueError(f"signals.ndim should be 1 or 2, but got {signals.ndim}")
    return signals


@ensure_3dims.register(torch.Tensor)
def _ensure_3dims_torch(signals: torch.Tensor, batch_first: bool = True):
    if signals.ndim != 3:
        if signals.ndim == 1:
            signals = signals.unsqueeze(0).unsqueeze(0)
        elif signals.ndim == 2:
            if batch_first:
                signals = signals.unsqueeze(1)
            else:
                signals = signals.unsqueeze(0)
        else:
            raise ValueError(f"signals.ndim should be 1 or 2, but got {signals.ndim}")
    return signals


@singledispatch
def ensure_2dims(signals: Union[np.ndarray, torch.Tensor]):
    """把数据转换为标准的 [Batch, T] 格式
    
        Parameters:
        ----------
            - `signals`: np.ndarray | torch.Tensor, 信号张量, shape 可以为 [T] 或者 [N, T]
    """
    ...


@ensure_2dims.register(np.ndarray)
def _ensure_2dims_npy(signals: np.ndarray):
    if signals.ndim != 2:
        if signals.ndim == 1:
            signals = signals[np.newaxis, :]
        else:
            signals = signals.squeeze()
            if signals.ndim == 2:
                ...
            elif signals.ndim == 1:
                signals = signals[np.newaxis, :]
            else:
                raise ValueError(f"signals.ndim should be 1 or 3, but got {signals.ndim}")
    return signals


@ensure_2dims.register(torch.Tensor)
def _ensure_2dims_torch(signals: torch.Tensor):
    if signals.ndim != 2:
        if signals.ndim == 1:
            signals = signals.unsqueeze(0)
        else:
            signals = signals.squeeze()
            if signals.ndim == 2:
                ...
            elif signals.ndim == 1:
                signals = signals.unsqueeze(0)
            else:
                raise ValueError(f"signals.ndim should be 1 or 3, but got {signals.ndim}")
    return signals
