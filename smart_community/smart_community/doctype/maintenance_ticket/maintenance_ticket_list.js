frappe.listview_settings['Maintenance Ticket'] = {
    add_fields: ["resident", "priority", "issue_type", "status", "assigned_to"],

    get_indicator: function (doc) {
        if (doc.status === "Open") {
            return [__("Open"), "red", "status,=,Open"];
        } else if (doc.status === "In Progress") {
            return [__("In Progress"), "orange", "status,=,In Progress"];
        } else if (doc.status === "Resolved") {
            return [__("Resolved"), "blue", "status,=,Resolved"];
        } else if (doc.status === "Closed") {
            return [__("Closed"), "green", "status,=,Closed"];
        }
    },

    onload: function (listview) {
        // Helper function to apply filter instantly
        function filterByStatus(status) {
            listview.filter_area.clear(); // remove existing filters
            listview.filter_area.add([[listview.doctype, "status", "=", status]]);
            listview.refresh(); // reload list instantly
        }

        // Add status filter buttons
        listview.page.add_inner_button(__('View Open Tickets'), function () {
            filterByStatus("Open");
        });

        listview.page.add_inner_button(__('View In Progress Tickets'), function () {
            filterByStatus("In Progress");
        });

        listview.page.add_inner_button(__('View Resolved Tickets'), function () {
            filterByStatus("Resolved");
        });

        listview.page.add_inner_button(__('View Closed Tickets'), function () {
            filterByStatus("Closed");
        });
    },

    formatters: {
        priority(value) {
            if (value === "High") {
                return `<span class="indicator red">${value}</span>`;
            } else if (value === "Medium") {
                return `<span class="indicator orange">${value}</span>`;
            } else if (value === "Low") {
                return `<span class="indicator green">${value}</span>`;
            }
            return value;
        }
    }
};
