from pymarkdown.plugin_manager.plugin_modify_context import PluginModifyContext


class MockPluginModifyContext(PluginModifyContext):
    def __init__(
        self, in_fix_mode: bool = True, is_during_line_pass: bool = False
    ) -> None:
        self.__is_during_line_pass = is_during_line_pass
        self.__in_fix_mode = in_fix_mode

    @property
    def is_during_line_pass(self) -> bool:
        """
        Report on whether fix mode is currently going through a line pass.
        """
        return self.__is_during_line_pass

    @property
    def in_fix_mode(self) -> bool:
        """
        Report on whether the application is in fix mode.x
        """
        return self.__in_fix_mode
