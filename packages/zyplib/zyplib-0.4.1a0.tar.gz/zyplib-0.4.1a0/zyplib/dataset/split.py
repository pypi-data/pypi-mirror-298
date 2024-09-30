import random
from typing import Any, List, Tuple, Union

import numpy as np


def random_split(
    data: Union[List[Any], np.ndarray],
    *,
    proportion: float = 0.7,
    count: int = None,
    seed: int = None,
) -> Tuple[Union[List[Any], np.ndarray], Union[List[Any], np.ndarray]]:
    """随机二分数据集

    ```py
    # first_part 占用 70%，second_part 占用 30%
    first_part, second_part = random_split(data, proportion=0.7)
    ```

    Parameters
    ----------
    - `data` : `Union[List[Any], np.ndarray]`
        - 需要切分的数据
    - `proportion` : `float`, optional
        - 第一部分的比例, by default 0.7
    - `count` : `int`, optional
        - 第一部分的个数，如果设置了，则覆盖 proportion 的设置, by default None
    - `seed` : `int`, optional
        - 随机种子

    Returns
    ----------
    - `Tuple[Union[List[Any], np.ndarray], Union[List[Any], np.ndarray]]`
        - 返回两个列表或数组，第一个是第一部分，第二个是第二部分
    """
    if seed:
        # Set the random seed for reproducibility
        random.seed(seed)
        np.random.seed(seed)

    # Determine the size of the first part
    if count is not None:
        first_part_size = count
    else:
        first_part_size = int(len(data) * proportion)

    # Handle list
    if isinstance(data, list):
        shuffled_data = data[:]
        random.shuffle(shuffled_data)
        first_part = shuffled_data[:first_part_size]
        second_part = shuffled_data[first_part_size:]

    # Handle numpy array
    elif isinstance(data, np.ndarray):
        shuffled_indices = np.random.permutation(len(data))
        shuffled_data = data[shuffled_indices]
        first_part = shuffled_data[:first_part_size]
        second_part = shuffled_data[first_part_size:]

    else:
        raise TypeError('Data must be a list or numpy array')

    return first_part, second_part
