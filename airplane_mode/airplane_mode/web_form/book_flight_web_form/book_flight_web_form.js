frappe.ready(function() {
	// bind events here
	const urlParams=new URLSearchParams(window.location.search);
	const flight=urlParams.get('flight');

	if (flight) {
        // set value of flight field
        frappe.web_form.set_value('flight', flight);
        // optionally make it read-only
        $('[data-fieldname="flight"] input, [data-fieldname="flight"] select').prop('disabled', true);
	}
});

