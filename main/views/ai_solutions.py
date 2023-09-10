from django.shortcuts import render
# self edited --------------------------
from django.conf import settings
import main.views.yolov5_optimized.detect as detect
from pathlib import Path
# self edited --------------------------

import logging

# for 3rd party AI classification API
import json
import requests
import time

from authentication.utils.check_login_state import check_login
from main.utils.ai_solutions_utils import *

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'main/index.html')


#@check_login
def ai_solutions(request, page):
    product_list, promotion_product_list, first_promotion_product, pagination = get_product(page)

    return render(request, 'main/ai_solutions.html',
                  {'product_list': product_list, 'promotion_product_list': promotion_product_list,
                   'first_promotion_product': first_promotion_product,
                   'promotion_product_num': range(len(promotion_product_list)),
                   'pagination': pagination})

#@check_login
def ai_classification(request):
    return render(request, 'main/ai_classification.html', {"success": True, "initial": True})

#@check_login
def ai_disease_diagnose(request):
    return render(request, 'main/ai_disease_diagnose.html', {"success": True, "initial": True})

def pic_handle_classification(request):
    diseases = []
    have_result = False
    
    if request.method == "POST":
        f1 = request.FILES.get('pic')
        if f1:
            fname = settings.MEDIA_ROOT + '/ai_classification/' + f1.name
            with open(fname,'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            try:
                response_inference = json.loads(
                    requests.post(
                        "https://api.modelplace.ai/v3/process",
                        params={"model_id": 15, },
                        files={"upload_data": open(fname, "rb")}
                    ).content
                )
                
                while True:
                    response_task = json.loads(
                        requests.get(
                            "https://api.modelplace.ai/v3/task",
                            params=response_inference
                        ).content
                    )
                    if len(response_task) == 0:
                        raise Exception("response empty!")
                    
                    if response_task.get("status", -1) == -1:
                        raise Exception("Error: Error when detecting your image! This may result from the inaccessibility of our sevice, try again later!")
                    
                    if response_task["status"] != "finished":
                        time.sleep(5)
                    else:
                        res = response_task["result"]
                        for i in range(len(res)):
                            diseases.append(res[i]["class_name"])
                        have_result = True
                        return render(request,'main/ai_classification.html', {'success':True, 'result_list': diseases, 'have_result': have_result, 'userimg': f1.name})
            except Exception as e:
                return render(request,'main/ai_classification.html', {'success':False, "err_msg": str(e), 'userimg': f1.name})
        else:
            return render(request,'main/ai_classification.html', {'success':False, "err_msg": "Error: file uploaded is empty! Please click choose file to select an image!"})
        
    return render(request,'main/ai_classification.html', {'success':True, 'result_list': diseases, 'have_result': have_result})

def pic_handle_yolov5(request):
    if request.method == "POST":
        f1 = request.FILES.get('pic')
        if f1:
            fname = settings.MEDIA_ROOT + '/aidiseasediagnose/' + f1.name
            with open(fname,'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            try:
                if "shallow" in request.POST:
                    result_path = detect.run(weights="main/views/yolov5_optimized/16x2.pt",imgsz=(416,416),conf_thres=0.5,source=fname)
                else:
                    result_path = detect.run(weights="main/views/yolov5_optimized/16x2.pt",imgsz=(416,416),conf_thres=0.25,source=fname)
            except Exception as e:
                return render(request,'main/ai_disease_diagnose.html', {'success':False, 'err_msg': repr(e)})
        else:
            error = "file uploaded is empty"
            return render(request,'main/ai_disease_diagnose.html', {'success':False, 'err_msg': error})

        # success
        txt_path = settings.MEDIA_ROOT + "/" + result_path + "/labels/result.txt"
        path = Path(txt_path)
        diseases = []
        have_result = False
        if path.is_file():
            have_result = True
            with open (txt_path, 'r') as f:
                for line in f.readlines():
                    disease = line.split(' ')[0]
                    if disease not in diseases:
                        diseases.append(disease)

        return render(request,'main/ai_disease_diagnose.html', {'success': True, 'result_path': result_path + "/result.jpg", 'result_list': diseases, 'have_result': have_result})

    return render(request,'main/ai_disease_diagnose.html', {'success': True})
# self edited --------------------------

#@check_login
def smart_curtain(request, page):
    product_list, promotion_product_list, first_promotion_product, pagination = get_product(page)
    load_animation = False
    if page == 1:
        load_animation = True

    return render(request, 'main/smart_curtain.html',
                  {'product_list': product_list,
                   'pagination': pagination,
                   'load_animation': load_animation})

#@check_login
def virtual_reality_forest_therapy(request, page):
    product_list, VR_product_list, first_promotion_product, pagination = get_VR_FT(page)

    return render(request, 'main/virtual_reality_forest_therapy.html',
                  {'product_list': product_list, 'VR_product_list': VR_product_list,
                   'first_promotion_product': first_promotion_product,
                   'promotion_product_num': range(len(VR_product_list)),
                   'pagination': pagination})

def digital_twin(request):
    return render(request,'main/VRFT_digital_twin.html')

def vr_detail(request):
    return render(request,'main/vr_detail.html')
