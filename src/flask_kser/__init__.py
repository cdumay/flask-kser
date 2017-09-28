#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""


def rename_keys(data):
    result = dict()
    for key, value in data.items():
        if isinstance(value, dict):
            result[key.lower()] = rename_keys(value)
        else:
            result[key.lower()] = value
    return result


class FlaskKser(object):
    _kclient = None

    def __init__(self, kclient_class, app=None, config=None):
        self.app = None
        self.config = dict()
        self.kclient_class = kclient_class
        if app:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        if config:
            self.config = rename_keys(config)
        else:
            if "KSER_CONFIG" not in app.config:
                raise RuntimeError("KSER_CONFIG not found in app.config !")
            self.config = rename_keys(app.config['KSER_CONFIG'])

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
            self._kclient = self.kclient_class(self.config)
        return self._kclient


class FlaskKserConsumer(FlaskKser):
    def __init__(self, kclient_class, app=None, config=None, topics=None):
        FlaskKser.__init__(self, kclient_class, app=app, config=config)
        self.topics = topics or list()

    @property
    def kclient(self):
        """ Kafka client

        :return: Kafka consumer
        :rtype: kser.consumer.Consumer
        """
        if self._kclient is None:
            self._kclient = self.kclient_class(self.config, self.topics)
        return self._kclient
