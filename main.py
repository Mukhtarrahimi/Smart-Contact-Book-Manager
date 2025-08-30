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

def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("This field cannot be empty.")

def find_contact_index_by_id(contacts, cid):
    for i, c in enumerate(contacts):
        if c["id"] == cid:
            return i
    return -1


def pretty_print_contacts(contacts):
    if not contacts:
        print("\n(No contacts found)\n")
        return
    print("\nContact List:")
    print("-" * 60)
