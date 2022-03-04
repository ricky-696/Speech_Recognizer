from tensorflow import keras
from tensorflow.keras.models import model_from_json
import librosa
import numpy as np
import pandas as pd

json_file = open('model.json', 'r')
# 讀入模型
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("saved_models/Voice_Model.h5")
# 讀入先前訓練模型的權重
print("Loaded model from disk")
 

# 輸入音訊預測
def classify(pretrain, file):
	X, sample_rate = librosa.load(file, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
	sample_rate = np.array(sample_rate)
	mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
	print(mfccs.shape)
	featurelive = mfccs
	livedf = featurelive 
	livedf= pd.DataFrame(data=livedf)
	livedf = livedf.stack().to_frame().T
	twodim= np.expand_dims(livedf, axis=2)
	livepreds = pretrain.predict(twodim, batch_size=32, verbose=1)
	return livepreds
ans = classify(loaded_model, '04-131.wav')
#錯位(1-3,2-4)(大千 牽影 岳霖 浩恩)
pname = ['Eterna','Jenny','Ricky','Vicent']
name1 = pname[np.argmax(ans)]
print(name1)
with open("outout.txt","w") as f:
        f.write(name1)  #這句話自帶檔案關閉功能，不需要再寫f.close()
