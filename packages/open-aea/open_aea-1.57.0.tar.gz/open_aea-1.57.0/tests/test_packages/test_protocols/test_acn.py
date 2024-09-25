# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the tests of the messages module."""

import os
from pathlib import Path
from types import ModuleType

from libs.go.aealite.protocols.acn import v1_0_0 as aealite_acn  # type: ignore

from packages.valory.protocols import acn as package_acn


def test_aealite_protocol_matching():
    """Ensure ACN protocol files are identical on aealite"""

    def get_path(module: ModuleType) -> Path:
        return Path(os.path.sep.join(module.__package__.split(".")))  # type: ignore

    acn_path, aealite_path = map(get_path, (package_acn, aealite_acn))

    readme = (acn_path / "README.md").read_text()
    yaml = (aealite_path / "acn.yaml").read_text()
    assert yaml in readme

    go_package = """option go_package = "libp2p_node/protocols/acn/v1_0_0";\n\n"""
    acn, aealite = ((p / "acn.proto").read_text() for p in (acn_path, aealite_path))
    assert acn == aealite.replace(go_package, "")
