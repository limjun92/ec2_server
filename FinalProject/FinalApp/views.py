from django.shortcuts import render
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import io
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import shutil


def main(request):
    return render(request, 'main.html')

def place_list(request):
    
    with open("model_t.json", "r") as f :
        loaded_model_json = f.read()

    model = model_from_json(loaded_model_json, custom_objects={'KerasLayer': hub.KerasLayer})
    model.load_weights("model_t.h5")

    if request.method == "POST":
        landmark = request.FILES['photo']

        default_storage.save('image.jpg', ContentFile(landmark.read()))
        path = 'media/image.jpg'
        img = tf.keras.preprocessing.image.load_img(path, target_size=(224, 224),)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) 
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        # t = np.array(score)
        print(score)

        # 여기다가 변수 정해주고, 상위 3~5개 저장 한다. => global 로 저장해두는게 나을듯

        # media 디렉토리 삭제
        shutil.rmtree('media')

    return render(request, 'place_list.html')

def place_detail(request):
    return render(request, 'place_detail.html')

def place_route(request):
    return render(request, 'place_route.html')