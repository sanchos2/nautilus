from sqlalchemy.orm import relationship
from webapp.db import db


class Purchase(db.Model):
    # fn_number - fn, fd_number - i, fpd_number - fp
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    fn_number = db.Column(db.String)
    fd_number = db.Column(db.String)
    fpd_number = db.Column(db.String)
    receipt_type = db.Column(db.String)
    date = db.Column(db.DateTime)
    sum = db.Column(db.Float)
    loaded = db.Column(db.String)
    organization = db.Column(db.String)

    user = relationship('User', backref='purchases')

    def __repr__(self):
        return f'<Покупка - {self.id}, за дату - {self.date}, на сумму - {self.sum}, валидность - {self.loaded}'


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id', ondelete='CASCADE'), index=True)
    product = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Float)
    sum = db.Column(db.Integer)
    category = db.Column(db.String)
    subcategory = db.Column(db.String)

    purchase = relationship('Purchase', backref='receipts')

    def __repr__(self):
        return f'<Позиция по чеку - {self.product}, сумма позиции - {self.sum}'
