#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   eeg2timefreq 
@Time        :   2024/9/20 19:04
@Author      :   Xuesong Chen
@Description :   
"""
from wuji.biosignal_transformer.utils import get_normalized_timefrequency


def get_eeg_feature(
        sigal,
        fs,
        seg_duration=1,
        seg_overlap_ratio=0.5,
        min_frequency=0.3,
        max_frequency=35,
):
    return get_normalized_timefrequency(
        sigal,
        fs,
        seg_duration=seg_duration,
        seg_overlap_ratio=seg_overlap_ratio,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        log=True
    )
