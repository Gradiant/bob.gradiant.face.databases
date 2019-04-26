#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain

import numpy as np
from bob.gradiant.core import VideoAccess


COMMON_PAI_CATEGORISATION = {'real': 0,
                             'print': {'low_quality': 1,  # dpi <= 600
                                       'medium_quality': 2,  # 609 < dpi <= 1000
                                       'high_quality': 3  # dpi > 1000
                                       },
                             'replay': {'low_quality': 4,  # res <= 480p
                                        'medium_quality': 5,  # 480p < res < 1080p
                                        'high_quality': 6  # res >= 1080p
                                        },
                             'mask': {'paper': 7,  # paper masks
                                      'rigid': 8,  # non-flexible plaster-like
                                      'silicone': 9  # silicone mask
                                      }
                             }

COMMON_CAPTURE_DEVICE_CATEGORISATION = {'webcam': {'low_quality': 0,  # SD res
                                                   'high_quality': 1  # HD res
                                                   },
                                        'mobile': {'low_quality': 2,  # SD res
                                                   'high_quality': 3  # HD res
                                                   },
                                        'tablet': {'low_quality': 2,  # SD res
                                                   'high_quality': 3  # HD res
                                                   },
                                        'digital_camera': {'low_quality': 4,
                                                           'high_quality': 5}
                                        }

COMMON_LIGHTNING_CATEGORISATION = {'controlled': 0,  # indoors controlled
                                   'adverse': 1,  # outdoors, indoors with extra lightning
                                   'no_info': 2,  # non labeled info or not general DB condition
                                   }

COMMON_FACE_RESOLUTION_CATEGORISATION = {'small_face': 0,   # IED <= ? px
                                         'medium_face': 1,  # ? px < IED <= ? px
                                         'big_face': 2      # IED > ? px
                                         }

COMMON_CATEGORISATION = {'common_pai': COMMON_PAI_CATEGORISATION,
                         'common_capture_device': COMMON_CAPTURE_DEVICE_CATEGORISATION,
                         'common_lightning': COMMON_LIGHTNING_CATEGORISATION,
                         'common_face_resolution':  COMMON_FACE_RESOLUTION_CATEGORISATION
                         }

AGGREGATE_DATABASE_AVAILABLE_LABELS = {'common_pai': {'real': [0],
                                                      'print': range(1, 4),
                                                      'replay': range(4, 7),
                                                      'mask': range(7, 10)
                                                      },
                                       'common_capture_device': {'webcam': range(0, 2),
                                                                 'mobile': range(2, 4),
                                                                 'tablet': range(2, 4),
                                                                 'digital_camera': range(5, 6)
                                                                 },
                                       'common_lightning': {'controlled': [0],
                                                            'adverse': [1],
                                                            'no_info': [2]
                                                            },
                                       'common_face_resolution': {'small_face': [0],
                                                                  'medium_face': [1],
                                                                  'big_face': [2]
                                                                  }
                                       }


def get_common_face_resolution(access):
    ied_all_frames = []

    try:
        dict_keyframes_annotations = VideoAccess.read_mtcnn_annotations(access + '.h5')
    except IOError:
        print('Unable to find mtcnn annotations for access {}'. format(access))
        return -1

    for keyframe in dict_keyframes_annotations:
        left_eye = (dict_keyframes_annotations[keyframe][4], dict_keyframes_annotations[keyframe][5])
        right_eye = (dict_keyframes_annotations[keyframe][6], dict_keyframes_annotations[keyframe][7])
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        ied = int(np.sqrt((dx ** 2) + (dy ** 2)))
        ied_all_frames.append(ied)

    mean_access_iec = sum(ied_all_frames) / len(ied_all_frames)

    if mean_access_iec < 120.0:  # ISO-IEC 19745-5
        common_face_resolution = COMMON_FACE_RESOLUTION_CATEGORISATION['small_face']

    elif mean_access_iec > 240.0:
        common_face_resolution = COMMON_FACE_RESOLUTION_CATEGORISATION['big_face']

    else:
        common_face_resolution = COMMON_FACE_RESOLUTION_CATEGORISATION['medium_face']

    return common_face_resolution
