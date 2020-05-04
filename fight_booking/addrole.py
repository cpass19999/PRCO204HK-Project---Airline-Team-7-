from fight_booking import db
from fight_booking.user import Role
from fight_booking.user.model import UserReister, Func

if( not Role.query.filter_by(name = 'ADMIN').first()):
    role_admin = Role(
        name = 'ADMIN')

    func_add_book = Func(
        func_module_name='fight_booking.flight.view.add_booking_user',
        func_description='add booking for other user')

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

    db.session.add(role_admin)
    db.session.add(admin)
    db.session.commit()