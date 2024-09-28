# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_coveragemarkers',
 'pytest_coveragemarkers.filter_specs',
 'pytest_coveragemarkers.heirarchical',
 'pytest_coveragemarkers.marker_specs',
 'pytest_coveragemarkers.utils']

package_data = \
{'': ['*'], 'pytest_coveragemarkers.marker_specs': ['jira/*']}

install_requires = \
['PyYAML>=5.4.1',
 'loguru>=0.6.0,<0.7.0',
 'pytest-jtr>=1.4.0',
 'pytest-xdist>=2.5.0,<3.0.0',
 'pytest>=7.1.2,<8.0.0',
 'rich>=13.3.0,<14.0.0',
 'rule-engine>=4.5.0,<5.0.0',
 'urllib3>2.2.1']

entry_points = \
{'console_scripts': ['prep-dev-release = scripts.prep_release:dev',
                     'prep-major-release = scripts.release_process:prep_major',
                     'prep-minor-release = scripts.release_process:prep_minor',
                     'prep-patch-release = scripts.release_process:prep_patch',
                     'release = scripts.release_process:upload_release'],
 'pytest11': ['coveragemarkers = pytest_coveragemarkers.plugin']}

setup_kwargs = {
    'name': 'pytest-coveragemarkers',
    'version': '3.3.0',
    'description': 'Using pytest markers to track functional coverage and filtering of tests',
    'long_description': '======================\npytest-coveragemarkers\n======================\n\n.. image:: https://img.shields.io/badge/security-bandit-yellow.svg\n    :target: https://github.com/PyCQA/bandit\n    :alt: Security Status\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\nUsing pytest markers to track functional coverage and filtering of tests\n\n----\n\nThis `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_\'s `cookiecutter-pytest-plugin`_ template.\n\n\nFeatures\n--------\n\n* Definition of CoverageMarkers© in YAML format\n* Support for applying CoverageMarkers© to tests\n* Filtering of tests based on CoverageMarkers©\n* Inclusion of CoverageMarkers© in JSON report\n\n\nInstallation\n------------\n\nYou can install "pytest-coveragemarkers" from `PyPI`_::\n\n    $ pip install pytest-coveragemarkers\n    # or\n    $ poetry add pytest-coveragemarkers\n\nUsage\n-----\n\nStep 1: Define your coverage markers yaml.\n\n    Using the format:\n\n.. code-block:: yaml\n\n  markers:\n    - name: <marker_name>\n      allowed:\n        - <marker_value_1>\n        - <marker_value_2>\n    - name: <marker2_name>\n      allowed:\n        - <marker2_value_1>\n        - <marker2_value_2>\n\nThen decorate your tests with them\n\n\n.. code-block:: python\n\n    import pytest\n\n    @pytest.mark.marker_name([\'value1\', \'value2\'])\n    @pytest.mark.marker2_name([\'value1\', \'value2\'])\n    def test_x():\n        ...\n\n    @pytest.mark.marker2_name([\'value1\', \'value2\'])\n    def test_y():\n        ...\n\n\nThen when the tests are executed with\n\n.. code-block:: shell\n\n    pytest --json-report --markers-location=/full/path/to/coverage_markers.yml\n\nThen the JSON Test Report output from the test execution contains:\n\n.. code-block:: json\n\n    "tests": [\n    {\n      "nodeid": "...",\n      "metadata": {\n        "cov_markers": {\n          "marker_name": {\n            "value1": true,\n            "value2": true\n          },\n          "marker2_name": {\n            "value1": true,\n            "value2": true\n          }\n        }\n      }\n    },\n    ...\n    ]\n\nThis can then be used to generate test coverage details based on the coverage markers.\nA nice demo will be produced to give examples of usage.\n\nBut wait there is another benefit:\n\nWe can filter tests for execution based on their coverage markers\n\n.. code-block:: shell\n\n    pytest \\\n        --filter=\'"value1" in marker_name\' \\\n        --json-report \\\n        --markers-location=/full/path/to/coverage_markers.yml\n\nThe above command run against the tests defined above would select \'test_x\' and deselect \'test_y\' for execution\n\nOther examples of filters are:\n\n.. code-block: shell\n\n    \'("value1" in marker_name) or ("value2" in marker_name)\'\n\nYou can also supply the path to a file containing your filter.\nUse argument --filter-location or key FilterLocation in the pytest.ini file.\n\nMandatory Coverage Markers\n--------------------------\n\nCoverage markers can be detailed as mandatory by including the mandatory attribute.\n\nE.g.\n\n.. code-block:: yaml\n\n  markers:\n    - name: <marker_name>\n      mandatory: True\n      allowed:\n        - <marker_value_1>\n        - <marker_value_2>\n\nDependent Coverage Markers\n--------------------------\n\nCoverage markers can be detailed as a dependency on another marker.\nThis ensures that if a marker is specified all dependencies of this\nmarker in the chain must also be specified.\n\nE.g.\n\n.. code-block:: yaml\n\n  markers:\n    - name: <marker_name>\n      dependents:\n        - <marker_name...>\n        - <marker_name...>\n      allowed:\n        - <marker_value_1>\n        - <marker_value_2>\n\n\nCoverage Marker Argument Format\n-------------------------------\n\nThe arguments supplied to Coverage Markers can follow multiple formats which allows the user to define the format that best suites them.\n\nE.g.\n\n.. code-block:: python\n\n    import pytest\n\n    @pytest.mark.marker_1(\'value1\')                 # single string argument\n    @pytest.mark.marker_2(\'value1\', \'value2\')       # multiple string arguments\n    @pytest.mark.marker_3([\'value1\', \'value2\'])     # list of arguments\n    @pytest.mark.marker_4((\'value1\', \'value2\'))     # tuple of arguments\n    def test_x():\n        ...\n\n\n\nTesting\n-------\n\nNox is used by this project to execute all tests.\nTo run a specific set of tests execute the below line::\n\n    $ poetry run nox -s <session_name>\n\nWhere session_name can be one of the following\n\n.. list-table:: Nox Sessions\n   :widths: 25 75\n   :header-rows: 1\n\n   * - Session Name\n     - Session Details\n   * - unit_tests\n     - Execute all tests marked as unit\n   * - functional_tests\n     - Execute all tests marked as functional\n\nThought Process\n---------------\n\n* The `pytest_docs`_ talks about using markers to set metadata on tests and use the markers to select required tests for execution.\n* For the markers I want to add, I also want to specify a list of values that go along with that marker.\n  E.g. If the marker was \'colour\' then supported values may be \'Red\', \'Green\', \'Gold\'.\n* I also want the list of values validated against supported values so no unsupported values can be added.\n  E.g. If the marker was \'colour\' then a value of \'Panda\' would not be allowed.\n* Then all this meta data I want to come out in the junit json report.\n* Next I want to use these markers and their supported values to filter tests. For this I need a more powerful filter engine.\n\nDocumentation\n-------------\n\nTo build the docs run::\n\n    poetry run mkdocs serve\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-coveragemarkers" is free and open source software\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n\nFuture Changes\n--------------\n\n* Type-Hints\n* Full Test Coverage\n* Full Documentation\n\n\n.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter\n.. _`@hackebrot`: https://github.com/hackebrot\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause\n.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt\n.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0\n.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin\n.. _`file an issue`: https://github.com/Gleams99/pytest-coveragemarkers/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`nox`: https://nox.thea.codes/en/stable/\n.. _`pip`: https://pypi.org/project/pip/\n.. _`PyPI`: https://pypi.org/project\n.. _`pytest_docs`: https://docs.pytest.org/en/7.1.x/how-to/mark.html?highlight=slow\n',
    'author': 'Gleams API user',
    'author_email': 'Stephen.Swannell+ghapi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.13.0',
}


setup(**setup_kwargs)
