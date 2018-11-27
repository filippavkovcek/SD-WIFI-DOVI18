POUZITIE IPERF-U V MININETE

	Predpoklad: Existujuca topologia s 2 prepojenymi zariadeniami A a B

	Spustenie iperf serveru:
		A # iperf -s -p PORT_NUMBER -i 1
			-s rola serveru
			-p pocuvaj na porte PORT_NUMBER
			-i 1 sleduj vysledky kazdu sekundu

	Spustenie iperf clienta:
		B # iperf -c 10.0.0.X -p PORT_NUMBER -t SECONDS
			-c rola clienta
			-10.0.0.X cielova IP adresa zariadenia
			-p PORT_NUMBER posielaj na port s cislom PORT_NUMBER
			-t SECOND po dobu SECONDS sekund

	! Prepinac -u u oboch stanic prepne premavku na typ UDP

	Vykreslenia grafov:
		Uskutocnuje sa cez vystupny subor, ktory je poskytnuty pri zadavani prikazu na vytvorenie iperf cliet-a/server-u
		A # iperf -s -p PORT_NUMBER -i 1 > OUTPUT_FILE

		Postprocessing nad grafom:
			Je potrebne vyparsovat data z vystupu
			cat OUTPUT_FILE | grep "/sec" | tr - " " | awk '{print $4,$8}' > PROCESSED_FILE
