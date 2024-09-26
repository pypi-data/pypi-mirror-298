from argparse import ArgumentParser
from argparse import _SubParsersAction as Subparser
from pathlib import Path

from lisa.globalfit.framework.logging import DEFAULT_LOG_LEVEL, LOG_LEVELS

DEFAULT_SIGNAL = Path("simulated_signal.h5")


def add_common_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--log-level",
        choices=LOG_LEVELS,
        default=DEFAULT_LOG_LEVEL,
        help="set the logging level",
    )
    parser.add_argument(
        "--servers",
        nargs="+",
        default=["nats://localhost:4222"],
        help="event bus server URLs",
    )
    parser.add_argument(
        "--pipeline-run-id",
        help="pipeline run identifier",
    )
    parser.add_argument(
        "--workdir",
        help="Working directory",
        type=Path,
    )


def add_simulator_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "simulate-signal",
        help="simulate input gaussian signals",
    )
    subparser.add_argument(
        "--n-gaussians",
        type=int,
        default=2,
        help="number of gaussians to sum",
    )
    subparser.add_argument(
        "--n-samples",
        type=int,
        default=365,
        help="number of data points to simulate",
    )
    subparser.add_argument(
        "--snr",
        type=int,
        default=20,
        help="signal to noise ratio",
    )
    subparser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_SIGNAL,
        help="output file to write the simulated data to",
    )


def add_preprocessing_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "preprocess",
        help="run preprocessors on input dataset",
    )
    subparser.add_argument(
        "--group-label",
        type=str,
        help="label for modules of this group",
        required=True,
    )
    subparser.add_argument(
        "--input-data",
        type=Path,
        help="input dataset",
        required=True,
    )
    subparser.add_argument(
        "--input-checkpoint",
        type=Path,
        help="checkpoint of previous iteration",
    )
    subparser.add_argument(
        "--output-preprocessed-signal",
        type=Path,
        help="pre-processed input signal forwarded to modules",
        required=True,
    )
    subparser.add_argument(
        "--output-group-configuration-path",
        type=Path,
        default=Path("config_group.json"),
        help="configuration file of group",
    )


def add_modules_execution_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "start-modules",
        help="spawn processing modules",
    )
    subparser.add_argument(
        "--input-group-configuration-path",
        type=Path,
        help="group configuration file",
        required=True,
    )
    subparser.add_argument(
        "--input-data",
        type=Path,
        help="input dataset",
        required=True,
    )
    subparser.add_argument(
        "--current-iteration",
        help="current iteration index",
        type=int,
        required=True,
    )
    subparser.add_argument(
        "--n-steps",
        type=int,
        help="number of MCMC steps to perform",
        default=1000,
    )


def add_module_execution_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "start-module",
        help="spawn a single processing module",
    )
    subparser.add_argument(
        "--input-data",
        type=Path,
        help="input dataset",
        required=True,
    )
    subparser.add_argument(
        "--group-label",
        help="group label",
        type=str,
        required=True,
    )
    subparser.add_argument(
        "--module-label",
        help="module label",
        type=str,
        required=True,
    )
    subparser.add_argument(
        "--input-group-configuration-path",
        help="module initial configuration",
        type=Path,
        required=True,
    )
    subparser.add_argument(
        "--current-iteration",
        help="current iteration index",
        type=int,
        required=True,
    )
    subparser.add_argument(
        "--n-steps",
        type=int,
        help="number of MCMC steps to perform",
        default=1000,
    )
    subparser.add_argument(
        "--output-checkpoint",
        type=Path,
        help="module state needed to resume execution",
        required=True,
    )


def add_engine_execution_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "start-engine",
        help="start framework engine",
    )
    subparser.add_argument(
        "--expected-groups",
        type=Path,
        help="expected worker groups",
        required=True,
    )
    subparser.add_argument(
        "--output-checkpoint",
        type=Path,
        help="output iteration checkpoint",
        default=Path("checkpoint.json"),
    )
    subparser.add_argument(
        "--output-iteration-decision",
        type=Path,
        help="iteration decision from rules evaluation",
        required=True,
    )
    subparser.add_argument(
        "--catalog-db",
        type=Path,
        help="local catalog of detected sources",
    )
    subparser.add_argument(
        "--max-iterations",
        type=int,
        help="maximum number of iterations",
        required=True,
    )
    subparser.add_argument(
        "--current-iteration",
        type=int,
        help="current iteration number",
        required=True,
    )


def add_execution_plot_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "plot",
        help="plot MCMC results",
    )
    subparser.add_argument(
        "--input-chain",
        type=Path,
        help="path to an HDF5 file containing sampler chains",
        required=True,
    )
    subparser.add_argument(
        "--chain-location",
        type=str,
        default="mcmc/chain",
        help="path to chain dataset in input file",
    )


def add_execution_monitoring_args(parser: Subparser) -> None:
    subparser: ArgumentParser = parser.add_parser(
        "monitor",
        help="monitor global fit execution",
    )
    subparser.add_argument(
        "--port",
        type=int,
        help="server port",
        default=8080,
    )
    subparser.add_argument(
        "--api-url",
        type=str,
        help="URL of the backend service",
        default="http://localhost:8080",
    )
    subparser.add_argument(
        "--s3-bucket",
        type=str,
        help="name of S3 bucket storing module checkpoints",
        required=True,
    )
