from django.db import models
from main.models import Users


class Categories(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def get_default_category():
    return Categories.objects.get(name='Прочее').id


class Ad(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    image_url = models.ImageField(upload_to='images')
    category = models.ForeignKey(Categories, on_delete=models.SET(get_default_category), null=True)
    condition = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    class Meta:
        verbose_name = 'Статус объявления'
        verbose_name_plural = 'Статусы объявлений'

    class Status(models.TextChoices):
        WAIT = 'wait', 'ожидает'
        ACCEPTED = 'accepted', 'принята'
        REJECTED = 'rejected', 'отклонена'

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sender')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='receiver')
    comment = models.TextField(max_length=1000)
    status = models.CharField(choices=Status.choices, default=Status.WAIT)
    created_at = models.DateTimeField(auto_now_add=True)

