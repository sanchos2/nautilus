"""Admin views."""
from flask import Blueprint, flash, redirect, render_template, url_for

from webapp.db import db
from webapp.admin.forms import CategoryForm, SubcategoryForm
from webapp.receipt.models import Category, Subcategory
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    """Admin page with category and subcategory adding functions."""
    category_list = Category.query.all()
    category_form = CategoryForm()
    subcategory_list = Subcategory.query.all()
    subcategory_form = SubcategoryForm()
    category_choices = Category.query.all()
    subcategory_form.category.choices = [
        (category.id, category.category) for category in category_choices
    ]
    return render_template(
        'admin/admin_index.html',
        category_list=category_list,
        category_form=category_form,
        subcategory_list=subcategory_list,
        subcategory_form=subcategory_form,
    )


@blueprint.route('/category-add', methods=['POST'])
@admin_required
def category_add():
    """Category add function."""
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(category=form.category.data)
        db.session.add(new_category)
        db.session.commit()
        flash('Категория добавлена')
        return redirect(url_for('admin.admin_index'))
    flash('Категория не добавлена')
    return redirect(url_for('admin.admin_index'))


@blueprint.route('/subcategory-add', methods=['POST'])
@admin_required
def subcategory_add():
    """Subcategory add function."""
    subcategory_form = SubcategoryForm()
    if subcategory_form.validate_on_submit():
        new_subcategory = Subcategory(
            category_id=subcategory_form.category.data,
            subcategory=subcategory_form.subcategory.data,
        )
        db.session.add(new_subcategory)
        db.session.commit()
        flash('Субкатегория добавлена')
        return redirect(url_for('admin.admin_index'))
    flash('Субкатегория не добавлена')
    return redirect(url_for('admin.admin_index'))
