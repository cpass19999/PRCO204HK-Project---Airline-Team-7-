from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint
from fight_booking import db
from datetime import datetime


class Flight(db.Model):
    __tablename__ = 'tbl_flight'
    __table_args__ = (
        PrimaryKeyConstraint('flightID'),
        ForeignKeyConstraint(['airlineName'], ['airline.airlineName'], name='FK_airlineName'),
    )
    flightID = db.Column(db.Integer, autoincrement=True, primark_key=True)
    # flightID = db.Column(db.String(30), unique=True, nullable=False)
    airlineName = db.Column(db.String(30), db.ForeignKey('airline.airlineName'), nullable=False,)
    flightNo = db.Column(db.String(30), nullable=False)
    airplacneModel = db.Column(db.String(30), nullable=False)
    from_place = db.Column(db.String(30), nullable=False)
    to_place = db.Column(db.String(30), nullable=False)
    depart_Date = db.Column(db.Date, nullable=False)
    depart_Time = db.Column(db.Time, nullable=False)
    #arrival_at_to = db.Column(db.DateTime)
    available = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable = False)


    airline = db.relationship("airline", backref=db.backref('airline', lazy=True))
    #airport = db.relationship("Airport", backref=db.backref('Airport', lazy=True))
    #airplacnes = db.relationship("airplacnes", backref=db.backref('airplacnes', lazy=True))
    # bookings = db.relationship("UserReister", secondary="booking" , backref=db.backref('flights', lazy='dynamic') )

    def __str__(self):
        return str(self.flightID) + str(self.from_place) + str(self.to_place) + str(self.depart_at_from) + str(
            self.arrival_at_to)

    @property
    def flightNo(self):
        raise AttributeError('Flight No is not a readable attribute')

    @flightNo.setter
    def flightNo(self):
        self.flightNo = airline.airline_short + self.flightID


    def __init__(self,airlineName,airplacneModel,from_place,to_place,depart_at_from,arrival_at_to,available):
        self.airlineName = airlineName
        self.airplacneModel = airplacneModel
        self.from_place = from_place
        self.to_place = to_place
        self.depart_at_from = depart_at_from
        self.arrival_at_to = arrival_at_to
        self.available = available

class airline(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('airlineID'),
    )
    airlineID = db.Column(db.Integer, autoincrement=True, primark_key=True)
    airlineName = db.Column(db.String(30), unique=True, nullable=False)
    airline_short = db.Column(db.String(5), unique=True, nullable=False)

    def __init__(self, name):
        self.airlineName = name

    def get_short(self):
        return self.airline_short


class Airport(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('airportID'),
    )
    airportID = db.Column(db.Integer, autoincrement=True, primark_key=True)
    airportNname = db.Column(db.String(30), unique=True, nullable=False)
    airport_localtion = db.Column(db.String(30), nullable=False)


class airplacnes(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('airplacneID'),
    )
    airplacneID = db.Column(db.Integer, autoincrement=True, primark_key=True)
    airlineName = db.Column(db.String(30), unique=True)
    airplacneModel = db.Column(db.String(30),nullable=False)
    airplacneTotalSeats = db.Column(db.Integer, nullable=False)

    def __init__(self, airlineName, airplacneTotalSeats):
        self.airlineName = airlineName
        self.airplacneTotalSeats = airplacneTotalSeats

    def __repr__(self):
        return '<airplacnes> %s' % self.airlineName


class Order(db.Model):
    __tablename__ = 'Order'
    __table_args__ = (
        PrimaryKeyConstraint('Order_id'),
        ForeignKeyConstraint(['user_id'], ['tbl_user.user_id'], name='FK_userid'),
        ForeignKeyConstraint(['flight_id'], ['tbl_flight.flightID'], name='FK_flightID'),
    )

    Order_id = db.Column(db.Integer, autoincrement=True, primark_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.user_id'))
    # user = db.relationship("UserReister", backref=db.backref('bookings', lazy=True))
    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flight.flightID'))
    # flight = db.relationship("UserReister", backref=db.backref('bookings', lazy=True))
    seat_no = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    price = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default = False)
    canceled = db.Column(db.Boolean, default=False)
    flights = db.relationship("Flight", backref=db.backref('flights', lazy=True))

    def __init__(self, user_id, flight_id, seat_no, price):
        self.user_id = user_id
        self.flight_id = flight_id
        self.seat_no = seat_no
        self.price = price

# db.create_all()
