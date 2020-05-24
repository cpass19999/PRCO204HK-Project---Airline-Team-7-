from fight_booking.flight.form import From_search_flight
from fight_booking.flight.model import Flight, Order
from fight_booking.main import main
from fight_booking import app, flight, decorator_permission
from fight_booking import db
from flask import render_template, flash, redirect, url_for, request, abort, session
from flask_login import login_required, current_user
from fight_booking.main.form import FormUserInfo, FormRole_Func_manager, Form_User_Role_manager, FormUserEdit, \
    Form_cacredit_card
from fight_booking.user.form import FormFunc, FormRole
from fight_booking.user.model import UserReister, Func, Role


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
@app.route('/')
def index():
    """
    首頁
    :return:
    """
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

    return render_template('index.html',form = form)

@main.route('/edituserinfo', methods=['GET', 'POST'])
@login_required
def edituserinfo():
    form = FormUserInfo()
    if form.validate_on_submit():
        current_user.user_fullname = form.user_fullname.data
        current_user.address = form.address.data
        current_user.gender = form.gender.data
        current_user.passportID = form.passportID.data
        current_user.contactNo = form.contactNo.data
        db.session.add(current_user)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return redirect(url_for('main.userinfo', username=current_user.user_username))
    form.user_fullname.data = current_user.user_fullname
    form.address.data = current_user.address
    form.contactNo.data = current_user.contactNo
    form.gender.data = current_user.gender
    return render_template('main/editUserInfo.html', form=form)

@main.route('/edituser/<username>', methods=['GET', 'POST'])
@login_required
def edituser(username):
    if not current_user.has_role('ADMIN'):
        abort(404)

    user = UserReister.query.filter_by(user_username = username).first()
    form = FormUserEdit()
    if form.validate_on_submit():
        user.user_fullname = form.user_fullname.data
        user.address = form.address.data
        user.gender = form.gender.data
        user.passportID = form.passportID.data
        user.contactNo = form.contactNo.data
        db.session.add(user)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return redirect(url_for('main.edituser', username=user.user_username))
    form.user_username.data = user.user_username
    form.user_email.data = user.user_email
    form.user_fullname.data = user.user_fullname
    form.address.data = user.address
    form.contactNo.data = user.contactNo
    form.gender.data = user.gender
    form.user_confirm.data = user.user_confirm
    return render_template('main/editUser.html', form=form)


@main.route('/userinfo/<username>')
@login_required
def userinfo(username):
    Usercolumns = ['Full name', 'Email', 'contactNo']
    ordercolums = ['order id','from','To', 'Paid','price']
    user = UserReister.query.filter_by(user_username= username).first()
    if user is None or not current_user.user_username == username:
        abort(404)
    return render_template('main/UserInfo.html', user=user,Usercolumns=Usercolumns,ordercolums = ordercolums)


@main.route('/viewfunction/c/', methods=['GET', 'POST'])
def view_function_c():
    """
    註冊View_Function的__module__與__name__，後續才有辦法在權限上設置取得
    :return:
    """
    form = FormFunc()
    if form.validate_on_submit():
        func = Func(
            func_module_name=form.func_module_name.data,
            func_description=form.func_description.data,
            func_is_activate=form.func_is_activate.data,
            func_remark=form.func_remark.data)
        db.session.add(func)
        db.session.commit()
        flash('New Func %s Register Success..' % form.func_module_name.data)
        return redirect(url_for('main.view_function_c'))
    return render_template('main/createViewFunction.html', form=form)

@main.route('/viewfunction/r/<int:page>/', methods=['GET'])
def view_function_r(page=1):
    """
    查詢View Function List
    :return:
    """
    #  欄位名稱
    columns = ['ID', 'Module_Name', 'Func_Description', 'is_activate' , 'Func_Remark']
    funcs = Func.query.paginate(page, 5, False)
    return render_template('main/readViewFunction.html', funcs=funcs, columns=columns)

@main.route('/viewfunction/e/<int:func_id>/', methods=['GET', 'POST'])
@login_required
def view_function_e(func_id):
    """
    編輯View Function
    利用WTForm的obj來渲染Model讀出的資料，前提在於兩邊的名稱設置需要一致。
    :param func_id: func's pk values
    :return:
    """
    func = Func.query.filter_by(id=func_id).first_or_404()
    form = FormFunc(obj=func)
    if form.validate_on_submit():
        form.populate_obj(func)
        db.session.commit()
        flash('Update Func Success!')
        return redirect(url_for('main.view_function_r', page=1))
    return render_template('main/createViewFunction.html', form=form)

@main.route('/rolemanager/c/', methods=['GET', 'POST'])
@login_required
def role_manager_c():
    """
    建立角色
    :return:
    """
    form = FormRole()
    if form.validate_on_submit():
        role = Role(
            name=form.name.data)
        db.session.add(role)
        db.session.commit()
        flash('New Role %s Register Success..' % form.name.data)
        return redirect(url_for('main.role_manager_c'))
    return render_template('main/managerRole.html', form=form, action='create')

@main.route('/rolemanager/r/<int:page>/', methods=['GET'])
@login_required
def role_manager_r(page=1):
    """
    查詢Role
    :return:
    """
    #  欄位名稱
    columns = ['ID', 'Role_Name']
    roles = Role.query.paginate(page, 10, False)
    return render_template('main/readRole.html', roles=roles, columns=columns)

@main.route('/rolemanager/e/<int:role_id>/', methods=['GET', 'POST'])
@login_required
def role_manager_e(role_id):
    """
    編輯Role
    利用WTForm的obj來渲染Model讀出的資料，前提在於兩邊的名稱設置需要一致。
    :param role_id: role''s pk values
    :return:
    """
    role = Role.query.filter_by(id=role_id).first_or_404()
    form = FormRole(obj=role)
    if form.validate_on_submit():
        form.populate_obj(role)
        db.session.commit()
        flash('Update Role Success!')
        return redirect(url_for('main.role_manager_r', page=1))
    return render_template('main/managerRole.html', form=form, action='edit')


@main.route('/role_func_manager/<int:role_id>/', methods=['GET', 'POST'])
@login_required
def role_func_manager(role_id):
    """
    角色權限管理
    取得角色目標權限以及未存在的權限
    :param role_id:角色id
    :return:
    """
    form = FormRole_Func_manager()
    #  取得角色
    role = Role.query.filter_by(id=role_id).first()
    #  取得目前擁有的View function list
    all_funcs = Func.query.with_entities(Func.id, Func.func_module_name).all()
    #  設置checkbox的項目
    form.all_function_option.choices = [(id, role) for id, role in all_funcs]
    #  以該角色目前擁有的權限做為預設值
    form.all_function_option.default = [role.id for role in role.funcs]
    if form.validate_on_submit():
        #  取得選取得View function項目
        funcs = Func.query.filter(Func.id.in_(form.all_function_option.data))
        #  先清空
        role.funcs.clear()
        for func in funcs:
            #  後寫入
            role.funcs.append(func)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('main.role_manager_r', page=1))
    #  務必執行，預設值才會成功
    form.process()
    return render_template('main/Role_Func_manager.html', form=form)

@main.route('/user_role_manager/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def user_role_manager(user_id):
    """
    使用者角色管理
    設置使用者角色
    :param user_id: 使用者id
    :return:
    """
    form = Form_User_Role_manager()
    #  取得使用者資料
    user = UserReister.query.filter_by(user_id=user_id).first()
    #  取得目前擁有的Role list
    all_roles = Role.query.with_entities(Role.id, Role.name).all()
    #  設置checkbox的項目
    form.all_role_option.choices = [(id, name) for id, name in all_roles]
    #  以使用者目前擁有的角色為預設值
    form.all_role_option.default = [role.id for role in user.roles]
    if form.validate_on_submit():
        #  取得選取得Role項目
        roles = Role.query.filter(Role.id.in_(form.all_role_option.data))
        #  先清空
        user.roles.clear()
        for role in roles:
            #  後寫入
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash('Modify %s Role Success!' % user.username)
        return redirect(url_for('main.index'))
    #  務必執行，預設值才會成功
    form.process()
    return render_template('main/User_Role_manager.html', form=form)

@main.route('/manage_menu', methods=['GET', 'POST'])
@login_required
@decorator_permission.decorator_permission
def manager_menu():
    return render_template('main/manager_menu.html')

@main.route('/manager_order', methods=['GET', 'POST'])
@login_required
@decorator_permission.decorator_permission
def manager_order():
    ordercolums = ['order id', 'Order user','from', 'To', 'Paid', 'price']
    users = UserReister.query.all()
    orders = Order.query.all()
    return render_template('main/manager_order.html',orders = orders,users = users, ordercolums=ordercolums)

@main.route('/manager_user', methods=['GET', 'POST'])
@login_required
@decorator_permission.decorator_permission
def manager_user():
    Usercolumns = ['user id','user name','Full name', 'Email', 'contactNo','gender','address','regist date','available']
    users = UserReister.query.all()
    orders = Order.query.all()
    return render_template('main/manager_user.html',orders = orders,users = users, Usercolumns=Usercolumns)

@main.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    form = Form_cacredit_card()
    #oid = session.get('orderid', None)
    #oid = 1
    #order = Flight.query.filter_by(order_id = oid).first_or_404()
    #order_id =
    #payment =

    cardNo = form.cardNo.data
    credit_expiration =  form.credit_expiration.data
    security_code = form.security_code.data
    if form.validate_on_submit():
        return redirect(url_for('main.userinfo', username=current_user.user_username))

    return render_template('main/payment.html', form =form)

