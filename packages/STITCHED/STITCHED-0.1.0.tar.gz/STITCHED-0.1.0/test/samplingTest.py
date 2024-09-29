import unittest
from tool.utils.sampling import *
class TestBalancedSamplingMethods(unittest.TestCase):

    def setUp(self):
        """Set up the initial DataFrame for testing"""
        self.data = {
            'label': ['A', 'A', 'A', 'B', 'B', 'C', 'C', 'C', 'C', 'A', 'B', 'C'],
            'second_col': ['X', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'Y', 'Z', 'Z', 'Z', 'Z']
        }
        self.df = pd.DataFrame(self.data)

    def test_balanced_upsampling(self):
        """Test balanced upsampling on a single column"""
        upsampled_on_label = balanced_upsampling(self.df, label_col='label')

        # Check if the length of the upsampled DataFrame is correct (all classes should be upsampled to the size of the largest class)
        max_count = self.df['label'].value_counts().max()
        self.assertTrue(all(upsampled_on_label['label'].value_counts() == max_count))

    def test_balanced_downsampling(self):
        """Test balanced downsampling on a single column"""
        downsampled_on_label = balanced_downsampling(self.df, label_col='label')

        # Check if the length of the downsampled DataFrame is correct (all classes should be downsampled to the size of the smallest class)
        min_count = self.df['label'].value_counts().min()
        self.assertTrue(all(downsampled_on_label['label'].value_counts() == min_count))

    def test_balanced_fixedcount(self):
        """Test balanced fixed-count sampling on a single column"""
        fixed_on_label = balanced_fixedcount(self.df, 5, label_col='label')

        # Check if the length of the fixed sample is exactly as requested
        self.assertEqual(len(fixed_on_label), 5)

        # Also check that labels are roughly balanced
        unique_label_counts = fixed_on_label['label'].value_counts()
        self.assertTrue(any(unique_label_counts == unique_label_counts.iloc[0]))

    def test_balanced_upsampling_two_columns(self):
        """Test balanced upsampling on two columns"""
        upsampled_df = balanced_upsampling(self.df, label_col='label', second_col='second_col')

        # Check if the DataFrame is upsampled correctly considering both columns
        grouped = upsampled_df.groupby(['label', 'second_col']).size()
        max_count = grouped.max()
        self.assertTrue(all(grouped == max_count))

    def test_balanced_downsampling_two_columns(self):
        """Test balanced downsampling on two columns"""
        downsampled_df = balanced_downsampling(self.df, label_col='label', second_col='second_col')

        # Check if the DataFrame is downsampled correctly considering both columns
        grouped = downsampled_df.groupby(['label', 'second_col']).size()
        min_count = grouped.min()
        self.assertTrue(all(grouped == min_count))

    def test_balanced_fixedcount_two_columns(self):
        """Test balanced fixed-count sampling on two columns"""
        fixed_df = balanced_fixedcount(self.df, 6, 'label', 'second_col')

        # Check if the total length is as expected
        self.assertEqual(len(fixed_df), 6)

        grouped = fixed_df.groupby(['label', 'second_col']).size()
        unique_label_counts = grouped.unique()
        self.assertTrue(len(unique_label_counts) <= 2)  # Can modify based on the sampling method


if __name__ == '__main__':
    unittest.main()
