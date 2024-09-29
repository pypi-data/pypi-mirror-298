import os
from typing import Any, Dict, Optional

import torch
import torchaudio
from torch.utils.data import Dataset

from .._common.dataset import BirdCLEFPrimaryLabelDataset

__all__ = [
    "BirdCLEF2024PrimaryLabelDataset",
    "BirdCLEF2024AudioDataset",
]


class BirdCLEF2024PrimaryLabelDataset(BirdCLEFPrimaryLabelDataset):
    """Dataset for training of bird classification model in BirdCLEF2024.

    Args:
        list_path (str): Path to list file. Each entry represents path to audio file
            without extension such as ``asbfly/XC49755``.
        feature_dir (str): Path to dataset containing ``train_metadata.csv`` file,
            ``train_audio`` directory, and so on.
        audio_key (str): Key of audio.
        sample_rate_key (str): Key of sampling rate.
        label_name_key (str): Key of prmary label name in given sample.
        filename_key (str): Key of filename in given sample.
        decode_audio_as_waveform (bool, optional): If ``True``, audio is decoded as waveform
            tensor and sampling rate is ignored. Otherwise, audio is decoded as tuple of
            waveform tensor and sampling rate. Default: ``True``.
        decode_audio_as_monoral (bool, optional): If ``True``, decoded audio is treated as
            monoral waveform of shape (num_samples,) by reducing channel dimension. Otherwise,
            shape of waveform is (num_channels, num_samples), which is returned by
            ``torchaudio.load``. Default: ``True``.

    """


class BirdCLEF2024AudioDataset(Dataset):
    """Dataset for inference of bird classification model.

    Args:
        list_path (str): Path to list file. Each entry represents path to audio file
            without extension such as ``soundscape_ABCDE``.
        feature_dir (str): Path to dataset containing ``sample_submission.csv`` file,
            ``test_soundscapes`` directory, and so on.
        audio_key (str): Key of audio.
        sample_rate_key (str): Key of sampling rate.
        filename_key (str): Key of filename in given sample.
        decode_audio_as_waveform (bool, optional): If ``True``, audio is decoded as waveform
            tensor and sampling rate is ignored. Otherwise, audio is decoded as tuple of
            waveform tensor and sampling rate. Default: ``True``.
        decode_audio_as_monoral (bool, optional): If ``True``, decoded audio is treated as
            monoral waveform of shape (num_samples,) by reducing channel dimension. Otherwise,
            shape of waveform is (num_channels, num_samples), which is returned by
            ``torchaudio.load``. Default: ``True``.

    """

    def __init__(
        self,
        list_path: str,
        feature_dir: str,
        audio_key: str = "audio",
        sample_rate_key: str = "sample_rate",
        filename_key: str = "filename",
        decode_audio_as_waveform: Optional[bool] = None,
        decode_audio_as_monoral: Optional[bool] = None,
    ) -> None:
        super().__init__()

        audio_root = os.path.join(feature_dir, "test_soundscapes")

        self.audio_root = audio_root
        self.list_path = list_path

        self.audio_key = audio_key
        self.sample_rate_key = sample_rate_key
        self.filename_key = filename_key

        if decode_audio_as_waveform is None:
            decode_audio_as_waveform = True

        if decode_audio_as_monoral is None:
            decode_audio_as_monoral = True

        self.decode_audio_as_waveform = decode_audio_as_waveform
        self.decode_audio_as_monoral = decode_audio_as_monoral

        filenames = []

        with open(list_path) as f:
            for line in f:
                filename = line.strip()
                filenames.append(filename)

        self.filenames = filenames

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        audio_root = self.audio_root
        filename = self.filenames[idx]

        audio_path = os.path.join(audio_root, f"{filename}.ogg")
        waveform, sample_rate = torchaudio.load(audio_path)

        if self.decode_audio_as_monoral:
            waveform = waveform.mean(dim=0)

        if self.decode_audio_as_waveform:
            audio = waveform
        else:
            audio = waveform, sample_rate

        sample_rate = torch.tensor(sample_rate, dtype=torch.long)

        feature = {
            self.audio_key: audio,
            self.sample_rate_key: sample_rate,
            self.filename_key: filename,
        }

        return feature

    def __len__(self) -> int:
        return len(self.filenames)
