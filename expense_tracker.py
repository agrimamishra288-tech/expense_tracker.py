#!/usr/bin/env python3
"""
Personal Expense Tracker
Name: Agrima Mishra
Roll no:2501010207
Date: 2025-11-18
Simple CLI program to record and view expenses using a CSV file.
"""

import csv
import os
import datetime

CSV_FILE = "expenses.csv"
FIELDNAMES = ["id", "date", "category", "amount", "note"]

def ensure_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def next_id():
    # compute next id from file
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            if not reader:
                return 1
            return int(reader[-1]["id"]) + 1
    except FileNotFoundError:
        return 1

def add_expense():
    ensure_file()
    eid = next_id()
    today = datetime.date.today().isoformat()
    date_str = input(f"Date (YYYY-MM-DD) [{today}]: ").strip()
    if date_str == "":
        date_str = today
    # basic validation
    try:
        datetime.date.fromisoformat(date_str)
    except Exception:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    category = input("Category (e.g. Food, Travel, Bills): ").strip()
    if category == "":
        category = "Other"

    amount_str = input("Amount (number): ").strip()
    try:
        amount = float(amount_str)
    except:
        print("Invalid amount.")
        return

    note = input("Note (optional): ").strip()

    row = {"id": eid, "date": date_str, "category": category, "amount": f"{amount:.2f}", "note": note}
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
    print("Saved expense.")

def view_expenses():
    ensure_file()
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            print("No expenses found.")
            return
        print("{:<4} {:10} {:12} {:8} {}".format("ID", "Date", "Category", "Amount", "Note"))
        print("-"*60)
        for r in rows:
            print("{:<4} {:10} {:12} {:8} {}".format(r["id"], r["date"], r["category"], r["amount"], r["note"]))

def total_spent():
    ensure_file()
    total = 0.0
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                total += float(r["amount"])
            except:
                pass
    print(f"Total spent: {total:.2f}")

def view_by_category():
    ensure_file()
    cat = input("Enter category to filter: ").strip()
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r["category"].lower() == cat.lower()]
        if not rows:
            print("No expenses in that category.")
            return
        print("{:<4} {:10} {:12} {:8} {}".format("ID", "Date", "Category", "Amount", "Note"))
        print("-"*60)
        for r in rows:
            print("{:<4} {:10} {:12} {:8} {}".format(r["id"], r["date"], r["category"], r["amount"], r["note"]))

def menu():
    while True:
        print("\nPersonal Expense Tracker — Menu")
        print("1) Add expense")
        print("2) View all expenses")
        print("3) View total spent")
        print("4) View by category")
        print("5) Exit")
        choice = input("Choose (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_spent()
        elif choice == "4":
            view_by_category()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    ensure_file()
    menu()
