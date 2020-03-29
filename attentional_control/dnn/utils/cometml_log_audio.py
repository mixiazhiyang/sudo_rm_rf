"""!
@brief Log audio files from a given batch in cometml experiment

@author Efthymios Tzinis {etzinis2@illinois.edu}
@copyright University of Illinois at Urbana-Champaign
"""

import os
import numpy as np
from scipy.io.wavfile import write as wavwrite


class AudioLogger(object):
    def __init__(self, fs=8000, bs=4, n_sources=2):
        """
        :param dirpath: The path where the audio would be saved.
        :param fs: The sampling rate of the audio in Hz
        :param bs: The number of samples in batch
        :param n_sources: The number of sources
        """
        self.fs = int(fs)
        self.bs = int(bs)
        self.n_sources = int(n_sources)

    def log_batch(self,
                  pr_batch,
                  t_batch,
                  mix_batch,
                  experiment,
                  step=None):
        """!
        :param pr_batch: Reconstructed wavs: Torch Tensor of size:
                         batch_size x num_sources x length_of_wavs
        :param t_batch: Target wavs: Torch Tensor of size:
                        batch_size x num_sources x length_of_wavs
        :param mix_batch: Batch of the mixtures: Torch Tensor of size:
                          batch_size x 1 x length_of_wavs
        :param experiment: Cometml experiment object
        :param step: The step that this batch belongs
        """
        print('Logging audio online...\n')
        mixture = mix_batch.detach().cpu().numpy()
        true_sources = t_batch.detach().cpu().numpy()
        pred_sources = pr_batch.detach().cpu().numpy()

        for b_ind in range(self.bs):
            experiment.log_audio(mixture[b_ind].squeeze(),
                                 sample_rate=self.fs,
                                 file_name='batch_{}_mixture'.format(b_ind+1),
                                 metadata=None, overwrite=False,
                                 copy_to_tmp=True, step=step)
            for s_ind in range(self.n_sources):
                experiment.log_audio(true_sources[b_ind].squeeze(),
                                     sample_rate=self.fs,
                                     file_name='batch_{}_source_{}_true'.format(
                                         b_ind+1, s_ind+1),
                                     metadata=None, overwrite=False,
                                     copy_to_tmp=True, step=step)
                experiment.log_audio(pred_sources[b_ind].squeeze(),
                                     sample_rate=self.fs,
                                     file_name='batch_{}_source_{}_est'.format(
                                         b_ind+1, s_ind+1),
                                     metadata=None, overwrite=False,
                                     copy_to_tmp=True, step=step)
