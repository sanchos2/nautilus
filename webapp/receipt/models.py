from webapp.db import db


class Purchase(db.Model):
    # fn_number - fn, fd_number - i, fpd_number - fp
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fn_number = db.Column(db.String, unique=True)
    fd_number = db.Column(db.String)
    fpd_number = db.Column(db.String)
    receipt_type = db.Column(db.String)
    date = db.Column(db.String)
    sum = db.Column(db.Integer)

    def __repr__(self):
        return f'<Покупка пользователя - {self.user_id}, за дату - {self.date}, на сумму - {self.sum}'


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    product = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.DECIMAL)
    sum = db.Column(db.Integer)
    category = db.Column(db.String)
    subcategory = db.Column(db.String)

    def __repr__(self):
        return f'Чек пользователя - {self.receipt_id}, сумма чека - {self.sum}'

