import pytest

from webapp.receipt.utils.receipt_handler import *


def test_qr_parser():
    assert qr_parser('t=20200316T1937&s=2683.44&fn=9289000100437652&i=133389&fp=1563903230&n=1') == {'t': '20200316T1937', 's': '2683.44', 'fn': '9289000100437652', 'i': '133389', 'fp': '1563903230', 'n': '1'}
