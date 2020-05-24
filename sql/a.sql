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

insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_at_from,arrival_at_to,available,collected,rate) 
			  	 values("Emirates", 777, "JFK",  "O'Hare", "2017-06-19 22:30:00", "2017-06-20 06:00:00", "Upcoming", 777,999);
                 
insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_at_from,arrival_at_to,available,collected , rate) 
			  	 values("Delta Airlines", 777, "O'Hare", "JFK", "2017-04-03 20:45:00",  "2017-04-04 07:00:00", "Upcoming", 777,452);
                 
insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_at_from,arrival_at_to,available,collected,rate) 
			  	 values("Delta Airlines", 777, "O'Hare", "JFK", "2017-04-02 19:45:00",  "2017-04-02 23:00:00", "Upcoming", 777,2032);
insert into tbl_flight (airlineName,airplacneModel,from_place,to_place,depart_at_from,arrival_at_to,available,collected,rate)   
				 values("Delta Airlines", 777, "JFK", "DFW", "2017-04-19 22:30:00",  "2017-04-20 06:00:00", "Upcoming", 777,1523);
                 
                 
