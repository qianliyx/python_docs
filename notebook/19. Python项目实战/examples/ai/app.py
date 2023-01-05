import re
import json
import jieba
from pathlib import Path
import tensorflow as tf
import uvicorn
from fastapi import FastAPI,Request



def read_json(file):
    '''读取json文件转化为python对象'''
    with open(file,'r',encoding='utf-8') as f:
        json_dict = json.load(f)
    return json_dict


def load_stopwords(file):
    with open(file,'r',encoding='utf-8') as f:
        sp = [x.strip() for x in f if x.strip()]
    return sp


def segment(x,stopwords = []):
    x = [
        y.replace(" ",'') for y in jieba.cut(x) 
        if y not in stopwords 
        and re.search('[a-zA-Z\u4e00-\u9fa5]+',y) 
        and len(y.replace(" ","")) >= 2 
    ]
    
    return " ".join(x) if len(x) > 0 else None


def data_to_seq(data,tokenizer,maxlen):
    # 序列模式，max_len同意序列长度，超过则过滤，不足则补0
    data_ids = tokenizer.texts_to_sequences(data)
    data_seq = tf.keras.preprocessing.sequence.pad_sequences(
        data_ids,
        maxlen = maxlen,
        padding = 'post'
    )
    return data_seq


def textcnn(maxlen,vocab_size,embedding_dim,cnn_filter_size,cnn_filter_num,dropout_rate,class_num):
    inputx = tf.keras.layers.Input(shape=(maxlen,))
    embx = tf.keras.layers.Embedding(
        vocab_size,
        embedding_dim
    )(inputx)

    ### 卷积池化层
    convs = []
    for size in cnn_filter_size:
        conv = tf.keras.layers.Conv1D(
            cnn_filter_num,
            size,
            padding='same',
            strides=1,
            activation='relu'
        )(embx)
        conv = tf.keras.layers.MaxPooling1D(
            padding = 'same',
            pool_size=size
        )(conv)
        
        convs.append(conv)
        
    ## 拼接卷积池化层输出
    convs = tf.keras.layers.Concatenate(axis=1)(convs)    
    
    convs = tf.keras.layers.Flatten()(convs)
    convs = tf.keras.layers.Dropout(dropout_rate)(convs)
    output = tf.keras.layers.Dense(
        class_num,
        activation='softmax'
    )(convs)
    model = tf.keras.models.Model(inputs = inputx, outputs = output)
    return model




class modelAPI(object):
    def __init__(self):
        path = Path().cwd()
        self.rep = re.compile('[^0-9a-zA-Z\u4e00-\u9fa5 ]')
        self.sp = load_stopwords(path.joinpath('./data/哈工大停用词表.txt'))
        ### 建立token 词语id特征转化
        tokenizer_config = path.joinpath('./output/tokenizer_config.json')
        tokenconfig = read_json(tokenizer_config)
        self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenconfig)
        self.vocab = self.tokenizer.word_index
        self.label2id = read_json(path.joinpath('./output/label2id.json'))
        self.id2label = {y:x for x,y in self.label2id.items()}
        self.maxlen = 70
        self.vocab_size = len(self.vocab) + 1
        self.embedding_dim = 100
        self.cnn_filter_size = [3,4,5]
        self.cnn_filter_num = 100
        self.dropout_rate = 0.3
        self.class_num = len(self.label2id)
        self.cnn_model = textcnn(self.maxlen,self.vocab_size,self.embedding_dim,self.cnn_filter_size,self.cnn_filter_num,self.dropout_rate,self.class_num)
        self.cnn_model.load_weights(path.joinpath('./output/cnn_model_weights.h5'))

    
    def web(self):
        app = FastAPI()

        @app.post('/nlp/classify')
        async def clf(request: Request):

            args = await request.json()
            text = args.get('sen')
            text = re.sub(self.rep,' ',text)
            text = segment(text,stopwords=self.sp)
            inputx = data_to_seq([text.split()],self.tokenizer,self.maxlen)
            label = self.cnn_model.predict(inputx).argmax().item()
            label = self.id2label[label]

            return {'result': f'{label}'}
        
        return app




app = modelAPI().web()




if __name__ == '__main__':
    uvicorn.run(
        app = app,
        host = "0.0.0.0",
        port = 5678
    )