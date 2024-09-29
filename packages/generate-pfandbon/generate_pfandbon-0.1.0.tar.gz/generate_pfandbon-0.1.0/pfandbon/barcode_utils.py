import random

def format_amount(amount):
    euros = int(amount)
    cents = int((amount - euros) * 100)
    return f"{euros:04}{cents:02}"

def generate_barcode(total_amount):
    if total_amount > 9999.99:
        raise ValueError("Der maximale Betrag von 9999,99 EUR wurde überschritten.")

    prefix = "22647700007"
    leergutbonnr = random.randint(1000000, 9999999)  # Ensure it is always 7 digits
    formatted_amount = format_amount(total_amount)
    barcode_text = f"{prefix}{leergutbonnr}{formatted_amount}"

    print(f"Generierter 24-stelliger Barcode: {barcode_text}")
    return barcode_text
