import sys

from webapp import create_app
from webapp.receipt.utils.receipt_handler import receipt_get_handler

app = create_app()
with app.app_context():
    receipt_get_handler()

sys.exit(0)