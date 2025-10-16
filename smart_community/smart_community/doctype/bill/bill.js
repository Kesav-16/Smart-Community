frappe.ui.form.on('Bill', {
    before_save(frm) {
        showDynamicProgressOverlay();
    },
    after_save(frm) {
        hideDynamicProgressOverlay();
    }
});

frappe.realtime.on('bill_progress', function(data) {
    updateDynamicProgressOverlay(data.percent, data.message);
});

frappe.realtime.on('bill_complete', function(data) {
    updateDynamicProgressOverlay(100, "✅ " + data.message);
    setTimeout(() => hideDynamicProgressOverlay(), 1500);
});
function showDynamicProgressOverlay() {
    if (document.getElementById("bill-progress-overlay")) return;

    const overlay = document.createElement("div");
    overlay.id = "bill-progress-overlay";
    overlay.innerHTML = `
        <div id="progress-content" style="
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.75);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            z-index: 9999;
            font-family: 'Segoe UI', sans-serif;
        ">
            <h2 id="progress-title" style="font-size: 22px; margin-bottom: 15px;">Saving your Bill...</h2>
            <div style="width: 60%; background: #333; border-radius: 25px; overflow: hidden;">
                <div id="progress-bar" style="
                    width: 0%; height: 20px;
                    background: linear-gradient(90deg, #50e3c2, #4a90e2);
                    transition: width 0.5s ease;
                "></div>
            </div>
            <p id="progress-msg" style="margin-top: 12px; font-size: 14px; color: #ddd;">Starting...</p>
            <div id="progress-spinner" style="margin-top:20px; border:4px solid #555; border-top:4px solid #50e3c2; border-radius:50%; width:40px; height:40px; animation:spin 1s linear infinite;"></div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
    document.body.appendChild(overlay);
}

function updateDynamicProgressOverlay(percent, message) {
    const bar = document.getElementById("progress-bar");
    const msg = document.getElementById("progress-msg");
    const title = document.getElementById("progress-title");
    if (bar) bar.style.width = percent + "%";
    if (msg) msg.innerText = message || "";
    if (title) title.innerText = percent < 100 ? "Processing Bill..." : "Completed!";
}

function hideDynamicProgressOverlay() {
    const overlay = document.getElementById("bill-progress-overlay");
    if (overlay) {
        overlay.style.opacity = "0";
        overlay.style.transition = "opacity 0.5s ease";
        setTimeout(() => overlay.remove(), 500);
    }
}
