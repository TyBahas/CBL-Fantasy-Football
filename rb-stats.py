import nflgame
import nflgame.live
import os
import json
import random
import io
from sendtext import SendText

'''
game = nflgame.games(2019, week=2)
players = nflgame.combine_game_stats(game)

for x in enemy_team:
    for p in players:
        if str(p) == enemy_team[x]['player'] and str(p.team) == enemy_team[x]['team']:
            print p, p.team, p.fumbles_lost, p.kicking_fg_missed, p.passing_int
'''


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
                                text_subject = enemy_team['fantasy_team'][x]['player'] + ' fumble!!!!'
                                text_content = insults[random.randint(0,len(insults)-1)]
                                enemy_team['fantasy_team'][x]['fum'] += 1
                                sms = SendText(email='cfbtrashtalk@gmail.com',
                                    pas='columbusbeerleague',
                                    #smsgateway='6149465257@vtext.com',
                                    smsgateway=enemy_team['phone'],
                                    text_subject=text_subject,
                                    text_content=text_content)
                                sms.send()
                                print text_subject + ": sent text to " + enemy_team['name'] + " - " + text_content
                            
                            elif int(p.passing_ints) >  int(enemy_team['fantasy_team'][x]['int']):
                                # if new interception
                                text_subject =  enemy_team['fantasy_team'][x]['player'] + ' interception!!!!'
                                text_content = insults[random.randint(0,len(insults)-1)]
                                enemy_team['fantasy_team'][x]['int'] += 1
                                sms = SendText(email='cfbtrashtalk@gmail.com',
                                    pas='columbusbeerleague',
                                    #smsgateway='6149465257@vtext.com',
                                    smsgateway=enemy_team['phone'],
                                    text_subject=text_subject,
                                    text_content=text_content)
                                sms.send()
                                print text_subject + ": sent text to " + enemy_team['name'] + " - " + text_content

                            elif int(p.kicking_fgmissed) >  int(enemy_team['fantasy_team'][x]['kick']):
                                # if new missed kick
                                text_subject = enemy_team['fantasy_team'][x]['player'] + ' missed the kick!!!!'
                                text_content = insults[random.randint(0,len(insults)-1)]
                                enemy_team['fantasy_team'][x]['kick'] += 1
                                sms = SendText(email='cfbtrashtalk@gmail.com',
                                    pas='columbusbeerleague',
                                    #smsgateway='6149465257@vtext.com',
                                    smsgateway=enemy_team['phone'],
                                    text_subject=text_subject,
                                    text_content=text_content)
                                sms.send()
                                print text_subject + ": sent text to " + enemy_team['name'] + " - " + text_content

                            elif int(p.kicking_xpmissed) >  int(enemy_team['fantasy_team'][x]['xp_miss']):
                                # if new extra point kick
                                text_subject = enemy_team['fantasy_team'][x]['player'] + ' missed the XP kick!!!!'
                                text_content = insults[random.randint(0,len(insults)-1)]
                                enemy_team['fantasy_team'][x]['xp_miss'] += 1
                                sms = SendText(email='cfbtrashtalk@gmail.com',
                                    pas='columbusbeerleague',
                                    #smsgateway='6149465257@vtext.com',
                                    smsgateway=enemy_team['phone'],
                                    text_subject=text_subject,
                                    text_content=text_content)
                                sms.send()
                                print text_subject + ": sent text to " + enemy_team['name'] + " - " + text_content

                            else:
                                pass
            data = enemy_team
            json_file.close()  #closes the original file
            with io.open(jsonfilename, 'w', encoding='utf-8') as outfile:
                outfile.write(json.dumps(data, ensure_ascii=False))

nflgame.live.run(cb, active_interval=15)