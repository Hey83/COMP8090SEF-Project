from typing import List, Dict, Optional
from items import Item, PerishableItem, NonPerishableItem


class InventoryManager:
    # Manages the inventory of items, including adding, updating, and reporting

    def __init__(self):
        self._items: Dict[str, Item] = {}

    def add_item(self, item: Item) -> bool:
        if item.name in self._items:
            print(f"Item '{item.name}' already exists. Use update instead.")
            return False
        self._items[item.name.lower()] = item
        print(f"Added: {item}")
        return True

    def update_quantity(self, name: str, change: int) -> bool:
        item = self.find_item(name)
        if not item:
            return False

        if change > 0:
            item.increase_stock(change)
            print(f"Increased {name} by {change} → now {item.quantity}")
            return True
        elif change < 0:
            success = item.decrease_stock(-change)
            if success:
                print(f"Deducted {-change} from {name} → now {item.quantity}")
            else:
                print(f"Not enough stock for {name}")
            return success
        return False

    def find_item(self, name: str) -> Optional[Item]:
        return self._items.get(name.lower())

    def get_low_stock_items(self, threshold: int = 10) -> List[Item]:
        return [item for item in self._items.values() if item.needs_restock_alert(threshold)]

    def get_expired_items(self) -> List[PerishableItem]:
        return [
            item for item in self._items.values()
            if isinstance(item, PerishableItem) and item.is_expired()
        ]

    def generate_simple_report(self):
        print("\n" + "="*50)
        print("      Perfect Brew Coffee - Stock Report")
        print("="*50)
        total_value = 0.0

        for item in sorted(self._items.values(), key=lambda x: x.category):
            status = item.get_status()
            print(f"{item}  →  {status}")
            total_value += item.quantity * item.unit_price

        print("-"*50)
        print(f"Total inventory value: HKD {total_value:.2f}")
        print("="*50 + "\n")