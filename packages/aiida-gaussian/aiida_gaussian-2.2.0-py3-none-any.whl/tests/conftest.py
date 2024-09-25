# pylint: disable=redefined-outer-name
"""Module with test fixtures."""
import collections
import pathlib

import pytest
from aiida.common.folders import Folder
from aiida.common.links import LinkType
from aiida.engine.utils import instantiate_process
from aiida.manage.manager import get_manager
from aiida.orm import CalcJobNode, FolderData
from aiida.plugins import ParserFactory

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


@pytest.fixture
def fixture_localhost(aiida_localhost):
    """Return a localhost `Computer`."""
    localhost = aiida_localhost
    localhost.set_default_mpiprocs_per_machine(1)
    return localhost


@pytest.fixture
def fixture_code(fixture_localhost):
    """Return a `Code` instance configured to run calculations of given entry point on localhost `Computer`."""

    def _fixture_code(entry_point_name):
        from aiida.orm import Code

        return Code(
            input_plugin_name=entry_point_name,
            remote_computer_exec=[fixture_localhost, "/bin/true"],
        )

    return _fixture_code


@pytest.fixture
def filepath_tests() -> pathlib.Path:
    """Return the path to the tests folder."""
    return pathlib.Path(__file__).resolve().parent


@pytest.fixture
def generate_calc_job(tmp_path):
    """Return a factory to generate a :class:`aiida.engine.CalcJob` instance with the given inputs.

    The fixture will call ``prepare_for_submission`` and return a tuple of the temporary folder that was passed to it,
    as well as the ``CalcInfo`` instance that it returned.
    """

    def factory(process_class, inputs=None, return_process=False):
        """Create a :class:`aiida.engine.CalcJob` instance with the given inputs."""
        manager = get_manager()
        runner = manager.get_runner()
        process = instantiate_process(runner, process_class, **inputs or {})
        calc_info = process.prepare_for_submission(Folder(tmp_path))

        if return_process:
            return process

        return tmp_path, calc_info

    return factory


@pytest.fixture
def generate_calc_job_node(filepath_tests, aiida_computer_local):
    """Create and return a :class:`aiida.orm.CalcJobNode` instance."""

    def flatten_inputs(inputs, prefix=""):
        """Flatten inputs recursively like :meth:`aiida.engine.processes.process::Process._flatten_inputs`."""
        flat_inputs = []
        for key, value in inputs.items():
            if isinstance(value, collections.abc.Mapping):
                flat_inputs.extend(flatten_inputs(value, prefix=prefix + key + "__"))
            else:
                flat_inputs.append((prefix + key, value))
        return flat_inputs

    def factory(
        entry_point: str,
        parser_entry_point_name: str,
        test_name: str,
        inputs: dict = None,
    ):
        """Create and return a :class:`aiida.orm.CalcJobNode` instance."""
        node = CalcJobNode(
            computer=aiida_computer_local(),
            process_type=f"aiida.calculations:{entry_point}",
        )

        if inputs:
            for link_label, input_node in flatten_inputs(inputs):
                input_node.store()
                node.base.links.add_incoming(
                    input_node, link_type=LinkType.INPUT_CALC, link_label=link_label
                )

        node.store()

        filepath_retrieved = (
            filepath_tests
            / "parsers"
            / "fixtures"
            / parser_entry_point_name
            / test_name
        )

        retrieved = FolderData()
        retrieved.base.repository.put_object_from_tree(filepath_retrieved)
        retrieved.base.links.add_incoming(
            node, link_type=LinkType.CREATE, link_label="retrieved"
        )
        retrieved.store()

        return node

    return factory


@pytest.fixture(scope="session")
def generate_parser():
    """Fixture to load a parser class for testing parsers."""

    def factory(entry_point_name):
        """Fixture to load a parser class for testing parsers.

        :param entry_point_name: entry point name of the parser class
        :return: the `Parser` sub class
        """
        return ParserFactory(entry_point_name)

    return factory
