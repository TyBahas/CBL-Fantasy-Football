import nflgame
import nflgame.live
import os
import json
import random
import io
from sendtext import SendText


insults = ['Why did you even start this guy?', 
'This guy is a good argument for late-term abortion', 
'I cant believe you started him',
'I imagine we will see this guy on waivers this week',
'HAHAHAHAHA pathetic!',
'Your birth certificate is an apology letter from the condom factory.',
'You"re so ugly, when your mom dropped you off at school she got a fine for littering.',
"I wasn't born with enough middle fingers to let you know how I feel about you.",
'You wouldnt know a good fantasy team if it hit you in the tits.',
'You suck, you JACKASS!!',
'You are one pathetic loser',
'This guys sleeps in jeans',
'Heartbreaking',
'May as well chalk this week up as a loss',
'Oof, that was a gut-buster',
'Oopsie',
"He just pooed his jorts"
]

def vault_get_email_pass(keyword):
    """[Gets the username and password from vault.json file to send SMS]
    
    Arguments:
        keyword {[string]} -- [the key that corresponds to the value (username/password) that you want to retrieve]
    
    Returns:
        [string] -- [username/password value in json file]
    """
    pw_file_path = os.path.abspath("./vault.json")
    json_data = json.load(open(pw_file_path))
    return json_data['email'][keyword]


def sms_generation(player, turnover_type, phone_num, coach):
    if turnover_type == 'fum':
        string = 'fumble'
    elif turnover_type == 'int':
        string = 'interception'
    elif turnover_type == 'fg':
        string = 'missed FG'
    elif turnover_type == 'xp':
        string = 'missed XP'

    text_subject = player + ' ' + string + ' !!!!'
    text_content = insults[random.randint(0,len(insults)-1)]
    sms = SendText(
        email=vault_get_email_pass('username'),
        pas=vault_get_email_pass('password'),
        smsgateway=phone_num,
        text_subject=text_subject,
        text_content=text_content
        )
    sms.send()
    print text_subject + ": sent text to " + coach + " - " + text_content



def cb(active, completed, diffs):
    for game in active:
        # Remember, it is possible for an active game to have not started yet.
        # However, sometimes NFL.com provides some data before the game starts.
        # If you omit this check, things still work OK.
        if not game.playing():
            continue

        #print '%s vs. %s' % (game.home, game.away)
        directory = './players'
        jsonfilename = ''
        data = ''
        for files in os.listdir(directory):
            #reads json files
            with open(directory+'/'+files) as json_file:
                jsonfilename = json_file.name
                enemy_team = json.load(json_file)

                for x in enemy_team['fantasy_team']:

                    for p in game.players:
                        
                        if str(p) == enemy_team['fantasy_team'][x]['player'] and str(p.team) == enemy_team['fantasy_team'][x]['team']:
                            #checks for players matching the players in json files
                            
                            if int(p.fumbles_lost) > int(enemy_team['fantasy_team'][x]['fum']):
                                # if new fumble
                                sms_generation(player=enemy_team['fantasy_team'][x]['player'], turnover_type='fum', phone_num=enemy_team['phone'], coach=enemy_team['name'])
                                enemy_team['fantasy_team'][x]['fum'] += 1

                            elif int(p.passing_ints) >  int(enemy_team['fantasy_team'][x]['int']):
                                # if new interception
                                sms_generation(player=enemy_team['fantasy_team'][x]['player'], turnover_type='int', phone_num=enemy_team['phone'], coach=enemy_team['name'])
                                enemy_team['fantasy_team'][x]['int'] += 1

                            elif int(p.kicking_fgmissed) >  int(enemy_team['fantasy_team'][x]['kick']):
                                # if new missed kick
                                sms_generation(player=enemy_team['fantasy_team'][x]['player'], turnover_type='fg', phone_num=enemy_team['phone'], coach=enemy_team['name'])
                                enemy_team['fantasy_team'][x]['kick'] += 1

                            elif int(p.kicking_xpmissed) >  int(enemy_team['fantasy_team'][x]['xp_miss']):
                                # if new extra point kick
                                sms_generation(player=enemy_team['fantasy_team'][x]['player'], turnover_type='xp', phone_num=enemy_team['phone'], coach=enemy_team['name'])
                                enemy_team['fantasy_team'][x]['xp_miss'] += 1

                            else:
                                pass

            data = enemy_team
            json_file.close()  #closes the original file
            with io.open(jsonfilename, 'w', encoding='utf-8') as outfile:
                outfile.write(json.dumps(data, ensure_ascii=False))

nflgame.live.run(cb, active_interval=15)