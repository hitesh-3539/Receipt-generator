# 🧾 Python CLI Receipt Generator

A robust, object-oriented Command Line Interface (CLI) application built in Python that dynamically generates professional, styled PDF payment receipts. 

This project demonstrates core backend development concepts including Object-Oriented Programming (OOP), third-party library integration, user input validation, and local data persistence.

## ✨ Features
* **Interactive CLI:** Step-by-step terminal prompts with error handling to prevent crashes from invalid user inputs.
* **Dynamic Calculations:** Automatically calculates item subtotals, applies percentage-based discounts, and computes the grand total.
* **PDF Generation:** Uses `reportlab` to build a beautifully styled, color-coded PDF receipt with a dynamic data table.
* **Unique Identification:** Generates a unique, mathematically random receipt ID for every transaction.
* **Data Persistence:** Silently logs all transaction details to a local JSON file to maintain a queryable database of generated receipts.

## 📸 Example Output

**Terminal Interface:**
<img width="1470" height="956" alt="Screenshot 2026-05-26 at 4 15 07 PM" src="https://github.com/user-attachments/assets/05690a53-972c-4580-904e-83e499e46b81" />


**Generated PDF Receipt:**
<img width="568" height="763" alt="Screenshot 2026-05-26 at 4 15 57 PM" src="https://github.com/user-attachments/assets/61dfaa05-3e15-4526-9a7b-1fc1880c7318" />


## 🛠️ Prerequisites
* Python 3.x
* `reportlab` library
