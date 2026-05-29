import frappe


def sanitize_expression(string: str | None = None) -> str | None:
	"""
	Removes leading and trailing whitespace and merges multiline strings into a single line.

	Args:
	    string (str, None): The string expression to be sanitized. Defaults to None.

	Returns:
	    str or None: The sanitized string expression or None if the input string is None.

	Example:
	    expression = "\r\n    gross_pay > 10000\n    "
	    sanitized_expr = sanitize_expression(expression)

	"""

	if not string:
		return None

	parts = string.strip().splitlines()
	string = " ".join(parts)

	return string


@frappe.whitelist()
def get_payroll_settings_for_payment_days(employee=None) -> dict:
	settings = frappe.get_cached_value(
		"Payroll Settings",
		None,
		[
			"payroll_based_on",
			"consider_unmarked_attendance_as",
			"include_holidays_in_total_working_days",
			"consider_marked_attendance_on_holidays",
		],
		as_dict=True,
	)
	if employee:
		override = frappe.get_cached_value(
			"Employee", employee, "custom_include_holidays_in_total_working_days"
		)
		if override == "Yes":
			settings["include_holidays_in_total_working_days"] = 1
		elif override == "No":
			settings["include_holidays_in_total_working_days"] = 0
	return settings
