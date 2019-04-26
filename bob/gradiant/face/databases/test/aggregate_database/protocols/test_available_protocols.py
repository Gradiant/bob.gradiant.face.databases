#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2018+ Gradiant, Vigo, Spain
import unittest


from bob.gradiant.face.databases import protocol_checker, AggregateDatabase
from bob.gradiant.face.databases.classes.aggregate_database.protocols.capture_device_low_quality_access_type_low_quality import \
    CAPTURE_DEVICE_LOW_QUALITY_ACCESS_TYPE_LOW_QUALITY_PROTOCOL


class UnitTestAvailableProtocols(unittest.TestCase):

    def test_should_not_throw_any_exception_for_available_protocols(self):
        for protocol in AggregateDatabase.get_available_protocols().values():
            protocol_checker(protocol)
