from django.apps import AppConfig
# from keras.models import load_model
from tensorflow.keras.models import load_model

class AreyouidolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AreYouIdol'
    model = load_model('model/Xception_Idol2.h5')
    img_path = 'media/images'
    crop_path = 'media/cropimages'