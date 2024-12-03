from django.db import models

# bar code import
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# end of import

class QRCode(models.Model):
    url = models.URLField()
    image = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


# bar code model for products
class Product(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.ImageField(upload_to='barcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate the barcode before saving
        if not self.barcode:
            buffer = BytesIO()
            # Customize barcode dimensions using ImageWriter options
            writer = ImageWriter()
            writer.dpi = 300  # Optional: Adjust DPI for better resolution
            writer.set_options({
                "module_height": 3.0,  # Height of the barcode modules
                "module_width": 0.5,   # Width of the barcode modules
                "font_size": 10,       # Font size for the text below the barcode
                "text_distance": 2.0,  # Distance between the barcode and text
            })
            # Generate barcode using product name
            code = Code128(self.name, writer=writer)
            code.write(buffer)
            # Save the image to the barcode field
            self.barcode.save(f'{self.name}_barcode.png', File(buffer), save=False)
            buffer.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name