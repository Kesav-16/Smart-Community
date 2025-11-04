<div style="font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #e8fff3, #f3fff7); color: #333; padding: 25px; border-radius: 12px; max-width: 600px; margin: auto; box-shadow: 0 0 20px rgba(0,0,0,0.08);">
  
  <!-- Header with Logo -->
  <!--<div style="text-align: center; margin-bottom: 15px;">-->
  <!--  <img src="/assets/smart_community/images/logo.png" alt="Smart Community Logo" style="height: 60px; border-radius: 8px;">-->
  <!--</div>-->

  <!-- Animated Header -->
  <h2 style="color: #28a745; text-align: center; background: linear-gradient(90deg, #00c851, #007e33); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px; margin-bottom: 10px;">
    ✅ Your Maintenance Ticket Has Been Resolved
  </h2>

  <!-- Greeting -->
  <p style="font-size: 16px; line-height: 1.6;">
    Dear <strong>{{ doc.resident }}</strong>,
  </p>

  <!-- Message -->
  <p style="font-size: 15px; line-height: 1.6; margin-bottom: 18px;">
    We’re happy to inform you that your maintenance request has been <strong>successfully resolved</strong>.  
    Please review the resolution details below.
  </p>

  <!-- Ticket Info Card -->
  <div style="background: #ffffff; border: 1px solid #c8eed5; border-radius: 10px; padding: 15px; box-shadow: 0 0 8px rgba(0, 200, 81, 0.1);">
    <h3 style="color: #28a745; border-bottom: 1px solid #e0e0e0; padding-bottom: 5px; margin-bottom: 10px;">
      📋 Ticket Summary
    </h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
      <tr>
        <td style="padding: 6px 0; font-weight: 600;">Issue Type:</td>
        <td>{{ doc.issue_type }}</td>
      </tr>
      <tr>
        <td style="padding: 6px 0; font-weight: 600;">Description:</td>
        <td>{{ doc.description }}</td>
      </tr>
      <tr>
        <td style="padding: 6px 0; font-weight: 600;">Priority:</td>
        <td>{{ doc.priority }}</td>
      </tr>
      <tr>
        <td style="padding: 6px 0; font-weight: 600;">Status:</td>
        <td><span style="background-color: #e8fff3; color: #007e33; padding: 4px 10px; border-radius: 6px;">{{ doc.status }}</span></td>
      </tr>
      <tr>
        <td style="padding: 6px 0; font-weight: 600;">Resolution Note:</td>
        <td>{{ doc.resolution_note or "N/A" }}</td>
      </tr>
    </table>
  </div>

  <!-- Footer Note -->
  <p style="font-size: 15px; line-height: 1.6; margin-top: 18px;">
    Thank you for your patience and cooperation.  
    If you have further issues, please don’t hesitate to submit another ticket.
  </p>

  <!-- Contact Info -->
  <div style="text-align: center; margin-top: 20px; font-size: 14px; color: #555;">
    <strong>Smart Community Maintenance Team</strong><br>
    📞 +91-74859654412 | ✉️ <a href="mailto:support@smartcommunity.com" style="color: #28a745; text-decoration: none;">support@smartcommunity.com</a><br>
    <span style="font-size: 13px; color: #999;">We’re glad to keep your community safe and comfortable!</span>
  </div>

</div>
