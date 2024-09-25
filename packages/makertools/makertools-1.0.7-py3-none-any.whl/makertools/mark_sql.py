#! /usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from timeit import default_timer
from loguru import logger
import settings


class UsingMysql(object):

    def __init__(self, commit=True, log_time=False, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):
        if self._log_time is True:
            self._start = default_timer()
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        if self._commit:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()

        if self._log_time is True:
            diff = default_timer() - self._start
            logger.info('-- %s: %.6f 秒' % (self._log_label, diff))

    @property
    def cursor(self):
        return self._cursor

    def get_connection(self):
        conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DBNAME,user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD)
        return conn

