from sqlalchemy import PrimaryKeyConstraint,ForeignKeyConstraint
from fight_booking import db
from datetime import  datetime



class Flight(db.Model):
    __tablename__ = 'tbl_flight'
    __table_args__ = (
        PrimaryKeyConstraint('flightID'),
    )
    flightID = db.Column(db.Integer, autoincrement=True , primark_key=True)
    #flightID = db.Column(db.String(30), unique=True, nullable=False)
    airlineName = db.Column(db.String(30), nullable=False)
    flightNo = db.Column(db.String(30), nullable=False)
    airplacneModel = db.Column(db.String(30), nullable=False)
    from_place = db.Column(db.String(30), nullable=False)
    to_place = db.Column(db.String(30), nullable=False)
    depart_at_from = db.Column(db.DateTime, nullable=False)
    arrival_at_to = db.Column(db.DateTime)
    available = db.Column(db.String(30), nullable=False)
    rate = db.Column(db.Integer)
    off = db.Column(db.Integer)
    collected = db.Column(db.Integer)

    #bookings = db.relationship("UserReister", secondary="booking" , backref=db.backref('flights', lazy='dynamic') )

    def __str__(self):
        return str(self.flightID) + str(self.from_place) + str(self.to_place) + str(self.depart_at_from) + str(
            self.arrival_at_to)

    @property
    def flightNo(self):
        raise AttributeError('Flight No is not a readable attribute')

    @flightNo.setter
    def flightNo(self):
        self.flightNo = airline.airline_short + self.flightID

class airline(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('airlineID'),
    )
    airlineID   = db.Column(db.Integer, autoincrement=True , primark_key=True)
    airlineName = db.Column(db.String(30), unique=True, nullable=False)
    airline_short = db.Column(db.String(5), unique=True, nullable=False)

    def __init__(self,name):
        self.airlineName = name

    def get_short(self):
        return self.airline_short

class Airport(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('airportID'),
    )
    airportID = db.Column(db.Integer, autoincrement=True , primark_key=True)
    airportNname = db.Column(db.String(30), unique=True, nullable=False)
    airport_localtion = db.Column(db.String(30), nullable=False)

class airplacnes(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('airplacneID'),
    )
    airplacneID = db.Column(db.Integer, autoincrement=True, primark_key=True)
    airlineName = db.Column(db.String(30), unique=True)
    airplacneModel = db.Column(db.String(30), nullable=False)
    airplacneTotalSeats = db.Column(db.Integer, nullable=False)

    def __init__(self,airlineName,airplacneTotalSeats):
        self.airlineName = airlineName
        self.airplacneTotalSeats = airplacneTotalSeats

    def __repr__(self):
        return '<airplacnes> %s' % self.airlineName

class Booking(db.Model):
    __tablename__ = 'booking'
    __table_args__ = (
        PrimaryKeyConstraint('Booking_ID'),
        ForeignKeyConstraint(['user_id'],['tbl_user.user_id'], name='FK_userid'),
        ForeignKeyConstraint(['flight_id'], ['tbl_flight.flightID'], name='FK_flightID'),
    )

    Booking_ID = db.Column(db.Integer, autoincrement=True , primark_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('tbl_user.user_id'))
    #user = db.relationship("UserReister", backref=db.backref('bookings', lazy=True))
    flight_id = db.Column(db.Integer,db.ForeignKey('tbl_flight.flightID'))
    #flight = db.relationship("UserReister", backref=db.backref('bookings', lazy=True))
    seat_no = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    price = db.Column(db.Integer)

    def __init__(self,user_id,flight_id,seat_no,price):
        self.user_id = user_id
        self.flight_id = flight_id
        self.seat_no = seat_no
        self.price = price


#db.create_all()