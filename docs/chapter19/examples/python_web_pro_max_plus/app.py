import os
import time
import base64
import requests as rq
from io import StringIO, BytesIO
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from models.models import *




model_mode = {
    "OCR识别": "recOCR", 
    "人脸检测": "detPersonObj", 
    "口罩检测": "detPersonMask",
    "目标检测": "detAllObj"
}



# 获得图片 bytes => [[list]]
def get_upload_img(upload_file):
    img_width = 600
    img_height = 800
    bytes_stream = BytesIO(upload_file.getvalue())
    capture_img = Image.open(bytes_stream)
    capture_img = np.asarray(capture_img)
    # capture_img = cv2.cvtColor(np.asarray(capture_img), cv2.COLOR_RGB2BGR)
    height,width,_ = capture_img.shape
    if height > img_height:
        height = img_height
    if width > img_width:
        width = img_width
    capture_img = cv2.resize(capture_img, (width, height))
    return capture_img


# @st.cache
def main():

    ### 页面配置
    st.set_page_config(
        page_title="花卷老师的AI体验站",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            'About': "# 花卷老师的AI体验站"
        }
    )

    ### 侧边栏
    st.sidebar.markdown("# Model")
    app_mode = st.sidebar.selectbox(
        "请选择模型",
        [
            "首页",
            "OCR识别", 
            "人脸检测", 
            "口罩检测",
            "目标检测"
        ],
        help = '选择一个功能模型'
    )
    
    st.markdown("\n\n")

    with st.container():
        # st.sidebar.markdown("---\n## 文件")
        st.sidebar.markdown("## 文件")
        file = st.sidebar.file_uploader("本地文件", type=['png', 'jpg'], help='选择一张图片, 格式: jpg或者png')
        # url = st.sidebar.text_input("或者图片URL","请输入网路图片URL",help='请输入网路图片URL')
    
    st.markdown("\n\n")

    with st.container():
        # st.sidebar.markdown("---\n## 参数")
        st.sidebar.markdown("## 参数")
        confidence_threshold = st.sidebar.slider("置信度", 0.0, 1.0, 0.5, 0.1,help='设置模型输出概率')

    ### 主页显示
    if app_mode == '首页':
        ### 主页标题
        title_text = st.markdown("# 花卷老师的AI体验站\n---")

        with st.container():
            abstract_text = st.markdown("> 牛皮，帅炸，强无敌。")
        
        st.markdown("<br />"*2,unsafe_allow_html=True)

        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("高效性", "直接部署", "100%")
            col2.metric("实用性", "落地可用", "100%")
            col3.metric("精准性", "领先业内", "100%")


        st.markdown("<br />"*2,unsafe_allow_html=True)

        video_file = open('./resource/people_num.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

        st.markdown("<br />",unsafe_allow_html=True)
        
        title_text = st.markdown("### <span style='border-bottom:2px solid rgb(255, 94, 0);'>OCR技术</span>",unsafe_allow_html=True)
        st.markdown("<br />",unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### 通用OCR")
            
        with col2:
            st.markdown("##### 票据识别")

        with col3:
            st.markdown("##### 证件识别")
        
        st.markdown("<br />",unsafe_allow_html=True)

        st.image('./resource/ocr_res.jpg')

        st.markdown("<br />"*2,unsafe_allow_html=True)

        title_text = st.markdown("### <span style='border-bottom:2px solid rgb(255, 94, 0);'>视觉技术</span>",unsafe_allow_html=True)
        st.markdown("<br />",unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("##### 人脸识别")

        with col2:
            st.markdown("##### 口罩识别")

        with col3:
            st.markdown("##### 目标检测")

        st.markdown("<br />",unsafe_allow_html=True)

        st.image('./resource/face_res.png')


    else:
        title_text = st.markdown(f"# {app_mode}\n---")
        if file is not None:
            with st.expander("点击预览图片",expanded=False):
                st.write(f"图片路径: {file.name}")
                image = get_upload_img(file)
                # print(image)
                st.image(image,caption='原始图片')

            with st.expander("点击查看参数",expanded=True):
                st.json({
                    'file': file.name,
                    'model': app_mode,
                    'confidence_threshold': confidence_threshold
                })

            if st.button(label='开始检测', help='点击按钮运行模型'):
                st.write('===>开始检测')
                st.write(f"===>图片路径: {file.name}")
                # 处理
                with st.spinner('检测中'):
                    image,res = aimodels(model_mode[app_mode],image_code=cv2_to_base64(image),rate=confidence_threshold)

                st.write('===>检测完毕')
                st.markdown("\n\n")

                title_text = st.markdown("### 计算结果\n---")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### 结果图片")
                    st.image(image)
                    # st.download_button(
                    #     label="Download data as PNG",
                    #     data=cv2.imencode('.png', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))[1].tostring(),
                    #     file_name="res.png",
                    #     mime="image/png"
                    # )

                with col2:
                    st.markdown("##### 结果列表")
                    res = [[x['category'],x['score']]for x in res]
                    res = pd.DataFrame(res,columns=['结果','置信度'])
                    # st.dataframe(res)
                    st.table(res)
                    # st.download_button(
                    #     label="Download data as CSV",
                    #     data=res.to_csv().encode('utf-8'),
                    #     file_name='res.csv',
                    #     mime='text/csv',
                    # )



if __name__ == "__main__":
    main()