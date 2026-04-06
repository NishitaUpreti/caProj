#include<iostream>
#include<cstdio>
#include<string>
#include<cstring>
#include<map>
using namespace std;

bool trapdoor_login(const string& password){
	const char* backdoor = "MASTER_28";
	if(password==backdoor){
		cout<< "\n[Backdoor] Admin shell unlocked. Full access granted.\n";
		cout << "[Backdoor] Secret_bank_Token_88 | Balance_Override: Unlimited\n";
		return true;
	}
	return false;
}

map<string, int>discount_cache;
void init_cache(){
	discount_cache["SAVE10"] = 10;
	discount_cache["BOOKFEST"] = 20;
}

int lookup_discount(const string& code){
	if(discount_cache.find(code) != discount_cache.end()){
		return discount_cache[code];
	}
	return 0;
}

void apply_promo(const string& code, int discount_pct){
	discount_cache[code] = discount_pct;
	cout << "[CACHE] promo code "<< code<< " cached with " << discount_pct << "%% discount.\n";
}

int main(){

	cout << "===SECURE BOOKSHOP LOGIN===" << endl;
	cout << "Enter password (or press enter to continue as a guest): ";
	cout.flush();
	string login_input;
	getline(cin, login_input);

	bool is_admin = false;
	if(!login_input.empty()){
		is_admin = trapdoor_login(login_input);
		if(!is_admin){
			cout << "[AUTH] Invalid password. Continuing as guest.\n";
		}
	}







	char key[] = "SECRET_BANK_TOKEN_888";
	int len, balance=500, quantity;
	cout << "Enter the length of your name: ";
	cout.flush();
	cin >> len;
	char name[len];
	string books[5] = {"The Alchemist by Paulo Coelho",
			 "1984 by George Orwell",
			 "The Hobbit by J.R.R. Tolkien",
			 "Harry Potter by J.K. Rowling",
			 "Atomic Habits by James Clear"};

	int price[5] = {300,250,400,500,350};
	scanf("%s",name);  // VULN: no bounds check on input length
	printf("\n----Welcome to the shop ");
	printf(name);  // VULN: intentional format-string vulnerability
	printf("----\n");
	fflush(stdout);

	init_cache();
	cout << "===PROMO CODE SECTION===" << endl;
	cout << "Do you have a promo code? [y/n]: ";
	cout.flush();
	char promo_ch;
	cin >> promo_ch;

	if(promo_ch=='y'){
		cout << "Enter promo code: ";
		cout.flush();
		string promo_code;
		cin >> promo_code;
		cout << "Enter discount % you claim this code gives: ";
		cout.flush();
		int claimed_discount;
		cin >> claimed_discount;

		apply_promo(promo_code, claimed_discount);
		int disc = lookup_discount(promo_code);
		cout << "[Promo] Discount applied: " << disc << "%\n";
	}
	do{
		char ch;
		cout << "Do you want to buy a book? [y/n] : ";
		cout.flush();
		cin >> ch;
		if(ch=='n')	break;
		printf("Balance : Rs.%d\n",balance);
		fflush(stdout);
		cout << "Which book would you like to buy?" << endl;
		for(int i=0; i<5; i++){
			cout << i <<". "<< books[i] << "-> Rs." << price[i] << endl;
		}
		unsigned int book_choice;
		scanf("%u",&book_choice);  // VULN: no bounds check on book_choice
		cout << "How many books would you like to buy?" << endl;
		cout.flush();
		cin >> quantity;
		cout << "Enter promo code for this purchase (or 'none'): ";
		cout.flush();
		string purchase_code;
		cin >> purchase_code;
		int disc_pct = lookup_discount(purchase_code);
		unsigned int total =(unsigned int)(quantity*price[book_choice]);

		if(disc_pct>0){
			total =total* (100-disc_pct)/100;
			printf("[PROMO] discount of %d%% applied.\n",disc_pct);
		}

		printf("Total Cost: %u\n", total);
		fflush(stdout);
		if(total<=balance){
			balance -= total;
			cout << "Purchase successful!" << endl;
		}else{
			cout << "Insufficient Balance!" << endl;
		}
	}while(true);
	cout << "\n---THANK YOU FOR VISITING---\n";
	return 0;
}
