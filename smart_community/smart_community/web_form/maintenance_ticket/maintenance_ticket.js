frappe.ready(() => {
    console.log("✅ Maintenance Ticket Web Form Loaded");

    // 1️⃣ --- Inject Unified Right-Aligned Navbar ---
    const navbarHTML = `
    <nav class="custom-navbar">
      <div class="nav-container">
        <div class="menu-toggle" id="menuToggle">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="nav-links">
          <a href="#" id="guestDashboardLink">Dashboard</a>
          <a href="/monthly-bill" id="monthlyBillBtn">Monthly Bill</a>
          <a href="/maintenance-ticket/new">Raise Ticket</a>
          <a href="#" id="logoutBtn">Logout</a>
        </div>
      </div>
    </nav>
    `;

    const navbarStyle = `
    <style>
    body {
      margin: 0;
      font-family: 'Inter', sans-serif;
      background: #f8fafc;
    }

    /* ✅ Full-width Responsive Navbar */
    .custom-navbar {
      width: 100%;
      background: #2563eb;
      color: white;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      position: sticky;
      top: 0;
      z-index: 1000;
    }

    .nav-container {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      padding: 12px 30px;
      max-width: 1200px;
      margin: auto;
      position: relative;
    }

    .custom-navbar a {
      color: white;
      text-decoration: none;
      margin: 0 18px;
      font-weight: 600;
      font-size: 15px;
      transition: color 0.3s;
    }

    .custom-navbar a:hover {
      color: #ffeb3b;
    }

    .nav-links {
      display: flex;
      align-items: center;
    }

    /* ✅ Hamburger Icon */
    .menu-toggle {
      display: none;
      flex-direction: column;
      justify-content: center;
      cursor: pointer;
      position: absolute;
      right: 20px;
      top: 15px;
    }

    .menu-toggle span {
      width: 25px;
      height: 3px;
      background: white;
      margin: 4px 0;
      border-radius: 3px;
      transition: 0.3s;
    }

    /* ✅ Responsive Design */
    @media (max-width: 900px) {
      .nav-container {
        flex-direction: column;
        align-items: flex-end;
        padding: 10px 20px;
      }

      .menu-toggle {
        display: flex;
      }

      .nav-links {
        flex-direction: column;
        align-items: flex-end;
        width: 100%;
        display: none;
        background: #1e40af;
        border-radius: 8px;
        margin-top: 10px;
        overflow: hidden;
      }

      .nav-links.show {
        display: flex;
      }

      .custom-navbar a {
        width: 100%;
        text-align: right;
        padding: 12px 15px;
        margin: 0;
        border-top: 1px solid rgba(255,255,255,0.2);
      }
    }

    /* ✅ Hamburger Animation */
    .menu-toggle.active span:nth-child(1) {
      transform: rotate(45deg) translateY(8px);
    }
    .menu-toggle.active span:nth-child(2) {
      opacity: 0;
    }
    .menu-toggle.active span:nth-child(3) {
      transform: rotate(-45deg) translateY(-8px);
    }
    </style>
    `;

    $('body').prepend(navbarStyle + navbarHTML);

    // 2️⃣ --- Hide Default Frappe Navbar ---
    const deskNav = document.querySelector(".navbar, #navbarSupportedContent");
    if (deskNav) deskNav.style.display = "none";

    // 3️⃣ --- Set Default Field ---
    frappe.web_form.set_value("status", "Open");

    // 4️⃣ --- Determine Email (URL → then Session Fallback) ---
    const params = new URLSearchParams(window.location.search);
    let userEmail = params.get("email");
    if (!userEmail && frappe.session.user !== "Guest") {
        userEmail = frappe.session.user;
    }

    // 5️⃣ --- Dashboard Redirect ---
    const dashboardLink = document.getElementById("guestDashboardLink");
    if (dashboardLink) {
        dashboardLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (userEmail) {
                const encodedEmail = encodeURIComponent(userEmail);
                window.location.href = `/guest-dashboard?email=${encodedEmail}`;
            } else {
                frappe.msgprint("⚠️ No email found in URL or session.");
            }
        });
    }

    // 6️⃣ --- Auto-Fill Resident ---
    if (frappe.session.user !== "Guest") {
        frappe.call({
            method: "frappe.client.get",
            args: { doctype: "Resident", filters: { user_id: frappe.session.user } },
            callback: (r) => {
                if (r.message) frappe.web_form.set_value("resident", r.message.name);
            },
        });
    }

    // 7️⃣ --- Logout ---
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function(e) {
            e.preventDefault();
            sessionStorage.removeItem("guest_email");
            frappe.msgprint("You have been logged out.");
            window.location.href = "/guest-login";
        });
    }

    // 8️⃣ --- Mobile Menu Toggle ---
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle) {
        menuToggle.addEventListener("click", () => {
            menuToggle.classList.toggle("active");
            navLinks.classList.toggle("show");
        });
    }

    // 9️⃣ --- After Save Confirmation ---
    frappe.web_form.on("after_save", () => {
        frappe.msgprint("✅ Your maintenance request has been submitted successfully!");
    });
});
