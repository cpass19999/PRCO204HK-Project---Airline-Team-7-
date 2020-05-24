from fight_booking import db
from fight_booking.flight.model import Flight, airline
from fight_booking.user import Role
from fight_booking.user.model import UserReister, Func

if( not Role.query.filter_by(name = 'ADMIN').first()):

    role_admin = Role(
        name = 'ADMIN')

    role_user = Role("USER")
    role_SENIOR = Role("SENIOR")
    role_JUNIOR = Role("JUNIOR")



    func_add_book = Func(
        func_module_name='fight_booking.flight.view.add_booking_user',
        func_description='add booking for other user')

    func_viewfunction_c = Func(
        func_module_name='fight_booking.main.view.view_function_c',
        func_description=' ')

    func_view_function_r = Func(
        func_module_name='fight_booking.main.view.view_function_r',
        func_description=' ')

    func_view_function_e = Func(
        func_module_name='fight_booking.main.view.view_function_e',
        func_description=' ')

    func_role_manager_c = Func(
        func_module_name='fight_booking.main.view.role_manager_c',
        func_description=' ')

    func_role_manager_r = Func(
        func_module_name='fight_booking.main.view.role_manager_r',
        func_description=' ')

    func_role_manager_e = Func(
        func_module_name='fight_booking.main.view.role_manager_e',
        func_description=' ')

    func_role_func_manager = Func(
        func_module_name='fight_booking.main.view.role_func_manager',
        func_description=' ')

    func_user_role_manager = Func(
        func_module_name='fight_booking.main.view.user_role_manager',
        func_description=' ')


    func_user_role_manager_users = Func(
        func_module_name='fight_booking.main.view.manager_user',
        func_description=' ')

    func_user_role_manager_odrers = Func(
        func_module_name='fight_booking.main.view.manager_order',
        func_description=' ')




    admin = UserReister(
    user_username = 'admin',
    user_email = 'admin@admin.com',
    user_confirm = 1,
    password = 'adminadmin',
    user_fullname = 'administator'
     )
    #user = UserReister.query.filter_by(user_username = 'admin').first()
    senior = UserReister(
    user_username = 'senior',
    user_email = 'senior@admin.com',
    user_confirm = 1,
    password = 'seniorsenior',
    user_fullname = 'seniorOfFlight'
     )

    s1001 = UserReister(
    user_username = 's1001',
    user_email = 's1001@email.com',
    user_confirm = 1,
    password = '12345678',
    user_fullname = 's1001_01'
     )

    admin.roles.append(role_admin)
    admin.roles.append(role_SENIOR)
    admin.roles.append(role_JUNIOR)
    admin.roles.append(role_user)

    senior.roles.append(role_SENIOR)
    senior.roles.append(role_JUNIOR)
    admin.roles.append(role_user)

    role_admin.funcs.append(func_add_book)
    role_admin.funcs.append(func_viewfunction_c)
    role_admin.funcs.append(func_view_function_r)
    role_admin.funcs.append(func_view_function_e)
    role_admin.funcs.append(func_role_manager_c)
    role_admin.funcs.append(func_role_manager_r)
    role_admin.funcs.append(func_role_manager_e)
    role_admin.funcs.append(func_role_func_manager)
    role_admin.funcs.append(func_user_role_manager)
    role_admin.funcs.append(func_user_role_manager_users)
    role_admin.funcs.append(func_user_role_manager_odrers)

    role_SENIOR.funcs.append(func_add_book)

    Emirates = airline(
        name = "Emirates",
        airline_short = "EA"
    )


    flight1 = Flight(
        airlineName ="Emirates",
        airplacneModel =777,
        from_place ="JFK",
        to_place ="O'Hare",
        depart_Date ="2020-06-19",
        depart_Time ="22:30:00",
        available = "Upcoming",
        price = 999
        )

    flight2 = Flight(
                 airlineName="Emirates",
                 airplacneModel=777,
                 from_place="O'Hare",
                 to_place="O'Hare",
                 depart_Date="2020-05-15",
                 depart_Time="10:30:00",
                 available="Upcoming",
                 price=899
             )


    db.session.add(role_admin)
    db.session.add(role_user)
    db.session.add(role_JUNIOR)
    db.session.add(role_SENIOR)

    db.session.add(admin)
    db.session.add(senior)
    db.session.add(s1001)
    db.session.commit()