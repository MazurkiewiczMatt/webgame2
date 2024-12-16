from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from .authentication import signup, login, logout
from .characters_management import character_sheet, create_character, load_characters, save_characters

def update_function():
    characters = load_characters()
    for character in characters.keys():
        if "age" in characters[character].keys():
            characters[character]["age"] += 1
        else:
            characters[character]["age"] = 1
    save_characters(characters)

# Flask app creation
def create_app(registered_users=None, active_sessions=None):
    app = Flask(__name__, template_folder='/home/Mazurkiewicz/webgame/webgame2/templates/')

    # Initialize the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_function, 'cron', hour="0-23", minute="*")  # Run every minute
    scheduler.start()

    @app.route('/')
    def main_app():
        active_players = list(active_sessions.keys())
        registered_users_list = list(registered_users.keys())
        return render_template('main_page.html', active_players=active_players, registered_users=registered_users_list)

    @app.route('/signup', methods=['POST'])
    def signup_endpoint():
        return signup(registered_users)

    @app.route('/login', methods=['POST'])
    def login_endpoint():
        return login(registered_users, active_sessions)

    @app.route('/logout', methods=['POST'])
    def logout_endpoint():
        return logout(active_sessions)

    @app.route('/character_sheet', methods=['POST'])
    def character_sheet_endpoint():
        return character_sheet(active_sessions)

    @app.route('/create_character', methods=['POST'])
    def create_character_endpoint():
        return create_character(active_sessions)

    # Ensure scheduler shuts down when the app is stopped
    @app.before_first_request
    def start_scheduler():
        if not scheduler.running:
            scheduler.start()

    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        scheduler.shutdown(wait=False)

    return app
