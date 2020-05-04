from fight_booking import db
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

    admin = UserReister(
    user_username = 'admin',
    user_email = 'admin@admin.com',
    user_confirm = 1,
    password = 'adminadmin',
    user_fullname = 'administator'
     )
    #user = UserReister.query.filter_by(user_username = 'admin').first()


    admin.roles.append(role_admin)
    role_admin.funcs.append(func_add_book)
    role_admin.funcs.append(func_viewfunction_c)
    role_admin.funcs.append(func_view_function_r)
    role_admin.funcs.append(func_view_function_e)
    role_admin.funcs.append(func_role_manager_c)
    role_admin.funcs.append(func_role_manager_r)
    role_admin.funcs.append(func_role_manager_e)
    role_admin.funcs.append(func_role_func_manager)
    role_admin.funcs.append(func_user_role_manager)



    db.session.add(role_admin)
    db.session.add(role_user)
    db.session.add(role_JUNIOR)
    db.session.add(role_SENIOR)
    
    db.session.add(admin)
    db.session.commit()