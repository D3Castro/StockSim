#include <thread>
#include <chrono>
#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <mutex>
#include <condition_variable>
#include <vector>
#include <time.h>
using namespace std;
//High 75 Mid 50 Low 25
#define NUM_THREADS 10000		
#define X			.25		//% price inc. to sell 
#define Y			.5		//% price dec. to sell
#define Z			.5		//% chance to buy

/*
Stock class to hold information necessary for a Stock. 
It also makes a priceList that randomnly generates numbers simulating the fluctuation of price.
*/
class Stock {
public:
	Stock(string sym);
	Stock(string sym, int nShares, int cPerShare);
	int checkPrice();
	int getPrice();
	int getCost();
	int getShares();
	string getName();

private:
	string symbol;
	int numShares;
	int costPerShare;
	vector<int> priceList;
};

Stock::Stock(string sym) {	//ADD rand low and high later
	symbol = sym;
	numShares = 0;
	costPerShare = 0;
	for (int i = 0; i < 10000; i++) {
		priceList.push_back(rand() % 20 + 10);
	}
}


Stock::Stock(string sym, int nShares, int cPerShare) {	//ADD rand low and high later
	symbol = sym;
	numShares = nShares;
	costPerShare = cPerShare;
	for (int i = 0; i < 10000; i++) {
		priceList.push_back(rand() % 20 + 10);
	}
}

int Stock::checkPrice() {
	return priceList.back();
}

int Stock::getPrice() {
	int x = priceList.back();
	priceList.pop_back();
	return x;
}

int Stock::getCost() {
	return costPerShare;
}

int Stock::getShares() {
	return numShares;
}

string Stock::getName() {
	return symbol;
}

mutex l;
vector<Stock> stocks,bought;
int balance = 10000, yield = 0, profit = 0, Tcost = 0, boughtStock = 0, soldStock = 0;

void serverT() {
	yield = profit - Tcost;
	cout << "Currently have bought: " << boughtStock << " stocks.\n"
		 << "Currently have sold:   " << soldStock << " stocks.\n"
		 << "Costing:               " << Tcost << ".\n"
		 << "Yielding:              " << yield << ".\n"
		 << "With a profit of:      " << profit << ".\n"
		 << "And a balance of:      " << balance << ".\n\n";
}

//In format  BUY SYM NUM_SHARES COST_PER
//In format  SELL SYM NUM_SHARES COST_PER 
/*
This function processes the transactions for BUY and SELL updating global values here.
It does this by parsing an input string Transaction for key words "BUY" or "SELL" then 
extracts the pertinent information and processes the BUY or SELL.
*/
void processTransact(string transaction) {
	//Parses the string into a vector of strings.
	istringstream iss(transaction);
	vector<string> words{ istream_iterator<string>(iss), istream_iterator<string> {} };
	if (words.front() == "BUY") {
		words.erase(words.begin());

		//Gets the stock name.
		string symbol = words.front();
		words.erase(words.begin());

		//Gets number of stock to buy.
		string a = words.front();
		int buyNum = atoi(a.c_str());
		words.erase(words.begin());

		//Gets the price per share.
		a = words.front();
		int sharePrice = atoi(a.c_str());

		Stock newBuy(symbol, buyNum, sharePrice);

		bought.push_back(newBuy);
		boughtStock += buyNum;
		balance -= (buyNum * sharePrice);
		Tcost += (buyNum * sharePrice);	

		return;
	}
	else {
		words.erase(words.begin());

		//Gets the stock name.
		string symbol = words.front();
		words.erase(words.begin());

		//Gets number of stock to buy.
		string a = words.front();
		int buyNum = atoi(a.c_str());
		words.erase(words.begin());

		//Gets the price per share.
		a = words.front();
		int sharePrice = atoi(a.c_str());
		words.erase(words.begin());

		soldStock += buyNum;
		balance += (buyNum * sharePrice);
		profit += (buyNum * sharePrice);

		return;
	}
}

/*
This is a thread that takes no arguments, it selects a random stock from the vector of stocks
and then buys it by creating a transactString and passing it to processTransact to be bought.
After this it sleeps for 2 seconds.
*/
void buy() {
	l.lock();
	srand((unsigned int)time(NULL));
	//Choose a random stock to buy.
	int i = rand() % stocks.size();

	//Creates a string that processTransact can parse.
	string transactString = "BUY " + stocks.at(i).getName() + " 50 " + to_string(stocks.at(i).getPrice());

	processTransact(transactString);
	
	l.unlock();
	this_thread::sleep_for(2s);
}

/*
This is a thread that takes int s, the location of the stock to be sold in vector bought, 
and then sells it by creating a transactString and passing it to be processTransact to be sold.
After this it sleeps for 2 seconds.
*/
void sell(string transactString) {
	processTransact(transactString);

	this_thread::sleep_for(2s);
}

/*
This program simulates buying and selling of stock NUM_THREADS - 1 times using threads.
It also intermittently shows information on the stocks every 10 threads.
It decides whether stock will be bought by a Z% chance or sold by a decrease by Y% or increase by X%.
*/
int main() {
	vector<thread> threads; int server = 0;
	int num_transacts = 0;	bool isBuy = true;
	
	srand((unsigned int)time(NULL));

	//Pushing values into vector stocks.
	Stock MSFT("MSFT");	stocks.push_back(MSFT);
	Stock AMZN("AMZN"); stocks.push_back(AMZN);
	Stock BAC("BAC"); stocks.push_back(BAC);
	Stock NKE("NKE"); stocks.push_back(NKE);
		
	//Buys or Sells for NUM_THREADS - 1 times
	while (num_transacts < NUM_THREADS) {
		//Intermittently display current monetary information.
		if (server == 250) {
			server = 0;
			thread serverThread(serverT);
			serverThread.join();
		}
		else {
			//If isBuy == true
			if (isBuy) {
				if (balance < 5000 && bought.size() > 0) {
					isBuy = false;
				}
				else {
					//Z percent chance to buy a stock.
					if (((double)rand() / (double)RAND_MAX) < Z) {
						threads.push_back(thread(buy));

						++num_transacts;
						++server;
						isBuy = false;
					}
				}
			}
			//If isBuy == false
			else {
				//Acquire lock to prevent any changes to vector bought while selling
				l.lock();
				//Assert there are values in bought
				if (bought.size() > 0) {
					//Percent chance to sell if it has increased or decreased too much in price
					int s = rand() % bought.size();
					if ((bought.at(s).checkPrice()) > (((1 + X)*bought.at(s).getCost())) || (bought.at(s).checkPrice()) < (((1 + Y)*bought.at(s).getCost()))) {
						//Creates a string that processTransact can parse.
						string transactString = "SELL " + bought.at(s).getName() + " 50 " + to_string(bought.at(s).getPrice());
						//Remove the stock from bought.
						bought.erase(bought.begin() + s);
						threads.push_back(thread(sell, transactString));

						++num_transacts;
						++server;
					}
					else {
						//Gets a new price for the next time the program tries to sell this stock.
						bought.at(s).getPrice();
					}
				}
				l.unlock();
				isBuy = true;
			}
		}
	}

	//Join all the threads in the vector.
	for (thread &th : threads) th.join();

	thread serverThread(serverT);
	serverThread.join();

	cout << "\n\nProgram has finished...";
	cin >> server;
	return 0;
}