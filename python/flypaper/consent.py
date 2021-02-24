"""
This module imeplements Flypaper's user consent mechanisms.
"""
import os
from typing import Callable, List, Optional, Sequence, Union

ConsentMechanism = Callable[[], bool]


class FlypaperConsent:
    """
    FlypaperConsent stores the client's consent settings.
    """

    def __init__(self, *mechanisms: Union[bool, ConsentMechanism]) -> None:
        if not mechanisms:
            mechanisms = [False]
        self._mechanisms = mechanisms

    def check(self) -> bool:
        """
        Checks if all consent mechanisms signal the user's consent. If any of them signal False, returns
        False. Otherwise, returns True.
        """
        for mechanism in self._mechanisms:
            if mechanism is True:
                continue
            elif mechanism is False:
                return False
            elif not mechanism():
                return False
        return True


def environment_variable_opt_in(
    varname: str, affirmative_values: Sequence[str]
) -> ConsentMechanism:
    def mechanism() -> bool:
        if os.environ.get(varname) in affirmative_values:
            return True
        return False

    return mechanism


def environment_variable_opt_out(
    varname: str, negative_values: Sequence[str]
) -> ConsentMechanism:
    def mechanism() -> bool:
        if os.environ.get(varname) in negative_values:
            return False
        return True

    return mechanism