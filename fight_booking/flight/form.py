from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, TextAreaField, IntegerField, SelectField, DateTimeField, \
    DateField
from fight_booking.flight.model import Flight, Airport, airline
from datetime import date


class Form_Testbooking(Form):
    """
    建置blog表頭的表單
    """
    flight_id = StringField('flight_id', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])
    user_id = StringField('User id', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])

    seat_no = IntegerField('seatNo', validators=[
         validators.NumberRange(1,250)])

    submit = SubmitField('Add booking')

class From_search_flight(Form):

    from_place = SelectField('From',coerce=str)
    to_place = SelectField('To',coerce=str)

    submit = SubmitField('Search Flight')


    def __init__(self):
        super(From_search_flight, self).__init__()
        self.from_place.choices = self._get_airport_localtion()
        self.to_place.choices = self._get_airport_localtion()

    def _get_airport_localtion(self):
        obj = Airport.query.with_entities( Airport.airportNname,Airport.airportNname).all()
        return obj

    def _get_airline(self):
        obj = airline.query.all()
        return obj

class From_book_confirm(Form):
    seat_no = IntegerField('seatNo', validators=[
        validators.NumberRange(1, 250)])
    submit = SubmitField('confirm')