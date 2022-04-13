from aip import imageclassify
import logging
import os

APP_Id = 'YOUR_APP_ID'
API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
appdataPath = os.getenv('APPDATA')
try:
    os.makedirs(f'{appdataPath}\\animal\\log\\')
except:
    pass

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f'{appdataPath}\\animal\\log\\log.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


options = {'baike_num': 1}


def get_animal_info(result):

    animal_info = {}
    animal_info['name'] = result['result'][0]['name']
    if result['result'][0]['baike_info'] == {}:
        animal_info['none'] = True
    else:
        try:
            animal_info['none'] = False
            animal_info['baike_url'] = result['result'][0]['baike_info'][
                'baike_url']
            animal_info['image_url'] = result['result'][0]['baike_info'][
                'image_url']
            animal_info['animal_description'] = result['result'][0][
                'baike_info']['description']
        except:
            logger.info('获取详情失败')
    return animal_info


def get(file):
    image = get_file_content(file)
    client = imageclassify.AipImageClassify(APP_Id, API_KEY, SECRET_KEY)
    result = client.animalDetect(image, options=options)
    animal = get_animal_info(result)
    return animal
