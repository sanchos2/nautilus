"""Receipt models."""
from sqlalchemy.orm import relationship

from webapp.db import db


class Purchase(db.Model):
    """Purchase model."""

    # fn_number - fn, fd_number - i, fpd_number - fp
    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True,
    )
    fn_number = db.Column(db.String)
    fd_number = db.Column(db.String)
    fpd_number = db.Column(db.String)
    receipt_type = db.Column(db.String)
    date = db.Column(db.DateTime)
    sum = db.Column(db.Float)  # noqa: WPS125
    loaded = db.Column(db.String)
    organization = db.Column(db.String)

    user = relationship('User', backref='purchases')
    category = relationship('Category', secondary='purchase_category', backref='purchases')

    def __str__(self):
        return self.organization

    def __repr__(self):
        return '<Покупка-{0}, за дату-{1}, на сумму-{2}, валид-{3}'.format(
            self.id, self.date, self.sum, self.loaded,
        )


class PurchaseCategory(db.Model):
    """Purchase - Category."""

    purchase_id = db.Column(
        db.Integer,
        db.ForeignKey('purchase.id', ondelete='CASCADE'),
        primary_key=True,
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id', ondelete='CASCADE'),
        primary_key=True,
    )


class Category(db.Model):
    """Category model."""

    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    category = db.Column(db.String)

    def __str__(self):
        return self.category

    def __repr__(self):
        return f'<Category({self.category})'


class Receipt(db.Model):
    """Receipt model."""

    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    purchase_id = db.Column(
        db.Integer,
        db.ForeignKey('purchase.id', ondelete='CASCADE'),
        index=True,
    )
    product = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Float)
    sum = db.Column(db.Integer)  # noqa: WPS125

    purchase = relationship('Purchase', backref='receipts')
    subcategory = relationship('Subcategory', secondary='receipt_subcategory', backref='receipts')

    def __str__(self):
        return self.product

    def __repr__(self):
        return f'<Позиция по чеку - {self.product}, сумма позиции - {self.sum}'


class ReceiptSubcategory(db.Model):
    """Purchase - Subcategory."""

    receipt_id = db.Column(
        db.Integer,
        db.ForeignKey('receipt.id', ondelete='CASCADE'),
        primary_key=True,
    )
    subcategory_id = db.Column(
        db.Integer,
        db.ForeignKey('subcategory.id', ondelete='CASCADE'),
        primary_key=True,
    )


class Subcategory(db.Model):
    """Subcategory model."""

    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    subcategory = db.Column(db.String)

    category = relationship('Category', secondary='category_subcategory', backref='subcategories')

    def __str__(self):
        return self.subcategory

    def __repr__(self):
        return f'<Category ({self.subcategory})'


class CategorySubcategory(db.Model):
    """Category - Subcategory."""

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id', ondelete='CASCADE'),
        primary_key=True,
    )
    subcategory_id = db.Column(
        db.Integer,
        db.ForeignKey('subcategory.id', ondelete='CASCADE'),
        primary_key=True,
    )
