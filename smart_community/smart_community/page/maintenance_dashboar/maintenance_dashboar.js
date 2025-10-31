frappe.pages['maintenance-dashboar'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Maintenance Dashboard',
        single_column: true
    });

    page.set_title_sub('Track and manage maintenance tickets');
    page.set_indicator('Active', 'green');

    // Load Animate.css & WOW.js
    if (!$('link[href*="animate.min.css"]').length) {
        $('<link/>', { rel: 'stylesheet', href: 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css' }).appendTo('head');
    }
    if (typeof WOW === 'undefined') {
        $.getScript('https://cdnjs.cloudflare.com/ajax/libs/wow/1.1.2/wow.min.js', function() { new WOW().init(); });
    } else { new WOW().init(); }

    // HTML structure
    $(page.body).html(`
        <div class="dashboard-container p-4">
            <div class="filter-bar mb-4 d-flex flex-wrap gap-3">
                <select id="statusFilter" class="form-select theme-filter">
                    <option value="">All Status</option>
                    <option value="Open">Open</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Resolved">Resolved</option>
                    <option value="Closed">Closed</option>
                </select>
                <select id="priorityFilter" class="form-select theme-filter">
                    <option value="">All Priority</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                </select>
            </div>
            <div id="ticket-grid" class="row g-4"></div>
        </div>
    `);

    let ticketsData = [];

    // Fetch tickets
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Maintenance Ticket',
            fields: ['name','resident','issue_type','priority','status','creation'],
            order_by: 'creation desc'
        },
        callback: function(r) {
            ticketsData = r.message || [];
            renderTicketGrid(ticketsData);
        }
    });

    // Filters change
    $('#statusFilter, #priorityFilter').on('change', function() {
        const status = $('#statusFilter').val();
        const priority = $('#priorityFilter').val();
        let filtered = ticketsData;
        if (status) filtered = filtered.filter(t => t.status === status);
        if (priority) filtered = filtered.filter(t => t.priority === priority);
        renderTicketGrid(filtered, status);
    });

    function renderTicketGrid(tickets, activeStatus='') {
        const grid = $('#ticket-grid');
        let html = '';

        if (tickets.length === 0) {
            html = `<div class="col-12 text-center text-muted wow animate__fadeIn">No tickets found.</div>`;
        } else {
            tickets.forEach((t, i) => {
                html += `
                    <div class="col-lg-4 col-md-6 col-sm-12 wow animate__fadeInUp" data-wow-delay="${i*0.1}s">
                        <div class="ticket-card">
                            <h5 class="ticket-title mb-2">${t.name}</h5>
                            <p><strong>Resident:</strong> ${t.resident || '-'}</p>
                            <p><strong>Issue:</strong> ${t.issue_type || '-'}</p>
                            <p><strong>Status:</strong> 
                                <span class="badge status-badge ${t.status === activeStatus ? 'active-status' : ''}">${t.status}</span>
                            </p>
                            <p><strong>Priority:</strong> <span class="priority-text">${t.priority || '-'}</span></p>
                            <p class="text-muted small mb-0">Created: ${t.creation.split(' ')[0]}</p>
                        </div>
                    </div>
                `;
            });
        }

        grid.html(html);
        new WOW().init();
    }
    

    // CSS Styling
    const style = document.createElement('style');
    style.innerHTML = `
        body { background: #f8f9fa; font-family: 'Inter', sans-serif; }
        .ticket-card {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s, box-shadow 0.3s;
            padding: 20px;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .ticket-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.08);
        }
        .ticket-card p { margin: 6px 0; font-size: 0.95rem; }
        .ticket-title { font-weight: 600; color: #333333; }
        .priority-text { font-weight: 600; }
        .filter-bar .theme-filter {
            background: #e3f2ff;
            color: #0d3b66;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 6px 12px;
            min-width: 150px;
        }
        .filter-bar .theme-filter option { background: #e3f2ff; }
        .status-badge {
            background: #3498db;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .status-badge.active-status {
            background: #21618c;
        }
        @media (max-width: 992px) { .ticket-card { padding: 16px; } }
        @media (max-width: 576px) { .ticket-card { padding: 14px; } }
    `;
    document.head.appendChild(style);
};
