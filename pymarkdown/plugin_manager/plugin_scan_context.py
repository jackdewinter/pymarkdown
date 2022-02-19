"""
Module to provide context when reporting any errors.
"""


class PluginScanContext:
    """
    Class to provide context when reporting any errors.
    """

    def __init__(self, owning_manager, scan_file):
        self.owning_manager, self.scan_file, self.line_number = (
            owning_manager,
            scan_file,
            0,
        )
        self.__reported = []

    # pylint: disable=too-many-arguments
    def add_triggered_rule(
        self,
        scan_file,
        line_number,
        column_number,
        rule_id,
        rule_name,
        rule_description,
        extra_error_information,
    ):
        """
        Add the triggering information for a rule.
        """
        new_entry = (
            scan_file,
            line_number,
            column_number,
            rule_id,
            rule_name,
            rule_description,
            extra_error_information,
        )
        self.__reported.append(new_entry)

    # pylint: enable=too-many-arguments

    def report_on_triggered_rules(self):
        """
        Report on the various points where rules were triggered,
        in sorted order.
        """
        reported_and_sorted = sorted(self.__reported)

        for next_entry in reported_and_sorted:
            self.owning_manager.log_scan_failure(
                scan_file=next_entry[0],
                line_number=next_entry[1],
                column_number=next_entry[2],
                rule_id=next_entry[3],
                rule_name=next_entry[4],
                rule_description=next_entry[5],
                extra_error_information=next_entry[6],
            )
        self.__reported.clear()
