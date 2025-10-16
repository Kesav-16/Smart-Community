frappe.ready(() => {
    console.log("✅ Maintenance Ticket Web Form Loaded");

    // 1️⃣ --- Inject Custom Navbar ---
    const navbarHTML = `
        <div class="custom-navbar">
  <div class="nav-left">
    <a href="#" id="guestDashboardLink">Dashboard</a>
    <a href="/about">About</a>
    <a href="/monthly-bill" id="monthlyBillBtn">Monthly Bill</a>
    <a href="/maintenance-ticket/new">Raise Ticket</a>
  </div>
  <div class="nav-right">
    <a href="#" id="logoutBtn">Logout</a>
  </div>
</div>
    `;
    const navbarStyle = `
        <style>
        .custom-navbar { width: 85%; background: #1e40af; margin-top:20px;margin-left:120px;color: white; display: flex; justify-content: space-between; align-items: center; padding: 15px 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000; }
.custom-navbar a { color: white; text-decoration: none; font-weight: 600; margin: 0 15px; transition: color 0.3s; }
.custom-navbar a:hover { color: #ffeb3b; }
        </style>
    `;
    $('body').prepend(navbarStyle + navbarHTML);

    // 2️⃣ --- Hide default Frappe navbar ---
    const deskNav = document.querySelector(".navbar, #navbarSupportedContent");
    if (deskNav) deskNav.style.display = "none";

    // 3️⃣ --- Set default status field ---
    frappe.web_form.set_value("status", "Open");

    // 4️⃣ --- Determine Email (URL → then session fallback) ---
    const params = new URLSearchParams(window.location.search);
    let userEmail = params.get("email"); // ✅ Priority: URL first

    if (!userEmail && frappe.session.user !== "Guest") {
        userEmail = frappe.session.user; // fallback if no ?email=
    }

    // 5️⃣ --- Dashboard Redirect Logic ---
    const dashboardLink = document.getElementById("guestDashboardLink");
    if (dashboardLink) {
        dashboardLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (userEmail) {
                const encodedEmail = encodeURIComponent(userEmail);
                window.location.href = `http://smart.localhost:8001/guest-dashboard?email=${encodedEmail}`;
            } else {
                frappe.msgprint("⚠️ No email found in URL or session.");
            }
        });
    }

    // 6️⃣ --- Auto-fill Resident (optional for logged-in users) ---
    if (frappe.session.user !== "Guest") {
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Resident",
                filters: { user_id: frappe.session.user }
            },
            callback: (r) => {
                if (r.message) {
                    frappe.web_form.set_value("resident", r.message.name);
                }
            }
        });
    }

    const logoutBtn = document.getElementById("logoutBtn");
    logoutBtn.addEventListener("click", function(e) {
        e.preventDefault();
        sessionStorage.removeItem("guest_email");
        frappe.msgprint("You have been logged out.");
        window.location.href = "/guest-login";
    });

    document.getElementById("guestDashboardLink").addEventListener("click", e => { 
    e.preventDefault(); 
    window.location.href="/guest-dashboard"; 
  });

    // 7️⃣ --- After Save Confirmation ---
    frappe.web_form.on("after_save", () => {
        frappe.msgprint("✅ Your maintenance request has been submitted successfully!");
    });
});
