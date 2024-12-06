from flask import render_template

def main_page(active_sessions):
    active_players = list(active_sessions.keys())
    return render_template('main_page.html', active_players=active_players)