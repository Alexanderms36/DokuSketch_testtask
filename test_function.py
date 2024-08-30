import unittest
from unittest.mock import patch
import pandas as pd
from function import draw_plots, generate_statistics, draw_anomalies


class TestDrawPlots(unittest.TestCase):

    @patch("pandas.read_json")
    @patch("os.makedirs")
    @patch("function.save_plot")

    def test_draw_plots(self, mock_save_plot, mock_makedirs, mock_read_json):
        mock_read_json.return_value = pd.DataFrame({
            'name': ['Room1', 'Room2'],
            'floor_mean': [6, 12],
            'ceiling_mean': [7, 12],
            'gt_corners': [4, 7],
            'rb_corners': [3, 7],
            'floor_max': [16, 20],
            'ceiling_max': [16, 22],
            'floor_min': [3, 6],
            'ceiling_min': [2, 5],
            'mean': [7, 12],
            'max': [18, 20],
            'min': [1, 1]
        })

        result = draw_plots('test_path.json')

        self.assertTrue(len(result) > 0)
        self.assertTrue(mock_save_plot.called)
        self.assertTrue(mock_makedirs.called)

    @patch("function.save_plot")
    def test_generate_statistics(self, mock_save_plot):
        df = pd.DataFrame({
            'name': ['Room1', 'Room2'],
            'floor_mean': [6, 12],
            'ceiling_mean': [7, 12],
            'gt_corners': [4, 7],
            'rb_corners': [3, 7],
            'floor_max': [16, 20],
            'ceiling_max': [16, 22],
            'floor_min': [3, 6],
            'ceiling_min': [2, 5],
            'mean': [7, 12],
            'max': [18, 20],
            'min': [1, 1]
        })
        result = generate_statistics(df)

        self.assertTrue(mock_save_plot.called)

    @patch("function.save_plot")
    def test_draw_anomalies(self, mock_save_plot):
        df = pd.DataFrame({
            'name': ['Room1', 'Room2'],
            'floor_mean': [6, 12],
            'ceiling_mean': [7, 12],
            'gt_corners': [4, 7],
            'rb_corners': [3, 7],
            'floor_max': [16, 20],
            'ceiling_max': [16, 22],
            'floor_min': [3, 6],
            'ceiling_min': [2, 5],
            'mean': [7, 12],
            'max': [18, 20],
            'min': [1, 1]
        })

        anomaly_threshold = 10
        result = draw_anomalies(df, anomaly_threshold)

        self.assertTrue(mock_save_plot.called)

if __name__ == "__main__":
    unittest.main()
