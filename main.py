import pandas as pd
from flask import Flask, render_template, jsonify
from sleeperpy import User
from sleeperpy import Drafts
from sleeperpy import Leagues
from sleeperpy import Avatars

app = Flask(__name__)

#real draft:
draft_id = 1120557302983110657

#mock draft:
#draft_id = x

csv_file = "astro_df.csv"
def get_csv_data(player_id):
    df = pd.read_csv(csv_file)
    return df[df["sleeper_id"] == int(player_id)][['sun.sign','sun.emoji','sun.element','chart']]


@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/recent_pick')
def get_recent_pick():
    picks = Drafts.get_all_picks_in_draft(draft_id)
    recent_pick = picks[-1] if picks else None
    if recent_pick:
        #get athlete information
        player_name = recent_pick['metadata']['first_name'] + ' ' + recent_pick['metadata']['last_name']
        team_name = recent_pick['metadata']['team']
        position = recent_pick['metadata']['position']
        round = recent_pick['round']
        pick_no = recent_pick['pick_no']

        #get owner name, avatar, and other 
        owner_id = recent_pick['picked_by']
        owner = User.get_user(owner_id)
        if owner_id:
            owner_name = owner['display_name']
            avatar_id = owner['avatar']
        else: #if the user doesn't exist, just for testing league drafts with bots
            owner_name = 'null'
            avatar_id = 'null'
        csv_data = get_csv_data(player_id)
        if csv_data:
            sun_sign = csv_data['sun.sign']
            sun_element = csv_data['sun.element']
            sun_sign_emoji = csv_data['sun.emoji']
            chart = csv_data['chart']
        else:
            sun_sign = 'null'
            sun_element = 'null'
            sun_sign_emoji = 'null'
            chart = 'null'
        
    else:
        player_name = "No recent pick"
        team_name = ""

    return jsonify({
        'player_name': player_name,
        'team_name': team_name,
        'position' : position,
        'round' : round,
        'pick_no': pick_no, 
        'owner_name': owner_name,
        'avatar_id': avatar_id,
        'player_id': player_id,
        'sun_sign': sun_sign,
        'sun_element': sun_element,
        'sun_sign_emoji': sun_emoji,
        'chart': chart
    })

if __name__ == '__main__':
    app.run(debug=True)
