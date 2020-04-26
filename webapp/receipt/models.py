"""Receipt models."""
from sqlalchemy.orm import relationship
from sqlalchemy_utils import LtreeType

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
    tree = db.Column(db.Integer, db.ForeignKey('category_tree.id'), index=True)

    user = relationship('User', backref='purchases')

    def __str__(self):
        return self.organization

    def __repr__(self):
        return '<Покупка-{0}, за дату-{1}, на сумму-{2}, валид-{3}'.format(
            self.id, self.date, self.sum, self.loaded,
        )


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
    category = db.Column(db.Integer, db.ForeignKey('category.id'), index=True)
    subcategory = db.Column(
        db.Integer,
        db.ForeignKey('subcategory.id'),
        index=True,
    )

    purchase = relationship('Purchase', backref='receipts')
    category_name = relationship('Category', backref='receipts')

    def __str__(self):
        return self.product

    def __repr__(self):
        return f'<Позиция по чеку - {self.product}, сумма позиции - {self.sum}'


class Category(db.Model):
    """Category model."""

    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    category = db.Column(db.String)

    def __str__(self):
        return self.category

    def __repr__(self):
        return f'<CategoryTree({self.category})'


class Subcategory(db.Model):
    """Subcategory model."""

    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id', ondelete='CASCADE'),
        index=True,
    )
    subcategory = db.Column(db.String)

    def __str__(self):
        return self.subcategory

    def __repr__(self):
        return f'<CategoryTree({self.subcategory})'


class CategoryTree(db.Model):
    """Category model."""

    # перед добавлением таблицы в базе установить расширение:
    # create extension if not exists ltree;
    id = db.Column(db.Integer, primary_key=True)  # noqa: WPS125
    name = db.Column(db.String, nullable=False)
    path = db.Column(LtreeType, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<CategoryTree({self.name})'
