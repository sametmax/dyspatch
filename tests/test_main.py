
import dyspatch


def test_version():
    assert "." in dyspatch.__version__
    assert len(dyspatch.__version__) >= 5
