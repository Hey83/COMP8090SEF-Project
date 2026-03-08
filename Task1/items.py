from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Item(ABC):
    # Base class for all inventory items, demonstrating encapsulation and abstraction
    def __init__(self, name: str, category: str, unit_price: float, quantity: int = 0):
        self._name = name.strip()              # encapsulation
        self._category = category.strip()
        self._unit_price = max(0.0, unit_price)
        self._quantity = max(0, quantity)

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def unit_price(self):
        return self._unit_price

    @property
    def quantity(self):
        return self._quantity

    def increase_stock(self, amount: int):
        if amount > 0:
            self._quantity += amount

    def decrease_stock(self, amount: int) -> bool:
        if 0 < amount <= self._quantity:
            self._quantity -= amount
            return True
        return False

    @abstractmethod
    def needs_restock_alert(self, threshold: int = 10) -> bool:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

    def __str__(self):
        return f"{self._name} ({self._category}): {self._quantity} units @ HKD {self._unit_price:.2f}"


class NonPerishableItem(Item):
    # Coffee beans, syrups, cups — items without expiry

    def needs_restock_alert(self, threshold: int = 10) -> bool:
        return self.quantity <= threshold

    def get_status(self) -> str:
        if self.needs_restock_alert():
            return "LOW STOCK"
        return "OK"


class PerishableItem(Item):
    # Milk, cream — items that expire and need special handling

    def __init__(self, name: str, category: str, unit_price: float,
                 quantity: int = 0, expiry_days: int = 7):
        super().__init__(name, category, unit_price, quantity)
        self._expiry_date = datetime.now() + timedelta(days=expiry_days)

    @property
    def expiry_date(self):
        return self._expiry_date

    def is_expired(self) -> bool:
        return datetime.now() > self._expiry_date

    def needs_restock_alert(self, threshold: int = 10) -> bool:
        return self.quantity <= threshold or self.is_expired()

    def get_status(self) -> str:
        if self.is_expired():
            return "EXPIRED"
        if self.quantity <= 5:
            return "LOW & URGENT"
        if self.quantity <= 10:
            return "LOW"
        return "OK"

    def __str__(self):
        base = super().__str__()
        return f"{base} | Expires: {self._expiry_date.strftime('%Y-%m-%d')}"