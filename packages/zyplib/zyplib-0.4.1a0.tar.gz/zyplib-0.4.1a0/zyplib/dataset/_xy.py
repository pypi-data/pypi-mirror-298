from typing import Callable, Union

import numpy as np

__all__ = ['make_Xy_pipeline']


def make_Xy_pipeline(
    files: list[str],
    fn_read: Callable[[str], np.ndarray],
    fn_segment: Callable[[np.ndarray], np.ndarray],
    label: Union[int, Callable[[str], int]],
    fn_before_segment: Callable[[np.ndarray], np.ndarray] = None,
    fn_after_segment: Callable[[np.ndarray], np.ndarray] = None,
):
    """从文件中读取数据，并自动切片、制作用于训练的数据集

    本函数适用于常规的脑电深度学习模型前期处理布置，包括:

    1. 从文件中读取完整的数据 X
    2. 对数据 X 进行预处理
    3. 对数据 X 进行切片
    4. 对数据 X 进行后处理
    5. 制作标签 y
    6. 返回数据集 (X, y)

    Parameters
    ----------
    - `files` : `list[str]`
        - 文件路径列表
    - `fn_read` : `(file_path: str) -> np.ndarray`
        - 文件读取函数
    - `fn_segment` : `(signal: np.ndarray) -> np.ndarray`
        - 数据切片函数
        - 输入一个 `[C, T]` 的信号
        - 输出一个 `[N, C, T]` 的信号
    - `label` : `int | (file_path: str) -> int`
        - 标签，如果为 int，则所有数据标签相同；如果为函数，则根据文件名生成标签
    - `fn_before_segment` : `(signal: [C, T]) -> [C, T]`, optional
        - 数据切片前的处理函数
    - `fn_after_segment` : `(signal: [N, C, T]) -> [N, C, T]`, optional
        - 数据切片后的处理函数

    Returns
    ----------
    - `X` : `np.ndarray`, shape = (N, C, T)
        - 数据
    - `y` : `np.ndarray`, shape = (N,)
        - 标签
    """
    if not files:
        raise ValueError('The files list is empty. Please provide at least one file.')

    fn_before_segment = fn_before_segment or (lambda x: x)
    fn_after_segment = fn_after_segment or (lambda x: x)

    label = label if callable(label) else (lambda _: label)

    # 首先从文件中读取所有数据
    data = map(fn_read, files)

    # 然后切分数据

    all_segments = []
    labels = []
    for signal, fname in zip(data, files):
        signal = fn_before_segment(signal)  # 数据预处理
        segments = fn_segment(signal)  # 数据切片
        segments = fn_after_segment(segments)  # 数据后处理
        all_segments.append(segments)
        N = len(segments)
        label_ = label(fname)
        labels.extend([label_] * N)

    X = np.concatenate(all_segments, axis=0)
    y = np.array(labels, dtype=int)
    return X, y
