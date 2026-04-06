#include<iostream>
#include<cstdio>
using namespace std;
int main(){
	char key[] = "abcdef@12345";
	char user_input[100];
	scanf("%s",user_input);
	printf(user_input);  // VULN: intentional format-string vulnerability for demonstration
	printf("\n");
	return 0;
}
