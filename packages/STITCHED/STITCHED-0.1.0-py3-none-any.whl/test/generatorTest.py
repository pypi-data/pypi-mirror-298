import unittest
from tool.config.generator import Config
import pandas as pd

class GeneratorTestCase(unittest.TestCase):
    def test_create_configGenerator(self):
        self.config = Config('config_generatorTest.csv', mode='create')
        self.config.add_entry(
            dataset_file_name='olid-training-v1.0.tsv',
            dataset_name='OLID19',
            label_name_definition={'subtask_a': '', 'subtask_b':'', 'subtask_c':''},
            source='@Twitter',
            language='@eng',
            text='tweet'
        )
        self.assertEqual(len(pd.read_csv('config_generatorTest.csv')), 1)

        ## Under mode='create', only one row can be initialized
        self.config.add_entry(
            dataset_file_name='olid-training-v1.0.tsv',
            dataset_name='OLID19',
            label_name_definition={'subtask_a': '', 'subtask_b':'', 'subtask_c':''},
            source='@Twitter',
            language='@eng',
            text='tweet'
        )
        self.assertEqual(len(pd.read_csv('config_generatorTest.csv')), 1)

    def test_append_new_dataset(self):
        self.config = Config('config_generatorTest.csv', mode='append')
        ## Under mode='create', only one row can be initialized
        self.config.add_entry(
            dataset_file_name='SBFv2.dev.csv, SBFv2.trn.csv, SBFv2.tst.csv',
            dataset_name='SBFv2',
            label_name_definition={"intentYN":"", "sexYN":"", "sexReason":"", "offensiveYN":""},
            source='@Twitter',
            language='@eng',
            text='post'
        )

        self.assertEqual(len(pd.read_csv('config_generatorTest.csv')), 2)


if __name__ == '__main__':
    unittest.main()
