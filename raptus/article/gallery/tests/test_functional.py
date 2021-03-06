# -*- coding: utf-8 -*-
"""Functional tests for basic UI functionalities using zope.testbrowser."""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing import layered
from plone.testing.z2 import Browser
from raptus.article.gallery.tests.base import FUNCTIONAL_TESTING
from Testing.ZopeTestCase.utils import startZServer

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import transaction
import unittest2 as unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE


def setUp(self):
    layer = self.globs['layer']
    # Update global variables within the tests.
    self.globs.update({
        'portal': layer['portal'],
        'browser': Browser(layer['app']),
        'startZServer': startZServer,
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
        'PNG_IMAGE': ('\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00'
                     '\x01\x01\x00\x00\x00\x007n\xf9$\x00\x00\x00\nIDATx\x9cc`\x00\x00'
                     '\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82')
    })

    portal = self.globs['portal']
    browser = self.globs['browser']

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()
    setRoles(portal, TEST_USER_ID, ['Manager'])

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags)
    m += manuel.codeblock.Manuel()

    suite = layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)
    return suite


def test_suite():
    return unittest.TestSuite([
        DocFileSuite('story.txt'),
        ])
