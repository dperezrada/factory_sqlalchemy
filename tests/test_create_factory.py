# -*- coding: utf-8 -*-
import unittest

from factory_sqlachemy import BaseFactory
from .configs import Actor, Comment, Entry, create_db, db_config, drop_db


class TestCreateFactory(unittest.TestCase):

    def setUp(self):
        self.engine, self.dbsession = create_db()

    def tearDown(self):
        drop_db(self.engine)

    class ActorFactory(BaseFactory):
        FACTORY_FOR = Actor
        name = 'Juan'

    def test_create_that_should_store_in_database(self):
        actor = self.ActorFactory.create(_db=db_config)
        actor_from_db = self.dbsession.query(Actor).first()
        self.assertEqual(actor.name, actor_from_db.name)


class TestAutomaticRelations(unittest.TestCase):

    def setUp(self):
        super(TestAutomaticRelations, self).setUp()
        self.engine, self.dbsession = create_db()

    def tearDown(self):
        drop_db(self.engine)
        super(TestAutomaticRelations, self).tearDown()

    class CommentFactory(BaseFactory):
        FACTORY_FOR = Comment

    def test_create_entry_from_comment_created(self):
        comment = self.CommentFactory.create(_db=db_config)
        self.assertIsNotNone(comment.id)
        self.assertIsInstance(comment.content, unicode)
        self.assertEqual(1, len(self.dbsession.query(Comment).all()))
        entries = self.dbsession.query(Entry).all()
        self.assertEqual(1, len(entries))
        self.assertEqual(comment.entry_id, entries[0].id)
