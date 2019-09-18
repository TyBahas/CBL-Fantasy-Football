import nflgame
from sendtext import SendText

#SentText test 
#sms = SendText(email='cfbtrashtalk@gmail.com',pas='columbusbeerleague',smsgateway='6145827473@vtext.com',text_subject='hello',text_content='But you already knew that \n \n \n' )
#sms.send()
'''
def cb(active, completed, diffs):
    for game in active:
        # Remember, it is possible for an active game to have not started yet.
        # However, sometimes NFL.com provides some data before the game starts.
        # If you omit this check, things still work OK.
        if not game.playing():
            continue

        print '%s vs. %s' % (game.home, game.away)
        for p in game.players.passing().sort("passing_yds"):
            print '\t%s %d %d %d %d %d' \
                    % (p, p.passing_cmp, p.passing_att,
                       p.passing_yds, p.passing_tds, p.passing_int)

nflgame.live.run(cb)       
'''                

import nflgame

games = nflgame.games(2016, week=3)
players = nflgame.combine_game_stats(games)
for p in players.passing().sort('rushing_yds'):
    msg = '%s %d carries for %d yards and %d TDs  %d'
    print msg % (p, p.rushing_att, p.rushing_yds, p.rushing_tds, p.passing_ints)