from django.shortcuts import render, redirect
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import io
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import shutil
import pandas as pd
import numpy as np
import datetime
import requests

class_name = pd.read_csv('location_amend_1.csv', encoding='utf-8')

def main(request):
    return render(request, 'main.html')

def place_list(request):
    
    df = pd.read_csv('csv_final_final.csv')
    img_url_df = df[['img_url', 'display']]

    img_url_dict = dict(img_url_df.values[:,::-1])
    
    with open("amend_model_1.json", "r") as f :
        loaded_model_json = f.read()

    model = model_from_json(loaded_model_json, custom_objects={'KerasLayer': hub.KerasLayer})
    model.load_weights("amend_model_1.h5")

    if request.method == "POST":
        landmark = request.FILES['photo']

        default_storage.save('image.jpg', ContentFile(landmark.read()))
        path = 'media/image.jpg'
        img = tf.keras.preprocessing.image.load_img(path, target_size=(224, 224),)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) 
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        total_score = np.array(score)
        total_sort_score = sorted(total_score)

        context = {
            'first': {
                'name': class_name.iloc[np.where(total_score == total_sort_score[-2])[0][0], 1],
                'address': class_name.iloc[np.where(total_score == total_sort_score[-2])[0][0], 2],
                'long': class_name.iloc[np.where(total_score == total_sort_score[-2])[0][0], 3],
                'lat': class_name.iloc[np.where(total_score == total_sort_score[-2])[0][0], 4],
                'img_url' : 'img/' + img_url_dict[class_name.iloc[np.where(total_score == total_sort_score[-2])[0][0], 1]],
            },
            'second': {
                'name': class_name.iloc[np.where(total_score == total_sort_score[-3])[0][0], 1],
                'address': class_name.iloc[np.where(total_score == total_sort_score[-3])[0][0], 2],
                'long': class_name.iloc[np.where(total_score == total_sort_score[-3])[0][0], 3],
                'lat': class_name.iloc[np.where(total_score == total_sort_score[-3])[0][0], 4],
                'img_url' : 'img/' + img_url_dict[class_name.iloc[np.where(total_score == total_sort_score[-3])[0][0], 1]],
            },
            'third': {
                'name': class_name.iloc[np.where(total_score == total_sort_score[-4])[0][0], 1],
                'address': class_name.iloc[np.where(total_score == total_sort_score[-4])[0][0], 2],
                'long': class_name.iloc[np.where(total_score == total_sort_score[-4])[0][0], 3],
                'lat': class_name.iloc[np.where(total_score == total_sort_score[-4])[0][0], 4],
                'img_url' : 'img/' + img_url_dict[class_name.iloc[np.where(total_score == total_sort_score[-4])[0][0], 1]],
            },
        }

        # media 디렉토리 삭제
        shutil.rmtree('media')
        

        return render(request, 'place_list.html', context)
    else:
        return render(request, 'index.html')



def place_detail(request):
    key = 'qOJ1%2BlTLwzbtiNUtJB4ZVGM1CFG8udmOZfTw8KTYct2EPlKXXW7U0u6R1oueez7kRw2TY4eWb0b%2FlBmwwJCdLQ%3D%3D'
    today = datetime.datetime.today().strftime('%Y%m%d')

    if request.method == "POST":
        context = {
            'map':{
                'name': request.POST['name'],
                'address': request.POST['address'],
                'long': request.POST['long'],
                'lat': request.POST['lat'],
                'img_url': request.POST['img_url'],
                },
            'festival':{
            }
        }

        festival = {}
        if context['map']['address'].split(' ')[0] == "서울특별시":
            areaCode = 1
        elif context['map']['address'].split(' ')[0] == "인천광역시":
            areaCode = 2
        elif context['map']['address'].split(' ')[0] == "대구광역시":
            areaCode = 4
        elif context['map']['address'].split(' ')[0] == "광주광역시":
            areaCode = 5
        elif context['map']['address'].split(' ')[0] == "부산광역시":
            areaCode = 6
        elif context['map']['address'].split(' ')[0] == "경기도":
            areaCode = 31
        elif context['map']['address'].split(' ')[0] == "충청남도":
            areaCode = 34
        elif context['map']['address'].split(' ')[0] == "경상북도":
            areaCode = 35
    
        url = f'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?serviceKey={key}&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=AppTest&arrange=A&listYN=Y&areaCode={areaCode}&eventStartDate={today}&_type=json'
        event = requests.get(url)
        event = event.json()
        if event['response']['body']['totalCount'] >= 2:
            for x in event['response']['body']['items']['item']:
                festival[x['title']] = x
        context['festival'] = festival
        
        return render(request, 'place_detail.html', context)

    else:
        return render(request, 'index.html')

def place_route(request):
    return render(request, 'place_route.html')