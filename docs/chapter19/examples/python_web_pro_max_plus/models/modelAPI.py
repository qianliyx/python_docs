import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import platform
import matplotlib
if platform.platform().lower().startswith('linux'):
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
#指定默认字体
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

import numpy as np
import paddlehub as hub
from .visualize import visualize_detection




class modelAPI(object):
    def __init__(self):
        self.personmaskmodel = hub.Module(name="pyramidbox_lite_mobile_mask")
        self.personobjmodel = hub.Module(name="pyramidbox_lite_mobile")
        self.allobjmodel = hub.Module(name="yolov3_mobilenet_v1_coco2017")
        self.ocrmodel = hub.Module(name="chinese_ocr_db_crnn_mobile")


    def detPersonObj(self,image,rate=0.6,save_dir=None):
        res = self.personobjmodel.face_detection(images=[image],visualization=False,confs_threshold=rate)
        newres = [{"category":"face","score": float(x['confidence']),"bbox":[x['left'],x['top'],x['right']-x['left'],x['bottom']-x['top']]} for x in res[0]['data']]
        image = visualize_detection(image, newres, threshold=rate,save_dir=save_dir)
        return image,newres

    def detAllObj(self,image,rate=0.5,save_dir=None):
        res = self.allobjmodel.object_detection(images=[image],score_thresh=rate,visualization=False)
        newres = [{"category":x['label'],"score": x['confidence'],"bbox":[x['left'],x['top'],x['right']-x['left'],x['bottom']-x['top']]} for x in res[0]['data']]
        image = visualize_detection(image, newres, threshold=rate,save_dir=save_dir)
        allres = {}
        for x in newres:
            if x['category'] not in list(allres.keys()):
                allres[x['category']] = 1
            else:
                allres[x['category']] += 1
        allres = [{'category': x, 'score': y} for x,y in allres.items()]
        return image,allres


    def detPersonMask(self,image,rate=0.2,save_dir=None):
        """检测口罩"""
        res = self.personmaskmodel.face_detection(images=[image],confs_threshold=rate,visualization=False)
        newres = [{"category":"mask","score": float(x['confidence']),"bbox":[x['left'],x['top'],x['right']-x['left'],x['bottom']-x['top']]} for x in res[0]['data'] if x['label'].lower()=='mask']
        image = visualize_detection(image, newres, threshold=rate,save_dir=save_dir)
        return image,newres


    def recOCR(self,image,rate=0.5,save_dir=None):
        """通用OCR"""
        res = self.ocrmodel.recognize_text(images=[image],box_thresh=0.5,text_thresh=rate,visualization=False)
        newres = []
        for x in res[0]['data']:
            xbbox = [y[0] for y in x['text_box_position']]
            xmin,xmax = min(xbbox),max(xbbox)
            ybbox = [y[-1] for y in x['text_box_position']]
            ymin,ymax = min(ybbox),max(ybbox)
            bbox = [xmin,ymin,xmax-xmin,ymax-ymin]
            item = {
                "category":x['text'],
                "score": float(x['confidence']),
                "bbox": bbox
            }
            newres.append(item)
        image = visualize_detection(image, newres, threshold=rate,save_dir=save_dir)
        return image,newres
