import pytest

from webapp.receipt.utils.receipt_handler import *


def test_qr_parser():
    assert qr_parser('') == {}
    assert qr_parser(12345) == {}
    assert qr_parser('13758405fdhasljrie38402183') == {}
    assert qr_parser(
        't=20200316T1937&s=2683.44&fn=9289000100437652&i=133389&fp=1563903230'
    ) == {}
    assert qr_parser(
        't=20200316T1937&s=2683.44&fn=9289000100437652&i=133389&fp=1563903230&n=1'
    ) == {
        't': '20200316T1937',
        's': '2683.44',
        'fn': '9289000100437652',
        'i': '133389',
        'fp': '1563903230',
        'n': '1',
    }


def test_recovery_pass():
    pass


def test_registration_fns():
    pass


def test_add_receipt_db():
    pass


def test_receipt_get_handler():
    pass


def test_purchase_valid_handler():
    pass


def test_format_date():
    from datetime import datetime
    assert format_date('20140220T1803') == datetime(2014, 2, 20, 18, 3)
    assert format_date('20140220T180305') == datetime(2014, 2, 20, 18, 3, 5)
    assert format_date('') == datetime.now().replace(microsecond=0)
    assert format_date('12345') == datetime.now().replace(microsecond=0)


def test_convert_date_to_fns_format():
    assert convert_date_to_fns_format(datetime(2014, 2, 20, 18, 3)) == '2014-02-20T18:03'
    assert convert_date_to_fns_format(datetime(2014, 2, 20, 18, 3, 5)) == '2014-02-20T18:03'