"""
Test Phase 2 fixes for code review issues.

Tests for:
1. Duplicate total_cost property removal
2. Cost double-counting fix in _record_cost
3. Proper error propagation in _llm_query_wrapper
4. Budget boundary consistency
"""

import unittest
from unittest.mock import Mock
from pathlib import Path
import tempfile
import shutil


try:
    import sys
    from pathlib import Path
    # Add brain/scripts to path for imports
    script_dir = Path(__file__).parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    
    from repl_environment import REPLSession, CostBudgetExceededError
    from llm_client import LLMClient, LLMResponse, LLMBudgetExceededError
except ImportError as e:
    REPLSession = None
    CostBudgetExceededError = None
    LLMClient = None
    LLMResponse = None
    LLMBudgetExceededError = None


@unittest.skipIf(REPLSession is None, "REPL Environment not yet implemented")
class TestDuplicatePropertyFix(unittest.TestCase):
    """Test that duplicate total_cost property is removed."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_store = Mock()
        self.mock_store.base_path = Path(self.temp_dir)
        self.mock_llm = Mock()
        
        self.repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_total_cost_property_exists(self):
        """total_cost property should be accessible."""
        cost = self.repl.total_cost
        self.assertIsInstance(cost, float)
        self.assertEqual(cost, 0.0)
    
    def test_get_cost_method_exists(self):
        """get_cost() method should be accessible."""
        cost = self.repl.get_cost()
        self.assertIsInstance(cost, float)
        self.assertEqual(cost, 0.0)
    
    def test_both_return_same_value(self):
        """Property and method should return the same value."""
        self.assertEqual(self.repl.total_cost, self.repl.get_cost())


@unittest.skipIf(REPLSession is None, "REPL Environment not yet implemented")
class TestCostDoubleCountingFix(unittest.TestCase):
    """Test that _record_cost doesn't double-count costs."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_store = Mock()
        self.mock_store.base_path = Path(self.temp_dir)
        
        # Create mock response with cost_usd
        self.mock_response = Mock()
        self.mock_response.text = 'test response'
        self.mock_response.cost_usd = 0.005
        
        # Mock LLM client that tracks cumulative cost
        self.mock_llm = Mock()
        self.mock_llm.complete = Mock(return_value=self.mock_response)
        self.mock_llm.get_cost = Mock(return_value=0.005)
        
        self.repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_single_query_cost(self):
        """Single query should record cost from response, not LLM client."""
        self.repl.execute('llm_query("Test")')
        
        # Should be 0.005, not 0.010 from double-counting
        self.assertEqual(self.repl.total_cost, 0.005)
    
    def test_multiple_queries_cost(self):
        """Multiple queries should accumulate correctly without double-counting."""
        # First query
        self.repl.execute('llm_query("Test 1")')
        self.assertEqual(self.repl.total_cost, 0.005)
        
        # Second query - LLM client cumulative is 0.010, but REPL should only add 0.005
        self.mock_llm.get_cost = Mock(return_value=0.010)
        self.repl.execute('llm_query("Test 2")')
        
        # Should be 0.010, not 0.015 or 0.020 from double-counting
        self.assertAlmostEqual(self.repl.total_cost, 0.010, places=6)
    
    def test_cost_from_response_only(self):
        """_record_cost should use response.cost_usd, not llm_client.get_cost()."""
        # Even if LLM client reports different cumulative cost
        self.mock_llm.get_cost = Mock(return_value=999.0)
        
        self.repl.execute('llm_query("Test")')
        
        # Should use response.cost_usd (0.005), not llm_client.get_cost() (999.0)
        self.assertEqual(self.repl.total_cost, 0.005)


@unittest.skipIf(REPLSession is None, "REPL Environment not yet implemented")
class TestErrorPropagation(unittest.TestCase):
    """Test that errors are properly raised, not swallowed."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_store = Mock()
        self.mock_store.base_path = Path(self.temp_dir)
        
        self.mock_llm = Mock()
        
        self.repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_llm_error_propagates_through_execute(self):
        """LLM errors should be caught by execute() and returned as error string."""
        self.mock_llm.complete = Mock(side_effect=Exception("API Error"))
        
        result = self.repl.execute('llm_query("Test")')
        
        # execute() catches and returns as error string
        self.assertIn("error", str(result).lower())
        self.assertIn("API Error", str(result))
    
    def test_budget_error_propagates(self):
        """Budget errors should propagate without being swallowed."""
        # Set a tight budget
        repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm,
            max_cost_usd=0.001
        )
        
        # Mock response that exceeds budget
        mock_response = Mock()
        mock_response.text = 'test'
        mock_response.cost_usd = 0.002
        self.mock_llm.complete = Mock(return_value=mock_response)
        
        # Should raise budget error (caught by execute and returned as error string)
        result = repl.execute('llm_query("Expensive")')
        self.assertIn("budget", str(result).lower())


@unittest.skipIf(REPLSession is None, "REPL Environment not yet implemented")
class TestBudgetBoundaryConsistency(unittest.TestCase):
    """Test budget boundary handling is consistent."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_store = Mock()
        self.mock_store.base_path = Path(self.temp_dir)
        
        # Mock response
        self.mock_response = Mock()
        self.mock_response.text = 'test response'
        self.mock_response.cost_usd = 0.005
        
        self.mock_llm = Mock()
        self.mock_llm.complete = Mock(return_value=self.mock_response)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_exact_budget_allowed(self):
        """Query that exactly meets budget should succeed."""
        repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm,
            max_cost_usd=0.005
        )
        
        # Query costs exactly 0.005
        result = repl.execute('llm_query("Test")')
        
        # Should succeed
        self.assertNotIn("budget", str(result).lower())
        self.assertEqual(repl.total_cost, 0.005)
    
    def test_over_budget_blocked(self):
        """Query that exceeds budget should be blocked."""
        repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm,
            max_cost_usd=0.004
        )
        
        # Query costs 0.005, which exceeds 0.004 budget
        result = repl.execute('llm_query("Test")')
        
        # Should fail with budget error
        self.assertIn("budget", str(result).lower())
    
    def test_pre_check_prevents_execution(self):
        """_ensure_budget should be called before LLM query."""
        repl = REPLSession(
            chunk_store=self.mock_store,
            llm_client=self.mock_llm,
            max_cost_usd=0.010
        )
        
        # First query succeeds
        repl.execute('llm_query("Test 1")')
        self.assertEqual(repl.total_cost, 0.005)
        
        # Second query would bring us to exactly 0.010 (budget limit)
        result = repl.execute('llm_query("Test 2")')
        
        # Should succeed because we allow equal
        self.assertNotIn("budget", str(result).lower())
        self.assertAlmostEqual(repl.total_cost, 0.010, places=6)


@unittest.skipIf(LLMClient is None, "LLM Client not yet implemented")
class TestLLMClientBudgetConsistency(unittest.TestCase):
    """Test LLMClient budget handling matches REPLSession."""
    
    def test_exact_budget_allowed(self):
        """LLMClient should allow queries that exactly meet budget."""
        # Use custom rates so mock provider accumulates cost
        custom_rates = {
            "mock": {"input": 1.0, "output": 1.0}
        }
        client = LLMClient(
            provider="mock",
            max_cost_usd=0.005,
            mock_sequence=["test response"],
            rate_table=custom_rates
        )
        
        # Query should succeed even though it uses entire budget
        response = client.complete("test prompt")
        self.assertIsNotNone(response)
    
    def test_over_budget_blocked(self):
        """LLMClient should block queries that would exceed budget."""
        # Use custom rates so mock provider accumulates cost
        custom_rates = {
            "mock": {"input": 1.0, "output": 1.0}
        }
        client = LLMClient(
            provider="mock",
            max_cost_usd=0.006,  # Budget allows first query but not second
            mock_sequence=["response 1", "response 2"],
            rate_table=custom_rates
        )
        
        # First query uses some budget (should be ~0.005)
        response1 = client.complete("test prompt 1")
        self.assertIsNotNone(response1)
        self.assertGreater(client.get_cost(), 0.0)
        
        # Second query would exceed budget
        with self.assertRaises(LLMBudgetExceededError):
            client.complete("test prompt 2")


if __name__ == '__main__':
    unittest.main()
