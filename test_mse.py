import os.path as osp
import sys
from glob import glob

import cv2
import numpy as np
import theano
from keras.models import model_from_json

theano.config.openmp = True


BATCH_SIZE = 1


def load_model():
    with open("./erika.json", "r") as f:
        loaded_model_json = f.read()

    model = model_from_json(loaded_model_json)
    model.load_weights("./erika_unstable.h5")
    return model


def test():
    model = load_model()

    for path in sorted(glob(osp.join(sys.argv[1], "**", "*.jpg"))):
        print(path)

        src = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        rows = int(src.shape[0] / 16 + 1) * 16
        cols = int(src.shape[1] / 16 + 1) * 16

        patch = np.empty((1, 1, rows, cols), dtype="float32")
        patch[0, 0, :, :] = np.ones((rows, cols), dtype="float32") * 255.0
        patch[0, 0, 0 : src.shape[0], 0 : src.shape[1]] = src

        out = model.predict(patch, batch_size=BATCH_SIZE)
        if isinstance(out, list):
            out = out[0]

        result = np.zeros((rows, cols), dtype=np.float32)
        result = out[0, 0, :, :]
        result[result > 255] = 255
        result[result < 0] = 0

        cv2.imwrite(
            osp.join(sys.argv[2], osp.basename(path)),
            result[0 : src.shape[0], 0 : src.shape[1]],
        )


if __name__ == "__main__":
    test()
