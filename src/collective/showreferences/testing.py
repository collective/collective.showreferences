# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.showreferences


class CollectiveShowreferencesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.showreferences)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.showreferences:default')


COLLECTIVE_SHOWREFERENCES_FIXTURE = CollectiveShowreferencesLayer()


COLLECTIVE_SHOWREFERENCES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SHOWREFERENCES_FIXTURE,),
    name='CollectiveShowreferencesLayer:IntegrationTesting'
)


COLLECTIVE_SHOWREFERENCES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SHOWREFERENCES_FIXTURE,),
    name='CollectiveShowreferencesLayer:FunctionalTesting'
)


COLLECTIVE_SHOWREFERENCES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SHOWREFERENCES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveShowreferencesLayer:AcceptanceTesting'
)
