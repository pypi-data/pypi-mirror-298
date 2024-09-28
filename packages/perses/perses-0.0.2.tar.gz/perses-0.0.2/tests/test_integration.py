import pytest
from perses.model.dashboard import Dashboard


def test_node_exporter_full(request: pytest.FixtureRequest):
    filepath = request.path.parent.joinpath("testdata/node-exporter-full.json")
    Dashboard.model_validate_json(filepath.read_text())
