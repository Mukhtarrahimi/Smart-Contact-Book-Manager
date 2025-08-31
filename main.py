import json
import os
import uuid
from datetime import datetime

# for pdf
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# json file name
DATA_FILE = "contacts.json"

# json data section

# load_contacts from json file
def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

# save_contact function
def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

# input function
def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("This field cannot be empty.")

# find contact by id
def find_contact_index_by_id(contacts, cid):
    for i, c in enumerate(contacts):
        if c["id"] == cid:
            return i
    return -1


# print contacts
def pretty_print_contacts(contacts):
    if not contacts:
        print("\n(No contacts found)\n")
        return
    print("\nContact List:")
    print("-" * 60)

    for i, c in enumerate(contacts, start=1):
        print(f"{i}. {c['name']} | {c['phone']} | {c['email']} | {c.get('group','-')}")
    print("-" * 60)


# add contacts
def add_contact():
    contacts = load_contacts()
    print("\nAdd new contact")
    name = input_nonempty("Name: ")
    phone = input_nonempty("Phone: ")
    email = input("Email (optional): ").strip()
    group = input("Group (optional): ").strip()
    notes = input("Notes (optional): ").strip()

    contact = {
        "id": str(uuid.uuid4()),
        "name": name,
        "phone": phone,
        "email": email,
        "group": group,
        "notes": notes,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    contacts.append(contact)
    save_contacts(contacts)
    print(" Contact added successfully.")


# list contacts
def list_contacts():
    contacts = load_contacts()
    pretty_print_contacts(contacts)

def search_contacts():
    contacts = load_contacts()
    if not contacts:
        print("\n(list is empty)\n")
        return
    q = input_nonempty("Search term: ").lower()
    results = [
        c
        for c in contacts
        if q in c["name"].lower()
        or q in c["phone"].lower()
        or q in c["email"].lower()
        or q in (c.get("group", "").lower())
    ]

    if not results:
        print("result not found")
        return
    print("\nsearch result: ")
    print("-" * 60)
    for i, c in enumerate(results, start=1):
        print(f"{i}. {c['name']} | {c['phone']} | {c['email']} | {c.get('group','-')}")
    print("-" * 60)

def edit_contact():
    contacts = load_contacts()
    if not contacts:
        print("\n(list empty: )\n")
        return
    pretty_print_contacts(contacts)
    try:
        idx = int(input("Row number to edit").strip())
        if idx < 1 or idx > len(contacts):
            print("Invalid number")
            return
    except ValueError:
        print("Invalid input")
        return