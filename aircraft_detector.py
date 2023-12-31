import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model


class Model:
    def __init__(self):
        self.__model_final = None
        self.load_model()

    def load_model(self):
        self.__model_final = load_model('ieeercnn_vgg16_1.h5')

    def process_image(self, path):
        cv2.setUseOptimized(True)
        ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

        img = cv2.imread(path)
        ss.setBaseImage(img)
        ss.switchToSelectiveSearchFast()
        ssresults = ss.process()
        imout = img.copy()
        print(len(ssresults))
        for e, result in enumerate(ssresults):
            if e < 2000:
                x, y, w, h = result
                timage = imout[y:y + h, x:x + w]
                resized = cv2.resize(timage, (224, 224), interpolation=cv2.INTER_AREA)
                img = np.expand_dims(resized, axis=0)
                out = self.__model_final.predict(img)
                if out[0][0] > 0.70:
                    cv2.rectangle(imout, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
        fig = plt.gcf()
        plt.axis('off')
        plt.imshow(imout)
        result_filename = 'result_' + str(get_file_sequence()) + '.png'
        fig.savefig(result_filename, bbox_inches='tight')
        return result_filename


def get_file_sequence():
    reader = open('file_sequence.txt', 'r')
    current_sequence = int(reader.readline())
    reader.close()

    writer = open('file_sequence.txt', 'w')
    writer.write(str(current_sequence + 1))
    writer.close()

    return current_sequence
