from __future__ import annotations

from admitad.items.base import Item


__all__ = [
    'CampaignRates',
]


class CampaignRates(Item):
    """
    Get campaign rates, tariffs and actions information

    """

    SCOPE = 'campaign_rates'

    URL = Item.prepare_url('campaign_rates/%(campaign_id)s/rates')

    def get(self, campaign_id: int, **kwargs: dict) -> dict:
        """
        Get campaign rates, tariffs and actions information

        Args:
            campaign_id (int): Campaign ID

        Returns:
            dict: Campaign rates information with actions, tariffs and rates

        """
        request_data = {
            'url': self.URL,
            'campaign_id': Item.sanitize_id(campaign_id)
        }

        return self.transport.get().request(**request_data)
