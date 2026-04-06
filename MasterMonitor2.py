import pexpect
from datetime import datetime
import sys
import argparse
from pathlib import Path


KNOWN_BACKDOORS = ["MASTER_28", "Master_28", "ADMIN", "ROOT", "BACKDOOR"]
KNOWN_PROMOCODES = {"SAVE10":10, "BOOKFEST":20}

def log_alerts(alert_msg: str, log_path: Path):
	print(alert_msg)
	with open(log_path, "a") as f:
		f.write(alert_msg + "\n")



def alert(attack_type: str, detail: str, log_path: Path):
	time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	msg = (
		f"\n{'='*60}\n"
		f"\t[ALERT] {attack_type}\n"
		f"\tTime	:	{time}\n"
		f"\tDetails	:	{detail}\n"
		f"{'='*60}"
	)
	log_alerts(msg, log_path)

def check_trapdoor(password: str, log_path: Path):
	if not password:
		return
	if password in KNOWN_BACKDOORS:
		alert("TRAPDOOR / BACKDOOR LOGIN ATTEMPT",
			f"'{password}' matches a hardcoded backdoor credential.",
			log_path
		)
		return
	sus_words = ["MASTER","28","ADMIN","ROOT","BACKDOOR","SECRET"]
	for i in sus_words:
		if i in password.upper():
			alert("SUSPICIOUS LOGIN ATTEMPT",
				f"Password: '{password}' contains suspicious keyword '{i}'.",
				log_path
			)
			return

def check_format_string(name: str, log_path:Path):
	dangerous_specifiers = {
		"%p":"Pointer /address leak",
		"%x":"hex memory dump",
		"%s":"string memory read(can crash)",
		"%n":"Write to arbitrary memory(critical crash)",
		"%hn":"half-word write (critical)",
		"%d":"integer read from stack",
		"%u":"unsigned int read from stack"
	}
	found = []
	for spec, defi in dangerous_specifiers.items():
		if name.count(spec)>0:
			found.append(f"'{spec}'({defi})")
	if found:
		alert("FORMAT STRING ATTACK DETECTED",
			f"Name field contains specifiers {', '.join(found)}.",
			log_path
		)

def check_overflow(declared_len:int, name:str, log_path:Path):
	if declared_len < len(name):
		alert("OVERFLOW ATTEMPT DETECTED",
			f"Declared length is '{declared_len}' but name has '{len(name)}' chars.",
			log_path
		)

def check_cache_poisoning(code: str, discount:int, log_path:Path):
	if code in ("none",""):
		return
	if code not in KNOWN_PROMOCODES:
		alert("CACHE POISONING - UNKNOWN PROMO CODE",
			f"Code '{code}' is not in the legitimate promo registry",
			log_path
		)
	else:
		legitimate = KNOWN_PROMOCODES[code]
		if discount != legitimate:
			alert("CACHE POISONING : VALUE TAMPERING",
				f"Code: '{code}' is legitimate but the claimed discount: '{discount}' is wrong",
				log_path
			)

def check_integer_overflow(qty: int, log_path:Path):
	if qty>17179870:
		alert("Integer OVERFLOW/ WRAP INTEGER",
			f"Quantity '{qty}' exceeds safe multiplication threshold",
			log_path
		)

def run_monitor(victim_path: Path, log_path:Path):
	print("\n" + "="*60)
	print("\tSECURITY MONITOR - REAL-TIME ATTACK DETECTION\t\n")
	print("\n" + "="*60)

	if not victim_path.exists():
		print(f"[ERROR] Victim binary not found: {victim_path}")
		print("		Compile with: g++ -o victim MasterVictim.cpp")
		sys.exit(1)

	try:
		child = pexpect.spawn(str(victim_path), encoding='utf-8', timeout=30)
		child.logfile_read = sys.stdout

		child.expect("Enter password")
		login_input = input()
		child.sendline(login_input)
		check_trapdoor(login_input, log_path)

		child.expect("Enter the length of your name: ")
		ui_len = int(input())
		child.sendline(str(ui_len))

		child.expect("Enter your name: ")
		ui_name = input("Enter name: ")
		child.sendline(ui_name)

		check_overflow(ui_len, ui_name, log_path)
		check_format_string(ui_name, log_path)

		child.expect(r"Do you have a promo code\?")
		promo_choice = input()
		child.sendline(promo_choice)
		if promo_choice == 'y':
			child.expect("Enter promo code: ")
			promo_code = input()
			child.sendline(promo_code)

			child.expect("Enter discount % you claim this code gives: ")
			claimed_discount = int(input())
			child.sendline(str(claimed_discount))

			check_cache_poisoning(promo_code,claimed_discount,log_path)




		while True:
			child.expect(r"Do you want to buy a book\?")
			ui_ch = input()
			child.sendline(ui_ch)

			if ui_ch == "n":
				print("\n---------Exiting shop---------\n")
				break


			child.expect("Which book would you like to buy?")
			ui_book_choice = int(input())
			child.sendline(str(ui_book_choice))

			child.expect("How many books would you like to buy?")
			ui_quantity = int(input())
			child.sendline(str(ui_quantity))

			check_integer_overflow(ui_quantity, log_path)

			child.expect(r"Enter promo code for this purchase")
			purchase_code = input()
			child.sendline(purchase_code)

			if purchase_code != "none":
				if purchase_code not in KNOWN_PROMOCODES:
					alert("CACHE POISONING - POISONED CODE USED AT CHECKOUT",
						f"Code: '{purchase_code}'used at checkout but not in legitimate registry of promo codes",
						log_path
					)

		child.expect(pexpect.EOF)
		#python might lose the terminal before total_cost is printed thus end of file(cpp reacher return 0) is required.

	except pexpect.exceptions.EOF:
		print("\n[!] The C++ program terminated unexpectedly.")
		#Crash detector:- catches EOF if it happens in the middle of conversation.

	except pexpect.exceptions.TIMEOUT:
		print("\n[!] The python script got stuck waiting for C++ program")
		#Typo/timeout:- the python script got stuck waiting for the C++ program.

	except Exception as e:
		print(f"\n[!] An error occurred:  {e}")
		#Crash detector:- standard exception handling.
	finally:
		print(f"\n[*]Session ended. Alerts logged to {log_path}\n")



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Security monitor - Detects attacks against MasterVictim in real-time.")
	parser.add_argument(
		"--victim",
		type=Path,
		default=Path(__file__).parent/"victim",
		help = "Path to the compiled victim binary (default: ./victim next to this script)"
	)
	parser.add_argument(
		"--log",
		type=Path,
		default=Path(__file__).parent /"security_alerts.log",
		help="Path to the alert log file (default: ./security_alerts.log next to this script)"
	)
	args = parser.parse_args()
	args.log.parent.mkdir(parents=True, exist_ok=True)
	run_monitor(args.victim,args.log)










