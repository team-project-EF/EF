from django.shortcuts import render, redirect
from django.contrib import messages
from AreYouIdol.models import Upload
from .apps import AreyouidolConfig as cf
from .PreProcessing.align_faces import crop
import numpy as np
from PIL import Image
import os
import shutil

# Create your views here.
def find(request):
    # 세션 관리
    if request.session.session_key == None:
        request.session['visited']=1

    print(request.session.session_key)

    if request.method == 'POST':
        
        img = request.FILES.get("img")
        ex = os.path.splitext(str(img))[-1].lower()

        if ex in ['.jpg', '.jpeg', '.png']:
            if os.path.exists(cf.img_path):
                shutil.rmtree(cf.img_path)
            if os.path.exists(cf.crop_path):
                shutil.rmtree(cf.crop_path)

            upload = Upload()
            upload.img = img
            upload.save()

            # 크롭 전 이름 변경
            img_path = os.path.join(cf.img_path, str(img))
            file_path  = os.path.join(cf.img_path, 'up_img'+ex)
            os.rename(img_path, file_path)

            crop()

            # 모델 예측
            model = cf.model
            file_name = os.path.basename(file_path)
            crop_path = os.path.join(cf.crop_path, file_name)
            crop_img = Image.open(crop_path)
            crop_img = crop_img.convert('RGB')
            data = np.asarray(crop_img)
            X = np.array(data)
            X = X.astype("float") / 255
            X = X.reshape(-1, 128, 128, 3)
            categories = ["idol", "ilban"]
            pred = model.predict(X)
            print(np.array(pred)[0])
            print(np.argmax(pred))
            pred_result = [file_path, categories[np.argmax(pred)]]

            messages.add_message(request, messages.SUCCESS, pred_result)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR,
                                 '이미지(jpg, jpeg, png) 파일을 업로드 해주세요.')
            return redirect('/')
    else:
        return render(request, 'areyouidol.html')
