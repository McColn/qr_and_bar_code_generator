import qrcode
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import QRCode
from django.conf import settings
import os


from .models import Product
from .forms import ProductForm


def home(request):
    return render(request, 'app/home.html')

def generate_qr(request):
    if request.method == "POST":
        url = request.POST.get('url')
        color = request.POST.get('color', 'black')  # Default color is black
        bg_color = request.POST.get('bg_color', 'white')  # Default background is white
        box_size = int(request.POST.get('box_size', 10))  # Default box size
        logo = request.FILES.get('logo')  # Uploaded logo

        if not url:
            return HttpResponse("Please provide a URL.")

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for logos
            box_size=box_size,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color=color, back_color=bg_color).convert("RGB")

        # Add logo if provided
        if logo:
            logo_image = Image.open(logo)
            logo_size = (img.size[0] // 4, img.size[1] // 4)  # Scale logo to 25% of QR size
            logo_image = logo_image.resize(logo_size)
            pos = ((img.size[0] - logo_size[0]) // 2, (img.size[1] - logo_size[1]) // 2)
            img.paste(logo_image, pos, logo_image)

        # Save QR code to database
        qr_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_path, exist_ok=True)
        file_name = f"qr_{QRCode.objects.count() + 1}.png"
        file_path = os.path.join(qr_path, file_name)
        img.save(file_path)

        # Save to model
        qr_instance = QRCode.objects.create(url=url, image=f'qr_codes/{file_name}')
        qr_instance.save()

        return HttpResponse(f"QR Code generated and saved! <br><img src='{qr_instance.image.url}' alt='QR Code'>")

    return HttpResponse("Invalid request method.")


def barCode(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new product to the database
            return redirect('barCodeList')  # Redirect to a list of products or another page
    else:
        form = ProductForm()
    
    return render(request, 'app/barCode.html', {'form': form})

def barCodeList(request):
    product = Product.objects.order_by('-id').first()  # Assuming 'id' is the primary key and auto-incremented
    return render(request, 'app/barCodeList.html', {'product': product})