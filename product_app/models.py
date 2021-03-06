import os, random, datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image


def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    date = datetime.datetime.now()
    return f'{instance.prod_code}/{date}-{instance.prod_code}{file_extension}'


PRODUCT_CATEGORY = [
    (0, _('Sofa')),
    (1, _('Sponge Sofa')),
    (2, _('Table')),
    (3, _('Chair')),
    (4, _('Curtain')),
    (5, _('Back Rest')),
    (6, _('Arm Rest')),
    (7, _('Pillow')),
]


class Product(models.Model):
    """
    Manage Product Information
    """
    prod_code = models.CharField(max_length=255, unique=True)
    category = models.IntegerField(choices=PRODUCT_CATEGORY, default=0)
    unit_price = models.PositiveIntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.png', upload_to = photo_path)

    def __str__(self):
        return self.prod_code

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 400:
            output_size = (300, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk':self.pk})
    
    class Meta:
        ordering = ['category']
