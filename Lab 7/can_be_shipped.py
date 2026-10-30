# can_be_shipped.py
# CanBeShipped: an interface-style abstract base class (a "must be able to" contract).
# Any class that signs this contract must provide calculate_shipping_cost().
# No product attributes or shipping rules live here.

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost (a number). Implementing classes decide how."""
        pass
