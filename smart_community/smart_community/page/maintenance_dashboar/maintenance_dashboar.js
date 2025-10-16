frappe.pages['maintenance-dashboar'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Maintenance Dashboard',
        single_column: true
    });

    page.set_title_sub('Track and manage maintenance tickets');
    page.set_indicator('Active', 'green');

    // Primary & secondary buttons
    page.set_primary_action('New Ticket', () => frappe.new_doc('Maintenance Ticket'), 'octicon octicon-plus');
    page.set_secondary_action('Refresh', () => location.reload(), 'octicon octicon-sync');

    // Inner buttons
    page.add_inner_button('Open', () => show_status('Open'));
    page.add_inner_button('In Progress', () => show_status('In Progress'));
    page.add_inner_button('Resolved', () => show_status('Resolved'));
    page.add_inner_button('Closed', () => show_status('Closed'));

    // Select field
    let status_field = page.add_field({
        label: 'Status',
        fieldtype: 'Select',
        fieldname: 'status',
        options: ['Open', 'In Progress', 'Resolved', 'Closed'],
        change(value) {
            frappe.msgprint(`Filtering by: ${value}`);
            show_status(value);
        }
    });

    // Dynamically load Animate.css
    if (!$('link[href*="animate.min.css"]').length) {
        $('<link/>', {
            rel: 'stylesheet',
            type: 'text/css',
            href: 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
        }).appendTo('head');
    }

    // Dynamically load WOW.js
    if (typeof WOW === 'undefined') {
        $.getScript('https://cdnjs.cloudflare.com/ajax/libs/wow/1.1.2/wow.min.js', function() {
            new WOW().init();
        });
    } else {
        new WOW().init();
    }

    // Body content
    $(page.body).html(`
        <div class="p-4 wow animate__fadeInUp" data-wow-delay="0.3s">
            <h3 class="wow animate__fadeInDown" data-wow-delay="0.2s">Maintenance Overview</h3>
            <p>Select a status above to view respective tickets.</p>
            <div id="ticket-container"></div>
        </div>
    `);

    // Fetch and show tickets
    function show_status(status) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Maintenance Ticket",
                filters: { status },
                fields: ["name", "resident", "issue_type", "priority"]
            },
            callback: (r) => {
                let html = "";
                if (r.message && r.message.length) {
                    html = r.message.map((d, i) => `
                        <div class="card p-3 mb-2 wow animate__fadeInUp" data-wow-delay="${i*0.1}s">
                            <b>${d.name}</b><br>
                            Resident: ${d.resident || '-'}<br>
                            Issue Type: ${d.issue_type || '-'}<br>
                            Priority: ${d.priority || '-'}
                        </div>
                    `).join("");
                } else {
                    html = `<div class="text-muted wow animate__fadeIn">No ${status} tickets found.</div>`;
                }
                $("#ticket-container").html(html);
                new WOW().init(); // Re-init WOW for dynamically added elements
                frappe.msgprint(`Loaded ${status} tickets.`);
            }
        });
    }
};
