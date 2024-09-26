from __future__ import annotations # Default behavior pending PEP 649

import unittest

import numpy as np

import pandas as pd

import simbench as sb # type: ignore

from gritscope.powergrid.grid import Grid

from .powerflow import compare_powerflows

# Power flow result tests versus Pandapower on various cases

class TestPowerFlowVersusSimbench(unittest.TestCase):
    """Test power flow results on various Simbench cases."""
    
    def setUp(self) -> None:
        """Set up test tolerances."""
        
        self.power_tolerance = 1e-2 # VA
        self.result_tolerances = pd.Series({'ang_diff': 1e-6, # Degrees
                                            'flow': 1e-6, # A
                                            'loading': 1e-6}) # Dimensionless
    
    def test_case_ehv(self) -> None:
        """Test power flow results versus Pandapower on Case 9."""
        
        net = sb.get_simbench_net('1-EHV-mixed--1-no_sw')
        
        shifts = np.random.default_rng(0).uniform(-5, 5, len(net.trafo))
        net.trafo['phase_shift'] = shifts
        
        with self.subTest("Pandapower to Gritscope"):
            grid = Grid.from_pp(net)
            result_diffs = compare_powerflows(grid, net, self.power_tolerance)
            self.assertTrue(all(result_diffs.max() < self.result_tolerances))
        
        with self.subTest("Gritscope back to Pandapower"):
            net = grid.to_pp()
            result_diffs = compare_powerflows(grid, net, self.power_tolerance)
            self.assertTrue(all(result_diffs.max() < self.result_tolerances))
