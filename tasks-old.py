import sys

from webapp import create_app
from webapp.receipt.utils.receipt_handler import add_receipt_db

app = create_app()
with app.app_context():
    add_receipt_db()

sys.exit(0)