# Perfect Brew Coffee - Stock Management System

**COMP8090SEF Course Project – Task 1** 
**Developed by: [To Pui Shan 14083402]**  

This repository contains the **OOP-based Stock Management System for Perfect Brew Coffee**, a fictional independent specialty coffee shop in Hong Kong. The system solves real-world inventory challenges common in busy urban cafes.

## Project Overview

Hong Kong's fast-paced cafe culture often leads to:
- Sudden stockouts of high-demand items (fresh milk, specialty beans, syrups) during peak hours
- Significant waste from expired perishables due to fluctuating customer traffic
- Manual tracking mistakes causing inaccurate levels, over-ordering, or profit loss
- Delayed low-stock detection and inefficient supplier reordering

This Python console application automates stock tracking, deducts ingredients based on drink recipes (e.g., cappuccino uses milk + espresso), issues alerts for low stock or nearing expiry, and provides quick reports—helping cafe owners maintain perfect brews, reduce waste, and run operations smoothly.

Built using **Object-Oriented Programming (OOP)** concepts, including:
- Classes and Objects
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction

## Features

- Add, update, remove items (categorized: beans, dairy, cups, syrups, etc.)
- Separate handling for perishable (with expiry) and non-perishable items
- Status checks and alerts (low stock, expiry warnings)
- Basic reports (total stock value, low/expired items list)
- Print()-based console menu

## Technologies & Requirements

- Python 3.8+
- Standard libraries: `datetime`, `abc`
- No external packages

## Repository Structure
perfect-brew-coffee-stock/
├── items.py          # OOP classes: Abstract Item, PerishableItem, NonPerishableItem
├── manager.py        # InventoryManager + operations (add, sell, report, alerts)
├── main.py           # Console menu and user interaction
└── README.md         # This file

## How to Run

1. Clone the repository:

2. Ensure Python 3 is installed.

3. Run the application:
python main.py
