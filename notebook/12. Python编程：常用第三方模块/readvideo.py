import cv2 as cv

if __name__ == '__main__':
    video = cv.VideoCapture()
    video.open('./examples/1.mp4')
    #判断是否成功创建视频流
    while video.isOpened():
        ret,frame = video.read()
        print(ret)
        if ret is True:
            cv.imshow('video: ./examples/1.mp4',frame)
            #设置播放速速
            cv.waitKey(int(1000 / video.get(cv.CAP_PROP_FPS)))
            #按下q键退出
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
                    #输出相关参数信息
    print('视频中的图像宽度{}'.format(video.get(cv.CAP_PROP_FRAME_WIDTH))) 
    print('视频中的图像高度{}'.format(video.get(cv.CAP_PROP_FRAME_HEIGHT))) 
    print('视频帧率{}'.format(video.get(cv.CAP_PROP_FPS))) 
    print('视频帧数{}'.format(video.get(cv.CAP_PROP_FRAME_COUNT))) 
    #释放资源并关闭窗口
    video.release()
    cv.destroyAllWindows()