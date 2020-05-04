from fight_booking.main import main
from fight_booking import app, decorator_permission
from. import flight
from fight_booking import db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from fight_booking.flight.form import Form_Testbooking, From_search_flight, From_book_confirm
from .model import Flight, Booking
from ..user.form import FormFunc
from ..user.model import Func


@flight.route('/flight/t', methods=['GET', 'POST'])
@decorator_permission.decorator_permission
@login_required
def add_booking_user():
    """使用者編輯blog"""
    #if not current_user.check_admin('fight_booking.view','add_booking_user'):
       # flash('You Have No Author!')
        #return redirect(url_for('main.index'))

    form = Form_Testbooking()
    if form.validate_on_submit():
        book = Booking(
            flight_id=form.flight_id.data,
            user_id=current_user.user_id,
            seat_no = form.seat_no.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Create New Blog Success')
        #return redirect(url_for('main.userinfo', username=current_user.user_username))
    return render_template('flight_main/bookingtest.html', form=form)

@flight.route('/flight_test/')
@decorator_permission.decorator_permission
@login_required
def flight_test():
    return 'i am test route'

@flight.route('/searchflight', methods=['GET', 'POST'])
def search_flight():
    form = From_search_flight()
    if form.validate_on_submit():
        flights = Flight.query.all()
        flight = Flight.query.filter_by(from_place = form.from_place.data , to_place = form.to_place.data).all()
        if flight:
            #search_flight_result(form.from_place.data,form.to_place.data)
            return redirect(url_for('flight.search_flight_result', f_place =form.from_place.data , t_place = form.to_place.data))
        flash ('No flight found ' )
    return render_template('flight_main/search_flight.html', form=form)

@flight.route('/searchresult/<f_place>&<t_place>', methods=['GET', 'POST'])
def search_flight_result(f_place,t_place):
    #flights = Flight.query.all()
    flight = Flight.query.filter_by(from_place=f_place, to_place=t_place).first_or_404()
    return render_template('flight_main/search_result.html',flight = flight)

@flight.route('/flightInfo/<flight_ID>/', methods=['GET', 'POST'])
def flight_list(flight_ID):
    """
    :param flight_ID: flight id
    :return:
    """
    flights = Flight.query.filter_by(flightID = flight_ID).all()
    #  利用first_or_404讓系統如果取不到blog的時候就拋出404
    flight = Flight.query.filter_by(flightID=flight_ID).first_or_404()
    return render_template('flight_main/flight_list.html', flights=flights, flight=flight)

@flight.route('/bookingDetail/<booking_ID>', methods=['GET', 'POST'])
@login_required
def booking_detail(booking_ID):
    bookings = Booking.query.filter_by( user_id = current_user.user_id).all()
    booking = Booking.query.filter_by().first_or_404()
    return render_template('booking_main/booking_detail.html', bookings = bookings, booking = booking)

@flight.route('/bookingconfirm/<flight_ID>', methods=['GET', 'POST'])
@login_required
def book_confirm(flight_ID):
    flight = Flight.query.filter_by(flightID=flight_ID).first_or_404()
    form = From_book_confirm()

    if form.validate_on_submit():
        book = Booking(
            flight_id = flight.flightID,
            user_id = current_user.user_id,
            seat_no = form.seat_no.data,
            price = 999
        )

        db.session.add(book)
        db.session.commit()
        flash('Your booking is confirmed')
        return redirect(url_for('main.userinfo', username=current_user.user_username))

    return render_template("flight_main/book_confirm.html" , flight = flight, form = form)

