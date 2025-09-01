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

    c = contacts[idx - 1]
    name = input(f"Name [{c['name']}]: ").strip() or c["name"]
    phone = input(f"Number [{c['phone']}]: ").strip() or c["phone"]
    email = input(f"Email [{c['email']}]: ").strip() or c["email"]
    group = input(f"Group [{c.get('group','')}]: ").strip() or c.get("group", "")
    notes = input(f"Note [{c.get('notes','')}]: ").strip() or c.get("notes", "")

    c.update(
        {"name": name, "phone": phone, "email": email, "group": group, "notes": notes}
    )
    save_contacts(contacts)
    print("Edit done.")

def delete_contact():
    contacts = load_contacts()
    if not contacts:
        print("\n(list empty)\n")
        return
    pretty_print_contacts(contacts)
    try:
        idx = int(input("row number for delete").strip())
        if idx < 1 or idx > len(contacts):
            print("invalid number")
            return
    except ValueError:
        print("invalid input")
        return
    c = contacts[idx - 1]
    confirm = (
        input(f"about deleting«{c['name']}» Are you sure؟ (y/n): ").strip().lower()
    )
    if confirm == "y":
        del contacts[idx - 1]
        save_contacts(contacts)
        print("contact deleted")
    else:
        print("canceled")


def export_pdf(filename=None):
    contacts = load_contacts()
    if filename is None or not filename.strip():
        filename = f"contacts_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=24,
        leftMargin=24,
        topMargin=24,
        bottomMargin=24,
    )
    styles = getSampleStyleSheet()
    elems = []

    title = Paragraph("Contacts Directory", styles["Title"])
    datep = Paragraph(
        f"PDF Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"],
    )
    elems.extend([title, Spacer(1, 12), datep, Spacer(1, 18)])

    if not contacts:
        elems.append(Paragraph("No contacts available.", styles["Normal"]))
        doc.build(elems)
        print(f"📄 Empty PDF created: {filename}")
        return
