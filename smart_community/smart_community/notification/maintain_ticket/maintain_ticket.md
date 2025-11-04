<div style="font-family: Arial, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px; border-radius: 8px;">
  <div style="text-align:center; margin-bottom:10px;">
    <img src="/assets/smart_community/images/logo.png" alt="Smart Community Logo" style="height:50px;">
  </div>

  <h2 style="color:#007bff;">Your Maintenance Ticket Has Been Received</h2>

  <p>Dear {{ doc.resident }},</p>

  <p>We have successfully received your maintenance request and logged it into our system. Our support team will review and assign it shortly.</p>

  <h4>📋 <strong>Ticket Details</strong></h4>
  <table style="width:100%; border-collapse: collapse;">
    <tr><td style="padding:6px;"><strong>Issue Type:</strong></td><td>{{ doc.issue_type }}</td></tr>
    <tr><td style="padding:6px;"><strong>Description:</strong></td><td>{{ doc.description }}</td></tr>
    <tr><td style="padding:6px;"><strong>Priority:</strong></td><td>{{ doc.priority }}</td></tr>
    <tr><td style="padding:6px;"><strong>Status:</strong></td><td>{{ doc.status }}</td></tr>
  </table>

  <p>Thank you for reaching out. You’ll be notified as soon as your ticket is assigned and resolved.</p>

  <p style="margin-top:15px;">Warm regards,<br>
  <strong>Smart Community Maintenance Team</strong><br>
  📞 +91-XXXXXXXXXX<br>
  ✉️ support@smartcommunity.com</p>
</div>
