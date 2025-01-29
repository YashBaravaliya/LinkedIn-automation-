from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from src.config import Config
from src.services.linkedin_service import LinkedInService
from src.services.calendar_service import GoogleCalendarManager
from src.services.post_generator import PostGenerator
from src.services.whatsapp import WhatsAppService
from datetime import datetime, timedelta
import json
from datetime import datetime

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

linkedin_service = LinkedInService(Config.LINKEDIN_ACCESS_TOKEN)
calendar_service = GoogleCalendarManager()
post_generator = PostGenerator(Config.MISTRAL_API_KEY)
whatsapp_service = WhatsAppService(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
whatsapp_to_number = Config.WHATSAPP_TO_NUMBER

def generate_and_save_draft():
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().date().isoformat()
    # Fetch next holiday
    events = calendar_service.fetch_indian_festival()
    if not events:
        return {"status": "No upcoming festival found"}
    
    # Generate post content
    result = json.loads(events)
    result = result["events"]
    result = result[0]
    date_of_event = result["start_date"]
    print(f"today: {today}, date_of_event: {date_of_event}")
    
    if today != date_of_event:
        return {"status": "there is no festival today"}
    else:
        post_content = post_generator.generate_post(result["title"])
        whatsapp_service.sand_message(whatsapp_to_number, f"Today is {result['title']}. Please check your LinkedIn account for the post.")
    
    # Create LinkedIn draft
    response = linkedin_service.create_draft(post_content)
    
    if response.status_code == 201:
        return {"status": "success", "message": "Draft created successfully"}
    else:
        return {"status": "error", "message": f"Failed to create draft: {response.json()}"}

@app.route('/generate-post', methods=['GET'])
def manual_generate():
    result = generate_and_save_draft()
    return jsonify(result)

# Schedule the job to run daily at 10 AM
@scheduler.task('cron', id='daily_post_check', hour=9,minute=0)
def scheduled_post_check():
    print("Checking for upcoming  festivals...")
    generate_and_save_draft()

if __name__ == '__main__':
    app.run(debug=True)