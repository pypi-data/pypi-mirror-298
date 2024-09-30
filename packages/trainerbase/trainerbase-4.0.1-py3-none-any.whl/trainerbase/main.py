from collections.abc import Callable
from os import _exit as force_exit
from traceback import print_exc
from typing import NoReturn

from trainerbase.codeinjection import safely_eject_all_code_injections
from trainerbase.common.rainbow import gradient_updater
from trainerbase.gameobject import update_frozen_objects
from trainerbase.gui.objects import update_displayed_objects
from trainerbase.process import shutdown_if_process_exited
from trainerbase.scriptengine import (
    enabled_by_default,
    process_healthcheck_script_engine,
    rainbow_script_engine,
    system_script_engine,
)
from trainerbase.speedhack import SpeedHack


type Callback = Callable[[], None]


def run(  # pylint: disable=too-complex
    run_gui: Callable[[Callback, Callback], None],
    on_gui_initialized_hook: Callback | None = None,
    on_shutdown_hook: Callback | None = None,
) -> NoReturn:
    def on_shutdown() -> NoReturn:
        rainbow_script_engine.stop()
        system_script_engine.stop()
        process_healthcheck_script_engine.stop()

        safely_eject_all_code_injections()
        SpeedHack.disable()

        if on_shutdown_hook is not None:
            on_shutdown_hook()

        force_exit(0)

    def on_gui_initialized() -> None:
        system_script_engine.start()
        process_healthcheck_script_engine.start()
        rainbow_script_engine.start()

        if on_gui_initialized_hook is not None:
            try:
                on_gui_initialized_hook()
            except Exception:
                print_exc()
                on_shutdown()

    system_script_engine.simple_script(update_frozen_objects, enabled=True)
    system_script_engine.simple_script(update_displayed_objects, enabled=True)
    process_healthcheck_script_engine.simple_script(shutdown_if_process_exited, enabled=True)
    rainbow_script_engine.register_script(enabled_by_default(gradient_updater))

    try:
        run_gui(on_gui_initialized, on_shutdown)
    except Exception:
        print_exc()

    on_shutdown()
