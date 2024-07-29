from typing import Optional, Dict
from decimal import Decimal
import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from enum import Enum

class BillingCycle(Enum):
    MPU = "monthly per user"
    APU = "anual per user"
    OT = "one time"
    CS = "contact sales"



@dataclass
class PricingInfo:
    plan: string
    price: Decimal
    company: string
    date_scraped: datetime
    billing_cycle: BillingCycle



class PricingScraper:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.soup: Optional[BeautifulSoup] = None
    @property
    def company_name(self)-> None:

        raise NotImplementedError("Subclasses must implement this method")


    def fetch_page(self) -> None:
        """Fetch the page content and parse it with BeautifulSoup."""
        try:
            response: requests.Response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            self.soup = None

    def parse_pricing(self) -> PricingInfo:
        """Method to parse pricing data.
        This should be implemented in subclasses."""

        raise NotImplementedError("Subclasses must implement this method")

    def get_pricing_data(self) -> PricingInfo | None:
        """Fetch and parse pricing data."""
        self.fetch_page()
        if self.soup:
            return self.parse_pricing()
        else:
            return None
