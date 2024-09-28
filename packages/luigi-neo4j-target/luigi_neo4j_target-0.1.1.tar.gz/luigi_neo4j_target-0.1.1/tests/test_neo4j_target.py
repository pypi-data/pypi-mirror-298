import unittest
from unittest.mock import patch, MagicMock
import neo4j
from luigi_neo4j_target import Neo4jTarget


class TestNeo4jTarget(unittest.TestCase):

    @patch('neo4j.GraphDatabase.driver')
    def setUp(self, mock_driver):
        self.mock_driver_instance = MagicMock()
        mock_driver.return_value = self.mock_driver_instance
        self.client = neo4j.GraphDatabase.driver('bolt://localhost:1234')

    def test_init_target_success(self):
        mock_session = MagicMock()
        self.mock_driver_instance.session.return_value = mock_session
        mock_tx = MagicMock()
        mock_session.begin_transaction.return_value = mock_tx
        mock_tx.run.return_value = None
        target = Neo4jTarget(self.client, 'foo')
        self.assertIsNotNone(target)

    def test_init_target_failed_sessions(self):
        self.mock_driver_instance.session.side_effect = neo4j.exceptions.ServiceUnavailable
        with self.assertRaises(neo4j.exceptions.ServiceUnavailable):
            target = Neo4jTarget(self.client, 'foo')


if __name__ == '__main__':
    unittest.main()
