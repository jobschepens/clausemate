"""Tests for benchmark.py."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.benchmark import BenchmarkResult, PerformanceBenchmark, run_benchmarks


class TestBenchmarkResult:
    """Test the BenchmarkResult dataclass."""

    def test_benchmark_result_creation(self):
        """Test creating a BenchmarkResult instance."""
        result = BenchmarkResult(
            execution_time=10.5,
            memory_peak_mb=150.2,
            memory_final_mb=120.8,
            cpu_percent=45.3,
            output_rows=1000,
            input_size_mb=5.2,
            throughput_rows_per_sec=95.2,
        )

        assert result.execution_time == 10.5
        assert result.memory_peak_mb == 150.2
        assert result.memory_final_mb == 120.8
        assert result.cpu_percent == 45.3
        assert result.output_rows == 1000
        assert result.input_size_mb == 5.2
        assert result.throughput_rows_per_sec == 95.2


class TestPerformanceBenchmark:
    """Test the PerformanceBenchmark class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.benchmark = PerformanceBenchmark()

    @patch("src.benchmark.psutil")
    def test_initialization_success(self, mock_psutil):
        """Test successful initialization."""
        mock_process = MagicMock()
        mock_psutil.Process.return_value = mock_process

        benchmark = PerformanceBenchmark()

        assert benchmark.process == mock_process
        mock_psutil.Process.assert_called_once()

    @patch("src.benchmark.psutil", None)
    def test_initialization_without_psutil(self):
        """Test initialization failure without psutil."""
        with pytest.raises(ImportError, match="psutil is required for benchmarking"):
            PerformanceBenchmark()

    @patch("src.benchmark.time")
    @patch("src.benchmark.pd")
    def test_benchmark_function(self, mock_pd, mock_time):
        """Test benchmarking a function."""
        # Mock time measurements
        mock_time.time.side_effect = [100.0, 110.5]  # start and end times

        # Mock process memory info
        mock_memory_info = MagicMock()
        mock_memory_info.rss = 100 * 1024 * 1024  # 100 MB
        self.benchmark.process.memory_info = MagicMock(return_value=mock_memory_info)

        # Mock CPU percent
        self.benchmark.process.cpu_percent = MagicMock(return_value=45.5)

        # Mock input file
        mock_input_file = MagicMock()
        mock_input_file.stat.return_value.st_size = 5 * 1024 * 1024  # 5 MB

        # Mock output file and DataFrame
        mock_output_file = MagicMock()
        mock_output_file.exists.return_value = True

        mock_df = MagicMock()
        mock_df.__len__ = MagicMock(return_value=1000)
        mock_pd.read_csv.return_value = mock_df

        # Mock function to benchmark
        def test_function(arg1, arg2, kwarg1=None):
            return "result"

        # Execute benchmark
        result = self.benchmark.benchmark_function(
            test_function,
            mock_input_file,
            mock_output_file,
            "arg1",
            "arg2",
            kwarg1="value",
        )

        # Verify result
        assert isinstance(result, BenchmarkResult)
        assert result.execution_time == 10.5
        assert result.memory_peak_mb == 100.0
        assert result.memory_final_mb == 100.0
        assert result.cpu_percent == 45.5
        assert result.output_rows == 1000
        assert result.input_size_mb == 5.0
        assert result.throughput_rows_per_sec == 95.23809523809524

    @patch("src.benchmark.time")
    def test_benchmark_function_no_output_file(self, mock_time):
        """Test benchmarking when output file doesn't exist."""
        # Mock time measurements
        mock_time.time.side_effect = [100.0, 105.0]

        # Mock process memory info
        mock_memory_info = MagicMock()
        mock_memory_info.rss = 50 * 1024 * 1024  # 50 MB
        self.benchmark.process.memory_info = MagicMock(return_value=mock_memory_info)
        self.benchmark.process.cpu_percent = MagicMock(return_value=30.0)

        # Mock input file
        mock_input_file = MagicMock()
        mock_input_file.stat.return_value.st_size = 2 * 1024 * 1024  # 2 MB

        # Mock output file (doesn't exist)
        mock_output_file = MagicMock()
        mock_output_file.exists.return_value = False

        def test_function():
            pass

        result = self.benchmark.benchmark_function(
            test_function, mock_input_file, mock_output_file
        )

        assert result.output_rows == 0
        assert result.throughput_rows_per_sec == 0

    @patch("src.benchmark.time")
    def test_benchmark_function_zero_execution_time(self, mock_time):
        """Test benchmarking with zero execution time."""
        # Mock time measurements (same time)
        mock_time.time.return_value = 100.0

        # Mock process memory info
        mock_memory_info = MagicMock()
        mock_memory_info.rss = 75 * 1024 * 1024  # 75 MB
        self.benchmark.process.memory_info = MagicMock(return_value=mock_memory_info)
        self.benchmark.process.cpu_percent = MagicMock(return_value=25.0)

        # Mock files
        mock_input_file = MagicMock()
        mock_input_file.stat.return_value.st_size = 1 * 1024 * 1024  # 1 MB

        mock_output_file = MagicMock()
        mock_output_file.exists.return_value = True

        with patch("src.benchmark.pd") as mock_pd:
            mock_df = MagicMock()
            mock_df.__len__ = MagicMock(return_value=500)
            mock_pd.read_csv.return_value = mock_df

            def test_function():
                pass

            result = self.benchmark.benchmark_function(
                test_function, mock_input_file, mock_output_file
            )

            assert result.throughput_rows_per_sec == 0  # Division by zero handled

    @patch("archive.phase1.clause_mates_complete.main")
    @patch("src.main.main")
    def test_compare_phases(self, mock_phase2_main, mock_phase1_main):
        """Test comparing performance of both phases."""
        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create input file
            input_file = temp_path / "2.tsv"
            input_file.touch()

            # Mock the main functions to do nothing
            mock_phase1_main.return_value = None
            mock_phase2_main.return_value = None

            results = self.benchmark.compare_phases()

            # Should have results for both phases
            assert "phase1" in results
            assert "phase2" in results
            assert isinstance(results["phase1"], BenchmarkResult)
            assert isinstance(results["phase2"], BenchmarkResult)

    def test_compare_phases_missing_files(self):
        """Test comparing phases when input files don't exist."""
        with patch("src.benchmark.Path") as mock_path:
            # Mock Path to return non-existent files
            mock_input_file = MagicMock()
            mock_input_file.exists.return_value = False
            mock_path.return_value = mock_input_file

            results = self.benchmark.compare_phases()

            # Should return empty results
            assert results == {}

    def test_save_benchmark_results(self):
        """Test saving benchmark results to file."""
        # Create test results
        results = {
            "phase1": BenchmarkResult(
                execution_time=15.2,
                memory_peak_mb=200.5,
                memory_final_mb=180.3,
                cpu_percent=55.2,
                output_rows=1500,
                input_size_mb=8.1,
                throughput_rows_per_sec=98.7,
            ),
            "phase2": BenchmarkResult(
                execution_time=12.8,
                memory_peak_mb=175.2,
                memory_final_mb=160.8,
                cpu_percent=48.9,
                output_rows=1500,
                input_size_mb=8.1,
                throughput_rows_per_sec=117.2,
            ),
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = Path(f.name)

        try:
            self.benchmark.save_benchmark_results(results, output_file)

            # Verify file was created and contains expected data
            assert output_file.exists()

            with open(output_file) as f:
                data = json.load(f)

            assert "timestamp" in data
            assert "system_info" in data
            assert "results" in data
            assert "phase1" in data["results"]
            assert "phase2" in data["results"]

            # Verify phase1 data
            phase1_data = data["results"]["phase1"]
            assert phase1_data["execution_time"] == 15.2
            assert phase1_data["memory_peak_mb"] == 200.5
            assert phase1_data["output_rows"] == 1500

            # Verify phase2 data
            phase2_data = data["results"]["phase2"]
            assert phase2_data["execution_time"] == 12.8
            assert phase2_data["memory_peak_mb"] == 175.2
            assert phase2_data["output_rows"] == 1500

        finally:
            output_file.unlink()

    @patch("src.benchmark.PerformanceBenchmark")
    @patch("src.benchmark.Path")
    def test_run_benchmarks(self, mock_path_class, mock_benchmark_class):
        """Test the run_benchmarks function."""
        # Mock benchmark instance
        mock_benchmark = MagicMock()
        mock_benchmark_class.return_value = mock_benchmark

        # Mock results
        mock_results = {"phase1": MagicMock(), "phase2": MagicMock()}
        mock_benchmark.compare_phases.return_value = mock_results

        # Mock output file
        mock_output_file = MagicMock()
        mock_path_class.return_value = mock_output_file

        # Mock print to capture output
        with patch("builtins.print") as mock_print:
            run_benchmarks()

            # Verify benchmark was created and methods called
            mock_benchmark_class.assert_called_once()
            mock_benchmark.compare_phases.assert_called_once()
            mock_benchmark.save_benchmark_results.assert_called_once_with(
                mock_results, mock_output_file
            )

            # Verify print was called (checking that results are displayed)
            assert mock_print.called

    @patch("src.benchmark.psutil")
    def test_system_info_collection(self, mock_psutil):
        """Test system information collection in save_benchmark_results."""
        # Mock psutil functions
        mock_psutil.cpu_count.return_value = 8
        mock_psutil.virtual_memory.return_value.total = 16 * 1024 * 1024 * 1024  # 16 GB

        with patch("src.benchmark.platform") as mock_platform:
            mock_platform.platform.return_value = "Windows-10"

            results = {}
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as f:
                output_file = Path(f.name)

            try:
                self.benchmark.save_benchmark_results(results, output_file)

                with open(output_file) as f:
                    data = json.load(f)

                system_info = data["system_info"]
                assert system_info["cpu_count"] == 8
                assert system_info["memory_total_mb"] == 16384.0  # 16 GB in MB
                assert system_info["platform"] == "Windows-10"

            finally:
                output_file.unlink()

    @patch("src.benchmark.psutil", None)
    def test_system_info_collection_without_psutil(self):
        """Test system information collection when psutil is not available."""
        results = {}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = Path(f.name)

        try:
            self.benchmark.save_benchmark_results(results, output_file)

            with open(output_file) as f:
                data = json.load(f)

            system_info = data["system_info"]
            assert system_info["cpu_count"] == "unknown"
            assert system_info["memory_total_mb"] == "unknown"

        finally:
            output_file.unlink()
