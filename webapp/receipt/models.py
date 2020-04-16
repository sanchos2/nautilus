from sqlalchemy.orm import relationship
from sqlalchemy import func
from webapp.db import db


class Purchase(db.Model):
    # fn_number - fn, fd_number - i, fpd_number - fp
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fn_number = db.Column(db.String, unique=True)
    fd_number = db.Column(db.String)
    fpd_number = db.Column(db.String)
    receipt_type = db.Column(db.String)
    date = db.Column(db.DateTime)
    sum = db.Column(db.Integer)
    valid = db.Column(db.String)

    user = relationship('User', backref='purchases')

    def __repr__(self):
        return f'<Покупка - {self.id}, за дату - {self.date}, на сумму - {self.sum}, валидность - {self.valid}'


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('purchase.id')) # TODO purchase_id
    product = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.DECIMAL) # TODO Float
    sum = db.Column(db.Integer)
    category = db.Column(db.String)
    subcategory = db.Column(db.String)

    purchase = relationship('Purchase', backref='receipts')

    def __repr__(self):
        return f'<Позиция по чеку - {self.product}, сумма позиции - {self.sum}'
