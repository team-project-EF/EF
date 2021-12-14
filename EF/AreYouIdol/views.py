from django.shortcuts import render, redirect
from django.contrib import messages
from AreYouIdol.models import Upload

# Create your views here.
def find(request):
    if request.method == 'POST':
        print(request.POST)
        img = request.FILES["img"]

        upload = Upload()
        upload.img = img
        upload.save()

        # 이미지 url 넘겨주기
        # context = {
        #     'img' : upload.img
        #  }

        messages.success(request, upload.img.url)
        return redirect('/')
    else:
        return render(request, 'areyouidol.html')