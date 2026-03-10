from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
import os


class CarouselImage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='carousel_images/')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carousel Image'
        verbose_name_plural = 'Carousel Images'
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.display_order:
            # Auto-assign display order
            last_order = CarouselImage.objects.filter(is_active=True).order_by('-display_order').last()
            if last_order:
                self.display_order = (last_order.display_order or 0) + 10
            else:
                self.display_order = 1
        
        super().save(*args, **kwargs)
    
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return '/static/placeholder/carousel.jpg'
