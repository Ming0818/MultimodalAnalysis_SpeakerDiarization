﻿# !/usr/bin/env python3

import os
import numpy as np
import pandas as pd
from SpeechFeatures import video_to_audio
from SpeechFeatures import StereoToMono
from SpeechFeatures import ExtractFeatures
from MouthDetection import mouthDetection
from FaceDetection import face_detection


def main():
    path = '/home/eleni/Desktop/Multimodal'   #'/Users/thanasiskaridis/Desktop/multimodal_/full_videos/'
    files = os.listdir(path)
    audio_features = []
    mouth_features = []
    face_features = []
    for f in files:
        if f[-3:] == "mp4":
            video_to_audio(f)
            wavFile = f[:-3]+'wav' 
            monoWav = StereoToMono(wavFile)
            mt_feats_normal = ExtractFeatures(monoWav)
            for sec_features in mt_feats_normal:
                audio_features.append(sec_features)
            mouth_feats = mouthDetection(path, f)      
#            print (mouth_feats)			
            for sec_features in mouth_feats:
                mouth_features.append(sec_features)
            face_feats = face_detection(path, f)
            for sec_features in face_feats:
                face_features.append(sec_features)
    final_audio_features = pd.DataFrame(np.row_stack(audio_features))
    final_audio_features.to_csv('final_audio_features.csv', sep = ',', header=None, index=False)
    final_mouth_features = pd.DataFrame(np.row_stack(mouth_features))
    final_mouth_features.to_csv('final_mouth_features.csv', sep = ',', header=None, index=False)
    final_face_features = pd.DataFrame(np.row_stack(face_features))
    final_face_features.to_csv('final_face_features.csv', sep = ',', header=None, index=False)

if __name__ == '__main__':
    main()


