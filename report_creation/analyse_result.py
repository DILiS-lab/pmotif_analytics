"""Generate analysis artifacts from raw analysis data."""
import argparse
import os
from pathlib import Path

import report_creation.local_analysis as local_analysis
from report_creation.global_analysis import analyse_relevance, get_random_graph_paths, plot_frequency_histogram


def run_local_analysis(analysis_out, original):
    """Produce artifacts for the local (un-randomized) scope."""
    original_frequency = local_analysis.get_frequency_data(original)
    local_analysis.graphlet_pie_chart(original_frequency, analysis_out)
    local_analysis.metric_distribution(original, analysis_out)
    local_analysis.outlier_detection(original, analysis_out)


def run_global_analysis(analysis_data: Path, global_out: Path, graphlet_size: int, original: Path):
    """Produce artifacts for the global (randomized) scope."""
    random_graphs = get_random_graph_paths(analysis_data)
    plot_frequency_histogram(global_out, original, random_graphs, graphlet_size)
    analyse_relevance(global_out, random_graphs, graphlet_size)


def main(analysis_out: Path, edgelist: Path, graphlet_size: int):
    """Create analysis artifacts and report."""
    analysis_data = analysis_out / edgelist.name / "raw" / str(graphlet_size)
    analysis_out = analysis_out / edgelist.name / "artifacts" / str(graphlet_size)
    original = analysis_data / edgelist.name

    local_out = analysis_out / "local"
    os.makedirs(local_out, exist_ok=True)
    run_local_analysis(local_out, original)

    global_out = analysis_out / "global"
    os.makedirs(global_out, exist_ok=True)
    run_global_analysis(analysis_data, global_out, graphlet_size, original)

    # TODO: Create report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis_out", required=True, type=Path)
    parser.add_argument("--edgelist_path", required=True, type=Path)
    parser.add_argument("--graphlet_size", required=True, type=int, default=3, choices=[3, 4])

    args = parser.parse_args()

    main(args.analysis_out, args.edgelist_path, args.graphlet_size)
