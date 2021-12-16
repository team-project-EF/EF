from django.shortcuts import render, redirect
from django.contrib import messages
from .apps import AreyouidolConfig as cf
from .PreProcessing.align_faces import crop
import numpy as np
from PIL import Image
import os
from django.core.files.storage import default_storage

# Create your views here.
def find(request):
    # 세션 관리
    if request.session.session_key == None:
        request.session['visited']=1

    print(request.session.session_key)
    sess = request.session.session_key

    if request.method == 'POST':
        
        img = request.FILES.get("img")
        ex = os.path.splitext(str(img))[-1].lower()

        if ex in ['.jpg', '.jpeg', '.png']:
            # 파일이름 : 세션키 + 확장자명
            file_name = sess + ex

            # 같은 파일의 이름(같은 세션에서 업로드한 파일)이 존재하면 삭제
            if os.path.exists(os.path.join(cf.img_path, file_name)):
                os.remove(os.path.join(cf.img_path, file_name))
            if os.path.exists(os.path.join(cf.crop_path, file_name)):
                os.remove(os.path.join(cf.crop_path, file_name))

            # 이미지 저장 경로
            img_path = default_storage.save('images/' + file_name, img)

            file_path = os.path.join('media',img_path)


            # 이후 작업시 주석 해제
            crop(file_name)

            # 모델 예측
            model = cf.model
            crop_image = os.path.join(cf.crop_path, file_name)
            crop_img = Image.open(crop_image)
            crop_img = crop_img.convert('RGB')
            data = np.asarray(crop_img)
            X = np.array(data)
            X = X.astype("float") / 255
            X = X.reshape(-1, 128, 128, 3)
            categories = ["idol", "ilban"]
            pred = model.predict(X)
            print(np.array(pred)[0])
            print(categories[np.argmax(pred)])

            messages.add_message(request, messages.SUCCESS, file_path)
            
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR,
                                 '이미지(jpg, jpeg, png) 파일을 업로드 해주세요.')
            return redirect('/')
    else:
        return render(request, 'areyouidol.html')
