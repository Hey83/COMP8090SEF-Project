from items import PerishableItem, NonPerishableItem
from manager import InventoryManager

# Show a simple text-based menu for the inventory system
def show_menu():
    print("\n" + "-"*40)
    print("  Perfect Brew Coffee - Stock System  ")
    print("-"*40)
    print("1. Add new item")
    print("2. Record stock arrival / deduction")
    print("3. Check item status")
    print("4. Show low stock & expired items")
    print("5. Show full inventory report")
    print("0. Exit")
    print("-"*40)


# Main function to run the inventory management system
def main():
    manager = InventoryManager()

    # Some example items (for testing / demonstration)
    manager.add_item(NonPerishableItem("Ethiopia Yirgacheffe", "Beans", 180.0, 15))
    manager.add_item(PerishableItem("Whole Milk", "Dairy", 28.0, 40, expiry_days=5))
    manager.add_item(NonPerishableItem("Paper Cups 8oz", "Cups", 0.8, 500))
    manager.add_item(PerishableItem("Fresh Cream", "Dairy", 45.0, 8, expiry_days=4))

    while True:
        show_menu()
        choice = input("Enter choice (0-5): ").strip()

        if choice == "0":
            print("Goodbye! Keep brewing perfectly ☕")
            break

        elif choice == "1":
            # Add new item flow
            name = input("Item name: ").strip()
            cat = input("Category: ").strip()
            price = float(input("Unit price (HKD): ") or 0)
            qty = int(input("Initial quantity: ") or 0)
            perishable = input("Perishable? (y/n): ").lower().startswith("y")

            if perishable:
                days = int(input("Expiry days from today: ") or 7)
                item = PerishableItem(name, cat, price, qty, days)
            else:
                item = NonPerishableItem(name, cat, price, qty)

            manager.add_item(item)

        elif choice == "2":
            # Update stock flow
            name = input("Item name: ").strip()
            change = int(input("Change quantity (+ add / - deduct): "))
            manager.update_quantity(name, change)

        elif choice == "3":
            # Check item status flow
            name = input("Item name: ").strip()
            item = manager.find_item(name)
            if item:
                print(item)
                print(f"Status: {item.get_status()}")
            else:
                print("Item not found.")

        elif choice == "4":
            # Show low stock and expired items
            low = manager.get_low_stock_items()
            expired = manager.get_expired_items()

            print("\nLOW STOCK ITEMS:")
            for it in low:
                print(f"  • {it} → {it.get_status()}")

            print("\nEXPIRED ITEMS:")
            for it in expired:
                print(f"  • {it}")

        elif choice == "5":
            # Show full inventory report
            manager.generate_simple_report()

        else:
            print("Invalid choice. Try again.")


# Run the main function when this script is executed
if __name__ == "__main__":
    main()