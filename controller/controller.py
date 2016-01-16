def main():
    print "Hello world!"



def PathGeneration():
	#generowanie sciezki robota
	#symulator generuje sciez
	#generujemy tez jak wyglada w punkcie startowym sate czyli cala plansza ktore resourcy sa zajete a ktore nie (!!!! CZyli wszystkie resourcy sa wolen)

def InitPathSendMessage():
	#wysylamy sciezki kazdego robota na poczatku do symulatora

def QueueController():
	#odbior danych/eventow z symulatora pakowanie ich do tablicy [idRobota,Resource w ktorym jest, resource w ktory chece zajac,resource w torym 		byl =unknown, priorytet=0 z deaultu] 
	
def ReceiveEvent():
	#odbior danych z QueueControllera
	#bierzemy pierwszy event 

	#event zwraca nam pozycje robota
 	#id robota
	#resource w ktorym jest
	#recource o ktory pyta

	#na podstawie tego w ktorym jest i o ktory pyta oraz generowanej sciezki
	#wyznaczamy resource w ktorym byl 
	#pakujemy 
	#wysylamy do controllera

def FreeResource():
	#odbiera dane z receive event
	#zwolnienie resourcu czyli ustawienie resourcu w ktorym byl robot na unknown
	#Update stata //czyli update informacji o planszy ktore resourcy sa wolne ktory nie itd

def PublishData():
	#wysylanie konkretnego pakietu danych do symulatora

def AllocateResource():
	#odbior danych
	#zajecie resourcu
	#Update stata
	#wyslij dane do symulator funckja PublishData()
	
def Controller():
	# z funkcji Receive Event dostajemy info w talblicyo id robota 
	
	#otrzymujemy dane
	
	#zwalniamy resource funckja FreeResource
	#sprawdzamy czy na liscie z wiekszym priorytetem mozna przypisac odpowiedni resource to to robimy

	#if resource o ktory pytamy jest wolny
	#odpalamy funckje AllocateResource
	#else
	#resource jest zajety 
	#tworzymy liste robotow z wyzszy priorytem,
	 
	






























if __name__ == '__main__':
    main()  # This is executed if file is not imported
