"""
Fastspring API wrapper

Partly based on https://github.com/projectfusion/fastspring/blob/master/fastspring.py
"""

import logging

import base64
import datetime
import urllib2

from xml.etree import ElementTree

logger = logging.getLogger('fastspring-api')

TEST_MODE = True
STORE_ID = ''
USERNAME = ''
PASSWORD = ''


class XMLResponse(object):
    """A really simple object for querying XML data returned from 
    fastspring requests.

    """
    def __init__(self, xml):
        self.xml = ElementTree.XML(xml)

    def __getitem__(self, key):
        attr = self.xml.find(key)
        return attr.text if attr is not None else None

    def __str__(self):
        return self.xml.tag

    @property
    def is_test(self):
        return self['test'] == 'true'


class Subscription(XMLResponse):
    """A response from the get_subscription call.

    """
    def __init__(self, xml):
        super(Subscription, self).__init__(xml)

    @property
    def is_active(self):
        return self['status'] == 'active'

    @property
    def status(self):
        return self['status']

    @property
    def statusChanged(self):
        # TODO: parse to datetime
        return datetime.datetime.strptime(self['statusChanged'], "%Y-%m-%dT%H:%M:%S.%fZ")

    @property
    def statusReason(self):
        return self['statusReason']

    @property
    def cancelable(self):
        return self['cancelable']

    @property
    def referrer(self):
        return self['referrer']

    @property
    def sourceName(self):
        return self['sourceName']

    @property
    def sourceKey(self):
        return self['sourceKey']

    @property
    def sourceCampaign(self):
        return self['sourceCampaign']

    @property
    def customer(self):
        return self['customer']

    @property
    def customerUrl(self):
        return self['customerUrl']

    @property
    def productName(self):
        return self['productName']

    @property
    def quantity(self):
        return self['quantity']

    @property
    def nextPeriodDate(self):
        return datetime.datetime.strptime(self['nextPeriodDate'], "%Y-%m-%dZ")

    @property
    def end(self):
        return self['end']


def addTestMode(url):
    if TEST_MODE:
        if url.find('?') > -1:
            url = url + "&mode=test"
        else:
            url = url + "?mode=test"

    return url


class FastspringNotFound(Exception):
    pass


class FastspringNotAuthorized(Exception):
    pass


class ResponseParseError(Exception):
    pass


def simpleCurl(url, data=None, method='GET'):
    """
    Data should be for urlopen

    From: http://stackoverflow.com/questions/2667509/curl-alternative-in-python

    >>> simpleCurl("https://api.fastspring.com/company/" + STORE_ID + "/subscription/123?mode=test")
    Traceback (most recent call last):
        ...
    FastspringNotFound
    """
    # manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # manager.add_password(None, url, USERNAME, PASSWORD)
    # handler = urllib2.HTTPBasicAuthHandler(manager)

    # director = urllib2.OpenerDirector()
    # director.add_handler(handler)
    # urllib2.install_openerp(director)

    req = urllib2.Request(url)
    req.add_header('Authorization', "Basic %s" % base64.standard_b64encode('%s:%s' % (USERNAME, PASSWORD)))
    req.add_header('Content-Type', "application/xml")
    req.get_method = lambda: method
    try:
        result = urllib2.urlopen(req, data)
    except urllib2.HTTPError, e:
        if e.code == 404:
            raise FastspringNotFound
        elif e.code == 401:
            raise FastspringNotAuthorized
        else:
            raise
    # result.read() will contain the data
    # result.info() will contain the HTTP headers

    # To get say the content-length header
    # length = result.info()['Content-Length']
    try:
        logger.debug("Url %s was fetched" % url)
        return Subscription(result.read()), result.getcode()
    except ElementTree.ParseError:
        raise ResponseParseError


def createSubscription(product_ref, customer_ref, redirect_fn):
    """
    >>> createSubscription('pear', 'mycustomer4', str)
    'http://sites.fastspring.com/vidzor/product/pear?referrer=mycustomer4&mode=test'
    """
    url = "http://sites.fastspring.com/%s/product/%s?referrer=%s" % (STORE_ID, product_ref, customer_ref)
    url = addTestMode(url)
    return redirect_fn(url)


def _getSubscriptionUrl(subscription_ref):
    url = "https://api.fastspring.com/company/" + STORE_ID + "/subscription/" + subscription_ref
    url = addTestMode(url)
    return url


def getSubscription(subscription_ref):
    """
    >>> print getSubscription("VID130423-6618-57114S")
    subscription
    """
    url = _getSubscriptionUrl(subscription_ref)
    url = addTestMode(url)

    return simpleCurl(url)[0]


def updateSubscription(subscription_ref, data):
    """
    Data should be a valid Subscription xml
    """
    url = _getSubscriptionUrl(subscription_ref)
    url = addTestMode(url)
    return simpleCurl(url, data)[0]


def cancelSubscription(subscription_ref):
    url = _getSubscriptionUrl(subscription_ref)
    url = addTestMode(url)
    return simpleCurl(url, None, 'DELETE')[0]


def renewSubscription(subscription_ref):
    """
    >>> renewSubscription('VID130423-6618-57114S')
    True
    """
    url = _getSubscriptionUrl(subscription_ref) + '/renew'
    url = addTestMode(url)
    response, status_code = simpleCurl(url, {})
    return status_code == 201


if __name__ == '__main__':
    import doctest
    from test_settings import STORE_ID, USERNAME, PASSWORD
    doctest.testmod()
