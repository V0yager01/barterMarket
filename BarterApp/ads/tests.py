from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal, Category


class AdsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.user2 = User.objects.create_user(username='otheruser',
                                              password='otherpass')
        self.category = Category.objects.create(name='Test Category')

        self.ad1 = Ad.objects.create(
            user=self.user,
            title='Ad Title 1',
            description='Ad Description 1',
            category=self.category,
            condition='new'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Ad Title 2',
            description='Ad Description 2',
            category=self.category,
            condition='used'
        )

    def test_main_page_access(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad Title 1')

    def test_create_ad_requires_login(self):
        response = self.client.get(reverse('main:createform'))
        self.assertEqual(response.status_code, 302)

    def test_create_ad_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('main:createform'), {
            'title': 'New Ad',
            'description': 'Some desc',
            'category': self.category.id,
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='New Ad').exists())

    def test_create_trade(self):
        self.client.login(username='testuser', password='testpass')
        Ad.objects.create(
            user=self.user,
            title='Sender Ad',
            description='Sender desc',
            category=self.category,
            condition='used'
        )
        response = self.client.post(reverse('main:create_trade',
                                            args=[self.ad2.id]), {
            'ad_sender': self.ad1.id,
            'comment': 'Trade'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.exists())

    def test_filter_trade_by_receiver(self):
        trade = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Test'
        )
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(reverse('main:trade') + '?direction=received')
        self.assertContains(response, trade.comment)

    def test_register_user(self):
        response = self.client.post(reverse('user:register'), {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_delete_ad(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('main:delete_ad', args=[self.ad1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ad.objects.filter(id=self.ad1.id).exists())

    def test_update_ad(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('main:update_ad', args=[self.ad1.id]), {
            'title': 'Updated',
            'description': 'Updated desc',
            'category': self.category.id,
            'condition': 'used'
        })
        self.assertRedirects(response, reverse('main:detail', args=[self.ad1.id]))
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Updated')

    def test_update_trade_status_accept(self):
        trade = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Testing'
        )
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.post(reverse('main:update_trade', args=[trade.id]), {
            'action': 'accept'
        })
        trade.refresh_from_db()
        self.assertEqual(trade.status, 'accepted')

    def test_pagination_main_page(self):
        for i in range(20):
            Ad.objects.create(
                user=self.user,
                title='Test',
                description='test',
                category=self.category,
                condition='new'
            )
        response_1 = self.client.get(reverse('main:index'))
        response_2 = self.client.get(reverse('main:index') + '?page=2')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
        ads_1 = response_1.context['ads']
        ads_2 = response_2.context['ads']
        self.assertEqual(len(ads_1), 10)
        self.assertEqual(len(ads_2), 10)
