# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.showreferences.testing import COLLECTIVE_SHOWREFERENCES_INTEGRATION_TESTING  # noqa
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from Products.CMFPlone.utils import safe_unicode

from plone import api
from zope.event import notify

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that bgp.AdminTools is properly installed."""

    layer = COLLECTIVE_SHOWREFERENCES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Member', 'Contributor'])

    def test_links(self):
        doc1 = api.content.create(
            container=self.portal,
            type='Document',
            title=u'A Document with links',
            id='doc1',
        )
        doc2 = api.content.create(
            container=self.portal,
            type='Document',
            title=u'A Document without links',
            id='doc2',
        )

        new_text = '''<p><a class="internal-link"
            href="resolveuid/{}" target="_self" title="">
             A link to
            </a></p>'''.format(doc2.UID())
        from Products.Archetypes.interfaces.base import IBaseContent
        if IBaseContent.providedBy(doc1):
            # Handle Archetypes
            doc1.setText(new_text)
        else:
            # Handle Dexterity
            from plone.app.textfield.value import RichTextValue
            doc1.text = RichTextValue(
                raw=safe_unicode(new_text),
                mimeType='text/plain',
                outputMimeType='text/x-html-safe')
        from zope.lifecycleevent import ObjectModifiedEvent
        notify(ObjectModifiedEvent(doc1))
        refs_view = doc1.restrictedTraverse('item_references')
        refs = refs_view.references()
        self.assertEqual(len(refs['links']), 1)
        self.assertEqual(len(refs['backlinks']), 0)

        refs_view = doc2.restrictedTraverse('item_references')
        refs = refs_view.references()
        self.assertEqual(len(refs['links']), 0)
        self.assertEqual(len(refs['backlinks']), 1)

    def test_refs(self):
        doc1 = api.content.create(
            container=self.portal,
            type='Document',
            title=u'A Document with refs',
            id='doc1',
        )
        doc2 = api.content.create(
            container=self.portal,
            type='Document',
            title=u'A Document without refs',
            id='doc2',
        )

        from Products.Archetypes.interfaces.base import IBaseContent
        if IBaseContent.providedBy(doc1):
            # Handle Archetypes
            doc1.addReference(doc2)
        else:
            # Handle Dexterity
            raise NotImplementedError
        from zope.lifecycleevent import ObjectModifiedEvent
        notify(ObjectModifiedEvent(doc1))
        refs_view = doc1.restrictedTraverse('item_references')
        refs = refs_view.references()
        self.assertEqual(len(refs['refs']), 1)
        self.assertEqual(len(refs['backrefs']), 0)

        refs_view = doc2.restrictedTraverse('item_references')
        refs = refs_view.references()
        self.assertEqual(len(refs['refs']), 0)
        self.assertEqual(len(refs['backrefs']), 1)
