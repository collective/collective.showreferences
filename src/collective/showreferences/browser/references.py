# -*- coding: UTF-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser import BrowserView
from collections import defaultdict
from plone import api
from plone.app.linkintegrity.handlers import referencedRelationship

try:
    import pkg_resources
    pkg_resources.get_distribution('Products.Archetypes')
except pkg_resources.DistributionNotFound:
    HAS_ARCHETYPES = False
else:
    HAS_ARCHETYPES = True
    from Products.Archetypes.interfaces.referenceable import IReferenceable

try:
    import pkg_resources
    pkg_resources.get_distribution('plone.app.relationfield')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
    pass
else:
    HAS_DEXTERITY = True
    from z3c.relationfield.index import dump
    from zc.relation.interfaces import ICatalog
    from zope.component import queryUtility

import logging

logger = logging.getLogger(__name__)


class ItemReferences(BrowserView):

    def references(self):
        """ Return a dict with all refs and backrefs fo the current object.

        Links are html-links in richtext-fields. They are stored in the
        relation_catalog when linkintegrity-support is enabled.
        For archetypes-objects that works ootb.

        For dexterity-object two additional packages need to be installed
        and their respective behaviors need to be enabled:

        1. plone.app.relationfield adds support for relations to arbitrary
        objects. Behavior: plone.app.relationfield.behavior.IRelatedItems

        2. plone.app.referenceablebehavior ads intid-support to dx-items and
        allows linkintegrity to work with them.
        Behavior: plone.app.referenceablebehavior.referenceable.IReferenceable

        """
        results = defaultdict(list)
        context = aq_inner(self.context)
        portal_catalog = api.portal.get_tool('portal_catalog')

        if HAS_DEXTERITY:
            relation_catalog = queryUtility(ICatalog)
            if relation_catalog:
                int_id = dump(context, relation_catalog, {})
                if int_id:
                    brels = relation_catalog.findRelations(dict(to_id=int_id))
                    for brel in brels:
                        if brel.isBroken():
                            results['broken'].append(brel)
                        elif brel.from_attribute == referencedRelationship:
                            results['backlinks'].append({
                                'item': brel.from_object,
                                'rel': brel.from_attribute
                                })
                        else:
                            results['backrefs'].append({
                                'item': brel.from_object,
                                'rel': brel.from_attribute
                                })

                    rels = relation_catalog.findRelations(dict(from_id=int_id))
                    for rel in rels:
                        if rel.isBroken():
                            results['broken_refs'].append(rel)
                        elif rel.from_attribute == referencedRelationship:
                            results['links'].append({
                                'item': rel.to_object,
                                'rel': rel.from_attribute
                                })
                        else:
                            results['refs'].append({
                                'item': rel.to_object,
                                'rel': rel.from_attribute})

        if not HAS_ARCHETYPES:
            return results

        try:
            reference_catalog = api.portal.get_tool('reference_catalog')
            HAS_REFERENCE_CATALOG = True
        except api.exc.InvalidParameterError:
            HAS_REFERENCE_CATALOG = False

        # at and dx can be IReferenceable
        is_referenceable = False
        if HAS_REFERENCE_CATALOG and IReferenceable.providedBy(context) or \
                safe_hasattr(aq_base(context), 'isReferenceable'):
            is_referenceable = True
        elif HAS_REFERENCE_CATALOG:
            try:
                context = IReferenceable(context)
                is_referenceable = True
            except TypeError:
                is_referenceable = False

        if HAS_REFERENCE_CATALOG and is_referenceable:
            # references by reference-type
            for rel in reference_catalog.getRelationships(context):
                refs = reference_catalog.getReferences(
                    context,
                    relationship=rel,
                    objects=True)
                for ref in refs:
                    brains = portal_catalog(UID=ref.targetUID)
                    if brains:
                        if rel == referencedRelationship:
                            results['links'].append({
                                'item': brains[0],
                                'rel': 'link'})
                        else:
                            results['refs'].append({
                                'item': brains[0],
                                'rel': rel})

            # backreferences by backreference-type
            for brel in reference_catalog.getBackRelationships(context):
                brefs = reference_catalog.getBackReferences(
                    context,
                    relationship=brel,
                    objects=True)
                for bref in brefs:
                    brains = portal_catalog(UID=bref.sourceUID)
                    if brains:
                        if brel == referencedRelationship:
                            results['backlinks'].append({
                                'item': brains[0],
                                'rel': 'link'})
                        else:
                            results['backrefs'].append({
                                'item': brains[0],
                                'rel': brel})

        return results
