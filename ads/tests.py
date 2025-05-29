# ads/tests.py
from io import BytesIO
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from .models import Ad, Categories, ExchangeProposal


def get_test_image(name="img.png", size=(50, 50), color=(255, 0, 0)):
    """Создаём in-memory PNG-картинку, чтобы не писать файл на диск."""
    data = BytesIO()
    Image.new("RGB", size, color).save(data, "PNG")
    data.seek(0)
    return SimpleUploadedFile(name, data.read(), content_type="image/png")


class BaseAdsTestCase(TestCase):
    """Общие фикстуры: два пользователя, категория и по объявлению для каждого."""
    def setUp(self):
        self.client = Client()

        self.User = get_user_model()
        self.u1 = self.User.objects.create_user(username="alice", password="pass")
        self.u2 = self.User.objects.create_user(username="bob", password="pass")

        self.cat = Categories.objects.create(title="Разное")

        # объявления-заготовки
        self.ad1 = Ad.objects.create(
            user=self.u1,
            title="Old Title",
            description="desc",
            image_url=get_test_image(),
            category=self.cat,
            condition="ok",
        )
        self.ad2 = Ad.objects.create(
            user=self.u2,
            title="Bob item",
            description="something",
            image_url=get_test_image("img2.png"),
            category=self.cat,
            condition="ok",
        )


class AdCRUDTestCase(BaseAdsTestCase):
    def test_create_ad(self):
        self.client.force_login(self.u1)
        url = reverse("ads:ad_create")
        data = {
            "title": "New Ad",
            "description": "great",
            "image_url": get_test_image("new.png"),
            "category": self.cat.id,
            "condition": "fresh",
        }
        resp = self.client.post(url, data, follow=True)
        self.assertJSONEqual(resp.content, {"status": "ok", "ad_id": Ad.objects.last().id})
        self.assertEqual(Ad.objects.filter(title="New Ad").count(), 1)

    def test_edit_ad(self):
        self.client.force_login(self.u1)
        url = reverse("ads:ad_edit", args=[self.ad1.pk])
        resp = self.client.post(url, {
            "title": "New Title",
            "description": self.ad1.description,
            "image_url": self.ad1.image_url,  # обязательное поле
            "category": self.cat.id,
            "condition": self.ad1.condition,
        }, follow=True)
        self.assertJSONEqual(resp.content, {"status": "ok", "ad_id": self.ad1.pk})
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, "New Title")

    def test_delete_ad(self):
        self.client.force_login(self.u1)
        url = reverse("ads:ad_edit", args=[self.ad1.pk])
        resp = self.client.delete(url)
        self.assertJSONEqual(resp.content, {"status": "deleted"})
        self.assertFalse(Ad.objects.filter(pk=self.ad1.pk).exists())


class AdsListViewTestCase(BaseAdsTestCase):
    def test_search_and_category_filter(self):
        self.client.force_login(self.u1)
        url = reverse("ads:ads_list") + f"?search=Bob&category={self.cat.id}"
        resp = self.client.get(url)
        ads = resp.context["ads"]
        self.assertEqual(list(ads), [self.ad2])  # найдено только объявление Bob


class ExchangeProposalTestCase(BaseAdsTestCase):
    def setUp(self):
        super().setUp()
        # u1 предлагает обмен u2
        self.client.force_login(self.u1)
        create_url = reverse("ads:proposal_create") + f"?receiver={self.ad2.id}"
        data = {"ad_sender": self.ad1.id,
                "ad_receiver": self.ad2.id,
                "comment": "swap?"}
        resp = self.client.post(create_url, data, follow=True)
        self.proposal_id = resp.json()["proposal_id"]
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_accept_proposal(self):
        self.client.force_login(self.u2)           # получатель принимает
        url = reverse("ads:proposal_accept", args=[self.proposal_id])
        resp = self.client.post(url, follow=True)
        self.assertJSONEqual(resp.content, {"status": ExchangeProposal.Status.ACCEPTED})
        proposal = ExchangeProposal.objects.get(pk=self.proposal_id)
        self.assertEqual(proposal.status, ExchangeProposal.Status.ACCEPTED)

    def test_cancel_proposal_by_sender(self):
        """Отправитель удаляет (отзывает) своё предложение через DELETE."""
        self.client.force_login(self.u1)
        url = reverse("ads:proposal_edit", args=[self.proposal_id])  # ← другой маршрут
        resp = self.client.delete(url)

        self.assertJSONEqual(resp.content, {"status": "deleted"})
        self.assertFalse(
            ExchangeProposal.objects.filter(pk=self.proposal_id).exists()
        )