=====
Usage
=====

.. _installation:

Installation
==============

Install and update using pip:

.. code-block:: console

   (.venv) $ pip install -U python-plugins

email
======

.. code-block:: python
   
   # smtp's host
   host = "smtp.host"
   port = "465"
   # smtp's username and password
   user = "test@test.com"
   password = "your password"

   # receiver and subject and content
   to = "test2@test.com"
   data = {
      "to": to,
      "subject": "subject of msg",
      "content": "content of msg",
   }

   s = SmtpSSL(host, port, user, password)
   r = s.send_emsg(data)

mixins
======

.. code-block:: python

   from flask_sqlalchemy import SQLAlchemy
   from python_plugins.models.mixins import PrimaryKeyMixin
   from python_plugins.models.mixins import UserMixin
   from python_plugins.models.mixins import DataMixin
   from python_plugins.models.mixins import TimestampMixin

   db = SQLAlchemy()

   class User(PrimaryKeyMixin, DataMixin, TimestampMixin, UserMixin, db.models):
      __tablename__ = "users"

remove_pycache
=======================

.. code-block:: python

    from  python_plugins.utils.remove_pycache import remove_pycache

    remove_pycache(".")


weixin.wechat
==================

.. code-block:: python

   from python_plugins.weixin.wechat import Wechat

   class MyWechat(Wechat):
      def get_app(self) -> dict:
         # may depended on self.name from self.__init__(name)
         return "<your app>"

   mywechat = MyWechat("name")
   mywechat.verify(query)
   mywechat.chat(query,content)
   