from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost (a number). Implementing classes decide how."""
        pass
