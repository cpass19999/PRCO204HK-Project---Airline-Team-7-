-- Airlines
insert into airline values(null,"Emirates","EA");
insert into airline values(null,"Korea Air","KA");
insert into airline values(null,"Vietnam Airlines","VA");
insert into airline values(null,"Delta Airlines","DA");
insert into airline values(null,"Lufthansa","LH");  
insert into airline values(null,"All Nippon Airways","AN");
insert into airline values(null,"American Airlines","AA");
insert into airline values(null,"Air France","AF");  

-- Airports
insert into airport values(null,"Heathrow", "London");
insert into airport values(null,"O'Hare", "Chicago");
insert into airport values(null,"JFK", "NYC");
insert into airport values(null,"Changi", "Singapore");
insert into airport values(null,"Tan Son Nhat", "HCMC");
insert into airport values(null,"Incheon", "Seoul");  
insert into airport values(null,"DFW", "Dallas");
insert into airport values(null,"Narita", "Tokyo");  

-- airplacness
insert into airplacnes values(null,"Emirates", 777, 250);
insert into airplacnes values(null,"Korea Air", 777, 250);
insert into airplacnes values(null,"Korea Air", 797, 250);
insert into airplacnes values(null,"Lufthansa", 777, 250);
insert into airplacnes values(null,"Air France", 787, 350);
insert into airplacnes values(null,"All Nippon Airways", 797, 450);
insert into airplacnes values(null,"Vietnam Airlines", 777, 500);
insert into airplacnes values(null,"American Airlines", 350 ,500);
insert into airplacnes values(null,"Delta Airlines", 777, 250);  

insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_Date,depart_Time,available,price) 
			  	 values("Emirates", 777, "JFK",  "O'Hare", "2020-06-19", "22:30:00", "Upcoming",999);
                 
insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_Date,depart_Time,available,price)
			  	 values("Delta Airlines", 777, "O'Hare", "JFK", "2020-04-03","20:45:00", "Upcoming",452);
                 
insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_Date,depart_Time,available,price)
			  	 values("Delta Airlines", 777, "O'Hare", "JFK", "2020-04-02","19:45:00", "Upcoming",2032);
insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_Date,depart_Time,available,price)values
					   ("Delta Airlines", 777, "JFK", "DFW", "2020-04-19","22:30:00","Upcoming",1523),
					   ("Delta Airlines", 777, "O'Hare",  "JFK", "2020-04-02","19:45:00","Upcoming", 799),
					   ("Korea Air", 797, "Incheon",  "JFK", "2020-04-30","19:45:00", "Upcoming", 2990),
					   ("Korea Air", 777, "Incheon",  "JFK", "2020-04-30","3:00:00", "Notavailable", 1990),
					   ("Korea Air", 777, "Incheon",  "JFK", "2020-04-30","7:00:00","Upcoming", 4990), 
					   ("Vietnam Airlines", 777, "Tan Son Nhat",  "JFK", "2020-04-30","19:45:00",  "Upcoming", 1099),
					   ("All Nippon Airways", 777, "Narita",  "O'Hare", "2020-05-19","19:45:00",  "Upcoming", 2990),
					   ("Delta Airlines", 777, "JFK",   "DFW","2020-04-19","22:30:00", "Upcoming", 800),
					   ("Lufthansa", 777, "JFK",  "DFW",  "2020-04-19","22:30:00", "Upcoming", 800), 
					   ("American Airlines", 797, "JFK",   "DFW", "2020-04-19","22:30:00","Upcoming", 800);

