# SPDX-FileCopyrightText: 2022-present deepset GmbH <info@deepset.ai>
#
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

from haystack.core.component import component


@component
class TransientValue:
    """
    Pss through provided value.
    """

    @component.output_types(value=int)
    def run(self, value: Optional[int] = 1):
        return {"value": value}
