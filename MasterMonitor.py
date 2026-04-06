import subprocess
from datetime import datetime
from pathlib import Path

VICTIM_PATH = str(Path(__file__).parent / "victim")
LOG_PATH = str(Path(__file__).parent / "security_alerts.log")

KNOWN_BACKDOORS = ["MASTER_28", "Master_28", "ADMIN", "ROOT", "BACKDOOR"]
KNOWN_PROMOCODES = {"SAVE10":10, "BOOKFEST":20}

def log_alert(alert_msg):
	print(alert_msg)
	with open(LOG_PATH, 'a') as f:
		f.write(alert_msg + "\n")

# ---- Gather all inputs upfront (batch/mail mode) ----

login_input = input("Enter password (or press enter for guest): ")

ui_len = int(input("Enter the length of your name: "))
ui_name = input("Enter name: ")

promo_ch = input("Do you have a promo code? [y/n]: ")
promo_code = ""
claimed_discount = 0
if promo_ch == 'y':
	promo_code = input("Enter promo code: ")
	claimed_discount = int(input("Enter discount % you claim this code gives: "))

ui_ch = input("Would you like to buy a book? [y/n]: ")
ui_book_choice = 0
ui_quantity = 0
purchase_code = "none"
if ui_ch == 'y':
	ui_book_choice = int(input("Which book would you like to buy? "))
	ui_quantity = int(input("How many books would you like to buy? "))
	purchase_code = input("Enter promo code for this purchase (or 'none'): ")

# ---- Detection checks ----

if login_input in KNOWN_BACKDOORS:
	log_alert(f"\n[!!!] ALERT : TRAPDOOR/BACKDOOR LOGIN ATTEMPT | Time : {datetime.now()}")
else:
	sus_words = ["MASTER","28","ADMIN","ROOT","BACKDOOR","SECRET"]
	for word in sus_words:
		if word in login_input.upper():
			log_alert(f"\n[!!!] ALERT : SUSPICIOUS LOGIN - contains '{word}' | Time : {datetime.now()}")
			break

if len(ui_name) > ui_len:
	log_alert(f"\n[!!!] ALERT : POTENTIAL OVERFLOW ATTEMPT! | Time : {datetime.now()}")

format_specs = ["%p", "%x", "%s", "%n", "%hn", "%d", "%u"]
found_specs = [s for s in format_specs if s in ui_name]
if found_specs:
	log_alert(f"\n[!!!] ALERT : POTENTIAL FORMAT STRING ATTACK! Specifiers: {found_specs} | Time : {datetime.now()}")

if promo_code and promo_code != "none":
	if promo_code not in KNOWN_PROMOCODES:
		log_alert(f"\n[!!!] ALERT : CACHE POISONING - UNKNOWN PROMO CODE '{promo_code}' | Time : {datetime.now()}")
	elif claimed_discount != KNOWN_PROMOCODES[promo_code]:
		log_alert(f"\n[!!!] ALERT : CACHE POISONING - VALUE TAMPERING on '{promo_code}' | Time : {datetime.now()}")

if ui_book_choice < 0 or ui_book_choice > 4:
	log_alert(f"\n[!!!] ALERT : POTENTIAL OUT-OF-BOUND ATTACK! | Time : {datetime.now()}")

if ui_quantity > 17179870:
	log_alert(f"\n[!!!] ALERT : POTENTIAL TRIGGER OF INTEGER WRAP! | Time : {datetime.now()}")

if purchase_code != "none" and purchase_code not in KNOWN_PROMOCODES:
	log_alert(f"\n[!!!] ALERT : CACHE POISONING - POISONED CODE AT CHECKOUT '{purchase_code}' | Time : {datetime.now()}")

# ---- Build payload and send to victim binary ----

payload = login_input + "\n"
payload += str(ui_len) + "\n"
payload += str(ui_name) + "\n"
payload += str(promo_ch) + "\n"
if promo_ch == 'y':
	payload += str(promo_code) + "\n"
	payload += str(claimed_discount) + "\n"
payload += str(ui_ch) + "\n"
if ui_ch == 'y':
	payload += str(ui_book_choice) + "\n"
	payload += str(ui_quantity) + "\n"
	payload += str(purchase_code) + "\n"
payload += "n\n"  # exit the shop loop

process = subprocess.Popen(VICTIM_PATH, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
output, error = process.communicate(input=payload.encode())

if process.returncode != 0:
	log_alert(f"\n[!!!] ALERT : MEMORY VIOLATION | Time : {datetime.now()} | Status : {process.returncode}")

print("\n-------OUTPUT--------\n")
print(output.decode())
