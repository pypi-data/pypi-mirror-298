"""Project pipelines."""

from typing import Dict

from kedro.pipeline import Pipeline

from quafel.pipelines import data_generation as dg
from quafel.pipelines import data_science as ds
from quafel.pipelines import visualization as viz

import glob
from pathlib import Path


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    # get all the partitions created with the "prepare" pipeline
    all_partitions = [Path(f).stem for f in glob.glob("data/02_intermediate/*.csv")]

    # ----------------------------------------------------------------
    # Gather all the existing artifacts and calculate the difference
    # ----------------------------------------------------------------

    # get all existing circuits, durations and results.
    # The hooks run prior to this, so
    # in case we don't want to restore existing results,
    # we should find empty directories
    existing_circuits = [Path(f).stem for f in glob.glob("data/03_qasm_circuits/*.txt")]
    # get all existing durations and results. The hooks run prior to this,
    # so in case we don't want to restore existing results,
    # we should find empty directories
    existing_measures = [Path(f).stem for f in glob.glob("data/04_measures/*.csv")]
    existing_durations = [
        Path(f).stem for f in glob.glob("data/06_execution_durations/*.csv")
    ]
    existing_results = [
        Path(f).stem for f in glob.glob("data/05_execution_results/*.csv")
    ]

    # get the intersection of the durations and results
    existing_evals = [m for m in existing_durations if m in existing_results]
    # .. and the intersection of all partitions
    ds_partitions = [p for p in all_partitions if p not in existing_evals]

    # gather all the .tmp files to create figures output
    tmp_files = [Path(f).stem for f in glob.glob("data/08_reporting/*.tmp")]

    # ----------------------------------------------------------------
    # Create the pipelines
    # ----------------------------------------------------------------

    # pass only the number of partitions we want to generate circuits for
    dg_pipelines = dg.create_pipeline(
        partitions=all_partitions,
        existing_circuits=existing_circuits,
        existing_measures=existing_measures,
    )
    # pass only the number of partitions we want to evaluate
    # (this would be equal to all partitions in an initial run or
    # in case we don't want to restore existing results)
    ds_pipelines = ds.create_pipeline(partitions=ds_partitions)
    viz_pipelines = viz.create_pipeline(figures=tmp_files)

    return {
        "__default__": dg_pipelines["pl_generate_evaluation_partitions"]
        + dg_pipelines["pl_generate_qasm_circuits"]
        + ds_pipelines["pl_parallel_measure_execution_durations"]
        + viz_pipelines["pl_visualize_evaluations"],
        "prepare": dg_pipelines["pl_generate_evaluation_partitions"],
        "measure": dg_pipelines[
            # "pl_generate_qasm_circuits"
            "pl_generate_qasm_circuits"
        ]
        + ds_pipelines["pl_parallel_measure_execution_durations"],
        # ct measure is the same as the measure pipeline, but we need to
        # tell the hooks that we don't want to delete the existing results
        "combine": ds_pipelines["pl_combine_evaluations"],
        "visualize": viz_pipelines["pl_visualize_evaluations"],
        "print_tests": viz_pipelines["pl_print_tests"],
    }
