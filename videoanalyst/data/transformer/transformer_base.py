# -*- coding: utf-8 -*-

import json
import pickle
import tarfile
import time
from abc import ABCMeta, abstractmethod
from typing import List, Dict

import cv2 as cv
import nori2 as nori
import numpy as np

from yacs.config import CfgNode

from videoanalyst.utils import Registry

TRACK_TRANSFORMERS = Registry()


class TransformerBase:
    __metaclass__ = ABCMeta

    r"""
    base class for Sampler. Reponsible for sampling from multiple datasets and forming training pair / sequence.

    Define your hyper-parameters here in your sub-class.
    """
    default_hyper_params = Dict()

    def __init__(self, cfg: CfgNode, seed: int=0) -> None:
        r"""
        Transformer, reponsible for data augmentation

        Arguments
        ---------
        cfg: CfgNode
            training config, including cfg for data / model
        seed: int
            seed to initialize random number generator
            important while using multi-worker data loader
        """
        self._hyper_params = self.default_hyper_params
        self._state = Dict()
        self._cfg = cfg
        self._state["rng"] = np.random.RandomState(seed)

    def get_hps(self) -> Dict:
        r"""
        Getter function for hyper-parameters

        Returns
        -------
        Dict
            hyper-parameters
        """
        return self._hyper_params

    def set_hps(self, hps: Dict) -> None:
        r"""
        Set hyper-parameters

        Arguments
        ---------
        hps: Dict
            Dict of hyper-parameters, the keys must in self.__hyper_params__
        """
        for key in hps:
            if key not in self._hyper_params:
                raise KeyError
            self._hyper_params[key] = hps[key]

    def __call__(self, Dict) -> Dict:
        r"""
        An interface to transform data

        Arguments
        ---------
        Dict
            data to transform
        """