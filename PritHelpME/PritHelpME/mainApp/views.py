import cv2
import numpy as np
import base64
import json
import ezdxf
import io
import tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.http import HttpResponse
# def find_and_draw_lines(image, line_color=(0, 0, 255), line_thickness=2.00):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 30, 150, apertureSize=3)
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=40, maxLineGap=100)

#     white_canvas = np.ones_like(image) * 255
#     dxf_doc = ezdxf.new(dxfversion='R2010')
#     dxf_msp = dxf_doc.modelspace()

#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(white_canvas, (x1, y1), (x2, y2), line_color, line_thickness)
#             dxf_msp.add_line((x1, y1), (x2, y2))

#     _, buffer = cv2.imencode('.png', white_canvas)
#     encoded_image = base64.b64encode(buffer).decode('utf-8')

#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         dxf_doc.saveas(temp_file.name)
#         temp_file.seek(0)
#         encoded_dxf = base64.b64encode(temp_file.read()).decode('utf-8')

#     return encoded_image, encoded_dxf

def find_and_draw_lines(image, line_color=(0, 0, 255), line_thickness=9, lineweight=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=40, maxLineGap=100)

    white_canvas = np.ones_like(image) * 255
    dxf_doc = ezdxf.new(dxfversion='R2010')
    dxf_doc.header["$LWDISPLAY"] = 1
    dxf_msp = dxf_doc.modelspace()
    # ezdxf.lldxf.const.VALID_DXF_LINEWEIGHTS
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(white_canvas, (x1, y1), (x2, y2), line_color, line_thickness)
            dxf_msp.add_line((x1, y1), (x2, y2), dxfattribs={"lineweight": 100})

    _, buffer = cv2.imencode('.png', white_canvas)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        dxf_doc.saveas(temp_file.name)
        temp_file.seek(0)
        encoded_dxf = base64.b64encode(temp_file.read()).decode('utf-8')

    return encoded_image, encoded_dxf

@csrf_exempt
def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        line_color = tuple(map(int, request.POST.get('line_color', '0,0,255').split(',')))
        line_thickness = int(request.POST.get('line_thickness', 2))

        try:
            image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            encoded_image, encoded_dxf = find_and_draw_lines(image, line_color, line_thickness)
            return JsonResponse({"image": encoded_image, "dxf": encoded_dxf})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def mainPage(request):
    return render(request, 'new.html')

def upload_form(request):
    return render(request, 'upload.html')