#!/usr/bin/env python
# -*-coding:utf-8-*-

import re
import os

from dotenv import load_dotenv
load_dotenv()

access_key = os.getenv('ACCESS_KEY_ID')
access_key_secret = os.getenv('ACCESS_KEY_SECRET')


def check_phone_verification_code(phone_number, biz_id, send_date, verification_code):
    """
    TODO
    """
    return True


