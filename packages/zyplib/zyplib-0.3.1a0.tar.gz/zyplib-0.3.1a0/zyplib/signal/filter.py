from typing import Literal, Union

import numpy as np
from scipy import fft, signal

from zyplib.utils.ensure import ensure_npy

FilterType = Literal['butter', 'cheby1', 'cheby2', 'ellip', 'bessel']


def notch(X, fs, f0=50, Q=30, axis=-1):
    r"""Notch filter.
    
        Parameters
        ----------
            - signals : array_like
                - Input signal.
            - fs : float
                - Sampling frequency.
            - f0 : float
                - Notch frequency.
            - Q : float, optional
                - Q factor. Default is 30.
                - https://en.wikipedia.org/wiki/Q_factor
                - $Q = \frac{f_0}{\Delta f}$
            - axis : int, optional
                - Axis along which to apply the filter. Default is -1.
    
        Returns
        ----------
            - y : ndarray
                - Filtered signal.
    """
    X = ensure_npy(X)
    b, a = signal.iirnotch(f0, Q, fs)
    return signal.lfilter(b, a, X, axis=axis)


def bandpass_butter(X, fs: float, lfreq: float, rfreq: float, order=5, axis=-1):
    r"""Bandpass filter.

        Parameters
        ----------
            - signals : array_like
                - Input signal.
            - fs : float
                - Sampling frequency.
            - lfreq : float
                - Left frequency.
            - rfreq : float
                - Right frequency.
            - order : int, optional
                - Filter order. Default is 5.
            - axis : int, optional
    
        Returns
        ----------
            - y : ndarray
                - Filtered signal.
    """
    X = ensure_npy(X)
    nyq = 0.5 * fs
    low = lfreq / nyq
    high = rfreq / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return signal.lfilter(b, a, X, axis=axis)
