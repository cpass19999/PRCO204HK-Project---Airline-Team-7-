from fight_booking.main import main
from fight_booking import app, decorator_permission
from. import flight
from fight_booking import db
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_required, current_user
from fight_booking.flight.form import Form_Testbooking, From_search_flight, From_book_confirm, From_book_flight
from .model import Flight, Order
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
        flight_d = Flight.query.filter_by(flightID=form.flight_id_r.data).first_or_404()

        if form.flight_id_r.data:
            flight_r = Flight.query.filter_by(flightID=form.flight_id_r.data).first_or_404()
            book = Order(
                depart_flightid=form.flight_id_r.data,
                return_flightid=form.flight_id_r.data,
                user_id=form.user_id.data,
                price=flight_r.price + flight_d.price,
                seat_no=form.seat_no.data
            )
        else:
            flight_r = None
            book = Order(
                depart_flightid=form.flight_id_r.data,
                user_id=form.user_id.data,
                price=flight_r.price + flight_d.price,
                seat_no=form.seat_no.data
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
        flight = Flight.query.filter_by(from_place = form.from_place.data , to_place = form.to_place.data,available = 'Upcoming', depart_Date = form.depart_date.data.strftime("%Y-%m-%d"), ).all()
        triptype = form.TripType.data

        if triptype == 'oneway':
            if flight:
                session['triptype'] = triptype
                session['depart_date'] = form.depart_date.data.strftime("%Y-%m-%d")
                return redirect(url_for('flight.search_flight_result',
                                        f_place=form.from_place.data, t_place=form.to_place.data))
            flash('No flight found ')

        if triptype == 'return':
            if form.return_date.data > form.depart_date.data :
                if flight:
                    session['triptype'] = triptype
                    session['depart_date'] = form.depart_date.data.strftime("%Y-%m-%d")
                    session['return_date'] = form.return_date.data.strftime("%Y-%m-%d")
                    return redirect(url_for('flight.search_flight_result',
                                            f_place =form.from_place.data , t_place = form.to_place.data))
                    flash ('No flight found ' )
                flash('Retrun date must after depart date')

    return render_template('flight_main/search_flight.html', form=form)

@flight.route('/searchresult/<f_place>&<t_place>', methods=['GET', 'POST'])
def search_flight_result(f_place,t_place):
    form = From_book_flight()

    #flights = Flight.query.all()
    depart_date = session.get('depart_date',None)
    return_date = session.get('return_date', None)
    triptype = session.get('triptype', None)


    columns = ['Airline', 'From','To','Depart Date', 'Depart Time','Price']
    if triptype == 'oneway':
        flights_1 = Flight.query.filter_by(from_place=f_place, to_place=t_place, depart_Date=depart_date,
                                           available='Upcoming').all()
        flights_2 = None
        trip = 'one way trip'

    else:
        trip = 'Round  trip'
        flights_1 = Flight.query.filter_by(from_place=f_place, to_place=t_place, depart_Date = depart_date, available = 'Upcoming').all()
        flights_2 = Flight.query.filter_by(from_place=t_place, to_place=f_place, depart_Date = return_date, available = 'Upcoming').all()


    if form.validate_on_submit():
        session['depart_id'] = request.form.get('depart_id', None)
        session['return_id'] = request.form.get('return_id', None)
        return redirect((url_for('flight.book_confirm')))

    return render_template('flight_main/search_result.html',flights_1= flights_1, flights_2 = flights_2 ,columns=columns, trip = trip , triptype = triptype,form=form)

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

@flight.route('/OrderDetail/<order_id>', methods=['GET', 'POST'])
@login_required
def order_detail(order_id):
    form = From_book_confirm()
    columns = ['Airline', 'From', 'To', 'Depart Date', 'Depart Time', 'Price']
    order = Order.query.filter_by().first_or_404()
    flights_1 = order.flight_d('d')
    flights_2 = order.flight_d('r')
    #return render_template('booking_main/booking_detail.html',  flight_d= flights_1, flight_r = flights_2, order = order, columns=columns)
    form.seat_no.data = order.seat_no

    if form.validate_on_submit():
        if form.confirmPay:
            order.paid = True
            db.session.commit()
            flash('Your order is Paid')
            return redirect(url_for('main.payment'))
            #return redirect(url_for('main.userinfo', username=current_user.user_username))

    return render_template("flight_main/book_confirm.html", flight_d=flights_1, flight_r=flights_2, form=form,columns=columns)

@flight.route('/Orderconfirm/' , methods=['GET','POST'])
@login_required
def book_confirm():
    form = From_book_confirm()
    columns = ['Airline', 'From','To','Depart Date', 'Depart Time','Price']

    depart_id = session.get('depart_id', None)
    return_id = session.get('return_id', None)
    triptype = session.get('triptype', None)

    if triptype == 'oneway':
        flight_d = Flight.query.filter_by(flightID=depart_id).first_or_404()
        flight_r = None
        book = Order(
            user_id=current_user.user_id,
            seat_no=form.seat_no.data,
            price=flight_d.price,
            depart_flightid=flight_d.flightID,
            return_flightid= None
        )
    else:
        flight_d = Flight.query.filter_by(flightID=depart_id).first_or_404()
        flight_r = Flight.query.filter_by(flightID=return_id).first_or_404()
        book = Order(
            user_id=current_user.user_id,
            seat_no=form.seat_no.data,
            price=flight_d.price + flight_r.price,
            depart_flightid=flight_d.flightID,
            return_flightid=flight_r.flightID
        )


    if form.validate_on_submit():
        if form.confirmPay:
            book.paid = True
            return redirect(url_for('main.payment'))
            #flash('Your order is confirmed and paid')
        else:
            flash('Your order is confirmed')

        db.session.add(book)
        db.session.commit()
        return redirect(url_for('main.userinfo', username=current_user.user_username))

    return render_template("flight_main/book_confirm.html" , flight_d = flight_d, flight_r = flight_r,form = form,columns=columns)

def search_flight_func():
    form = From_search_flight()
    if form.validate_on_submit():
        flight = Flight.query.filter_by(from_place = form.from_place.data , to_place = form.to_place.data,available = 'Upcoming').all()
        triptype = form.TripType.data

        if form.return_date.data > form.depart_date.data:
            if flight:
                session['triptype'] = triptype
                session['depart_date'] = form.depart_date.data.strftime("%Y-%m-%d")
                session['return_date'] = form.return_date.data.strftime("%Y-%m-%d")
                return redirect(url_for('flight.search_flight_result',
                                        f_place =form.from_place.data , t_place = form.to_place.data))
                flash ('No flight found ' )
        flash('Retrun date must after depart date')