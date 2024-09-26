import pytest

def pytest_addoption(parser):
    parser.addoption("--jupyter-file",
                    default="",
                    type=str,
                    action="store",
                    help="Full path of the JupyterLab file")

    parser.addoption("--applet-id",
                    default="applet-GXY9vBj09z7kZFFxj4kGqJj0",
                    type=str,
                    action="store",
                    help="xvJupyterLab applet id")
    
    parser.addoption("--requirement-file",
                    default="",
                    type=str,
                    action="store",
                    help="Requirement file id")


@pytest.fixture
def cmdopt_jupyter_file(request):
    return request.config.getoption("--jupyter-file")

@pytest.fixture
def cmdopt_applet_id(request):
    return request.config.getoption("--applet-id")

@pytest.fixture
def cmdopt_requirement_file(request):
    return request.config.getoption("--requirement-file")