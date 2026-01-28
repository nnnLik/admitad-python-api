# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from admitad.items import CampaignRates
from admitad.tests.base import BaseTestCase


class CampaignRatesTestCase(BaseTestCase):

    def test_get_campaign_rates(self):
        campaign_id = 1
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignRates.URL, campaign_id=campaign_id),
                json={
                    'campaign_id': campaign_id,
                    'actions': [{
                        'action_id': 1,
                        'action_name': 'Sale',
                        'action_code': 'sale',
                        'action_type': 'sale',
                        'system_commission': '10.00',
                        'system_commission_from_cart': None,
                        'tariffs': [{
                            'tariff_id': 1,
                            'tariff_name': 'Standard Tariff',
                            'tariff_code': 'TAR001',
                            'default': True,
                            'rates': [{
                                'price_s': '100.00$',
                                'size': '50.00$',
                                'country': 'Russia'
                            }, {
                                'price_s': '200.00$',
                                'size': '100.00$',
                                'country': 'USA'
                            }]
                        }]
                    }]
                },
                status=200
            )
            result = self.client.CampaignRates.get(campaign_id)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['campaign_id'], campaign_id)
        self.assertIn('actions', result)
        self.assertEqual(len(result['actions']), 1)
        self.assertEqual(result['actions'][0]['action_id'], 1)
        self.assertEqual(result['actions'][0]['action_name'], 'Sale')
        self.assertIn('tariffs', result['actions'][0])
        self.assertEqual(len(result['actions'][0]['tariffs']), 1)
        self.assertIn('rates', result['actions'][0]['tariffs'][0])
        self.assertEqual(len(result['actions'][0]['tariffs'][0]['rates']), 2)

    def test_get_campaign_rates_with_multiple_actions(self):
        campaign_id = 2
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignRates.URL, campaign_id=campaign_id),
                json={
                    'campaign_id': campaign_id,
                    'actions': [
                        {
                            'action_id': 1,
                            'action_name': 'Sale',
                            'action_code': 'sale',
                            'action_type': 'sale',
                            'system_commission': '10.00',
                            'system_commission_from_cart': None,
                            'tariffs': []
                        },
                        {
                            'action_id': 2,
                            'action_name': 'Lead',
                            'action_code': 'lead',
                            'action_type': 'lead',
                            'system_commission': None,
                            'system_commission_from_cart': '5.00',
                            'tariffs': [{
                                'tariff_id': 2,
                                'tariff_name': 'Lead Tariff',
                                'tariff_code': 'TAR002',
                                'default': False,
                                'rates': [{
                                    'price_s': '50.00$',
                                    'size': '25.00$',
                                    'country': None
                                }]
                            }]
                        }
                    ]
                },
                status=200
            )
            result = self.client.CampaignRates.get(campaign_id)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['campaign_id'], campaign_id)
        self.assertEqual(len(result['actions']), 2)
        self.assertEqual(result['actions'][0]['action_code'], 'sale')
        self.assertEqual(result['actions'][1]['action_code'], 'lead')

    def test_get_campaign_rates_with_empty_actions(self):
        campaign_id = 3
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignRates.URL, campaign_id=campaign_id),
                json={
                    'campaign_id': campaign_id,
                    'actions': []
                },
                status=200
            )
            result = self.client.CampaignRates.get(campaign_id)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['campaign_id'], campaign_id)
        self.assertEqual(result['actions'], [])

    def test_get_campaign_rates_invalid_id(self):
        campaign_id = 0
        with self.assertRaises(ValueError):
            self.client.CampaignRates.get(campaign_id)
