# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import copy


class LBCOffer(object):

    _tag_synonyms = {
        'listitem_date': 'date',
        'aditem_location': 'placement',
        'aditem_category': 'category'
    }

    url_domain = 'https://www.leboncoin.fr'

    def __init__(self, title=None, date=None, image=None, placement=None, category=None, price=None, url=None):
        self.title = title
        self.date = date
        self.image = image
        self.placement = placement
        self.category = category
        self.price = price
        self.url = url

    def html(self):
        s = "<a href='%s'><img src='%s' width='120px'>%s</a>" % (self.url, self.image, self.title)
        s += u" à %s" % self.placement
        s += " : %s EUR" % self.price
        return s

    def is_complete(self):
        res = self.title and self.placement and self.price and self.url
        return res

    def __str__(self):
        return u'<Offer %s>' % self.__dict__
    __repr__ = __str__

    def __hash__(self):
        return hash(str(self))

    def __setitem__(self, key, value):
        newkey = self._tag_synonyms.get(key, key)
        if key == 'url' and not value.startswith(self.url_domain):
            value = self.url_domain + value
        setattr(self, newkey, value)

    def __getitem__(self, key):
        getattr(self, key)


class LBCParser(HTMLParser):

    def error(self, message):
        print('parsing error', message)

    def __init__(self):
        HTMLParser.__init__(self)
        self.offers = []
        self._reset_offer()
        self._reset_temp_vars()

    def _reset_temp_vars(self, tag=None, attrs=[]):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        self.current_data = ''

    def _reset_offer(self):
        self._in_offer = False
        self.current_offer = LBCOffer()
        self.li_level = 0

    def handle_starttag(self, tag, attrs):

        self._reset_temp_vars(tag, attrs)

        if tag == 'li':
            self.li_level += 1
            if self.current_attrs.get('itemtype', '') == 'http://schema.org/Offer':
                self._in_offer = True
                self.li_level = 1

        if self._in_offer:
            if tag == 'a' and 'href' in self.current_attrs and 'title' in self.current_attrs:
                self.current_offer['url'] = self.current_attrs['href']
                self.current_offer['title'] = self.current_attrs['title']
        if tag == 'img':
            src = self.current_attrs.get('content', 'not set')
            self.current_offer["image"] = src

    def _txt(self):
        s = self.current_data.strip()
        while '  ' in s:
            s = s.replace('  ', ' ')
            s = s.replace('\t', ' ')
            s = s.replace('\n', '')
        return s

    def handle_endtag(self, tag):

        if tag == 'li':
            self.li_level -= 1

        if not self._in_offer:
            return

        if tag == 'li':
            if self._in_offer and self.li_level == 0:
                self.offers.append(copy.deepcopy(self.current_offer))
                self._reset_offer()

        if tag == 'p':
            for attr_key, attr_value in (
                    ('data-qa-id', 'listitem_date'),
                    ('data-qa-id', 'aditem_location'),
                    ('data-qa-id', 'aditem_category')
            ):
                if self.current_attrs.get(attr_key, '') == attr_value:
                    k = self.current_attrs[attr_key]
                    v = self._txt()
                    self.current_offer[k] = v
        elif tag == 'span' and self.current_attrs.get('itemprop', '') == 'priceCurrency':
            v = self._txt()
            self.current_offer['price'] = v

    def handle_data(self, data):
        self.current_data += data


def parse(s):
    parser = LBCParser()
    parser.feed(s)
    return parser.offers
