#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from kser.producer import Producer
from kser.consumer import Consumer


class FlaskKser(object):
    _kclient = None

    def __init__(self, app=None):
        self.app = None
        self.config = dict()
        if app:
            self.init_app(app)

    def init_app(self, app):
        if "KSER_CONFIG" not in app.config:
            raise RuntimeError("KSER_CONFIG not found in app.config !")

        for key, value in app.config['KSER_CONFIG'].items():
            self.config[key.lower().replace('_', '.')] = value

        self.app = app

    @property
    def kclient(self):
        """ Kafka client

        :return: Kafka producer or consumer
        :rtype: kser.producer.Producer or kser.consumer.Consumer
        """
        raise NotImplementedError("This method MUST be implemented")


class FlaskKserProducer(FlaskKser):
    @property
    def kclient(self):
        """ Kafka client

        :return: Kafka producer
        :rtype: kser.producer.Producer
        """
        if self._kclient is None:
            self._kclient = Producer(self.config)
        return self._kclient


class FlaskKserConsumer(FlaskKser):
    def __init__(self, app=None, topics=None):
        FlaskKser.__init__(self, app=app)
        self.topics = topics or list()

    @property
    def kclient(self):
        """ Kafka client

        :return: Kafka consumer
        :rtype: kser.consumer.Consumer
        """
        if self._kclient is None:
            self._kclient = Consumer(self.config, self.topics)
        return self._kclient
