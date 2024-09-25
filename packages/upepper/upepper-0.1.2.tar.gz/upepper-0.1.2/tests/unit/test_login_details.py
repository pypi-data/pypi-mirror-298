# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys

# Import Pepper Libs
import upepper.cli

# Import Testing libraries
from mock import MagicMock, patch


def test_interactive_logins():
    sys.argv = ['pepper', '-c', 'tests/.pepperrc', '-p', 'noopts']

    with patch(
             'pepper.cli.input',
             MagicMock(return_value='pepper')
         ), patch(
             'pepper.cli.getpass.getpass',
             MagicMock(return_value='pepper')
         ):
        result = upepper.cli.PepperCli().get_login_details()
    assert result['SALTAPI_USER'] == 'pepper'
    assert result['SALTAPI_PASS'] == 'pepper'
