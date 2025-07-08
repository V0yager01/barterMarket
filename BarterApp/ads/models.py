from django.db import models
from django.contrib.auth import get_user_model

from .const import CONDITION_CHOICES, STATUS_CHOICES


User = get_user_model()


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='ads')
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)
    condition = models.CharField(max_length=20,
                                 choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    id = models.AutoField(primary_key=True)
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE,
                                  related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE,
                                    related_name='received_proposals')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Предложение обмена от {self.ad_sender} к {self.ad_receiver} — {self.status}'


class Category(models.Model):
    name = models.CharField(max_length=256,
                            blank=False,
                            null=False)

    def __str__(self):
        return self.name
