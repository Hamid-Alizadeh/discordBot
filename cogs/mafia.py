import json
import pickle

import discord
from discord.ext import commands, tasks
from threading import Timer
import random

god = []
lobby = game = dict()
role = {
    # 'Mafia': {'side': 1, 'Question': "Whom Do you want to kill ?",
    #           'picture':'https://www.industryglobalnews24.com/images/amidst-the-corona-virus-pandemic-the-italian-mafia-finds-opportunities-.jpeg'},
    'GodFather': {'side': 1, 'Question': "Whom Do you want to kill ?",
                  'picture': 'https://scrapsfromtheloft.com/wp-content/uploads/2017/09/The-Godfather-1972-Marlon-Brando-as-Don-Vito-Corleone.jpg'},
    'Detective': {'side': 0, 'Question': "Whom Do you want to heal ?",
                  'picture': 'https://compote.slate.com/images/1f76a990-6b45-415f-8693-c0fa2ad334f4.jpeg?width=780&height=520&rect=1620x1080&offset=153x0'},
    'Doctor': {'side': 0, 'Question': "Whom Do you want to know ?",
               'picture': 'https://www.thehealthy.com/wp-content/uploads/2017/09/02_doctor_Insider-Tips-to-Choosing-the-Best-Primary-Care-Doctor_519507367_Stokkete.jpg'},
    # 'Spy': {'side': 0, 'Question': "Whom Do you want to rob ?",
    #         'picture': 'https://i2-prod.mirror.co.uk/incoming/article9363091.ece/ALTERNATES/s615/3_Computer-Hacker.jpg'},
    # 'Robinhood': {'side': 0, 'Question': "Whom Do you want to shot ?",
    #               'picture':'https://images.markets.businessinsider.com/image/5dd7f372fd9db266dc27fab3-1200/errol-flynn-robin-hood.jpg'},
    # 'Citizen': {'side': 0, 'Question': "Whom Do you want to espionage ?",
    #             'picture': 'https://www.thelomaxfolkproject.com/images/lomax-group-mainpage.png'},
}
god_task = {'src_msg': '',
            'role': '',
            'target': ''
            }
live_ps = []
emoji_list = ['\U0001F1E6', '\U0001F1E7', '\U0001F1E8',
              '\U0001F1E9', '\U0001F1EA', '\U0001F1EB',
              '\U0001F1EC', '\U0001F1EF', '\U0001F1F0',
              '\U0001F1F1',
              '\U0001F1F2', '\U0001F1F3', '\U0001F1F4',
              '\U0001F1F5', '\U0001F1F6', '\U0001F1F7',
              '\U0001F1F8', '\U0001F1F9', '\U0001F1F0',
              '\U0001F1FA', '\U0001F1FB', '\U0001F1FC',
              '\U0001F1FD', '\U0001F1FE', '\U0001F1FF',
              ]


class Mafia(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mafia Cog is online.')

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     print('NewMessage from "{0.author}" in {0.channel} in {0.guild}\n {0.content}'.format(message))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global god
        global live_ps
        channel = reaction.message
        if user != self.client.user:
            print(len(god))
            for task in god:
                print(task)
                src = task['src_msg']
                print(str(src.id) + "\t" + str(channel.id))
                if src.id == channel.id:
                    for j in live_ps:
                        print(j[0] + str(reaction.emoji))
                        if j[0] == reaction.emoji:
                            task['target'] = j[1]
                            await user.send('{0} has reacted with {1.emoji} to {2}!'.format(user, reaction, j[1]))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('ping!')

    @commands.command()
    async def join(self, ctx):
        await ctx.send('Joine to kunet ?!')

    @commands.command()
    async def team(self, ctx, *, member: discord.Member = None):
        """ Join the lobby to start a game
        :param member:
        :param ctx: msg sender
        :return: lobby list
        """
        member = member or ctx.author

        global lobby
        list_players = []
        player = {'name': member,
                  "role": "Citizen",
                  "status": True,
                  "time": 120,
                  "side": 0}
        if len(lobby) == 0:
            # Lobby was empty. First entry'
            lobby.update({"player " + str(len(lobby) + 1): player})
        else:
            print('Number of players in Lobby: ' + str(len(lobby)))

            # Check Double registration
            for p_id, p_info in lobby.items():
                if member == p_info['name']:
                    print('Double registration')
                    return await ctx.send('{} has already joined the lobby'.format(member.display_name))

            lobby.update({"player " + str(len(lobby) + 1): player})
            print('lobby updated.')

        for key, value in lobby.items():
            list_players.append(str(value['name'].display_name))
            print(value['name'])

        # embed
        field_title = 'players(' + str(len(lobby)) + ")"
        field_value = '\n'.join(list_players)

        print('length of lobby:' + str(len(lobby)))
        await ctx.send(embed=creat_embed(title="welcome To shiraz",
                                         desc="People in the game lobby are listed below ",
                                         field_t=field_title,
                                         field_v=field_value))

    @commands.command()
    async def setup(self, ctx):
        total_player = len(lobby)
        global game
        # Create game channel

        # guild = ctx.message.guild
        # overwrites = {
        #     guild.default_role: discord.PermissionOverwrite(read_messages=True),
        #     guild.me: discord.PermissionOverwrite(read_messages=True)
        # }
        # room = await guild.create_text_channel('RunningGame', overwrites=overwrites)
        # print(room.id)

        # create an list to random       from keys in   role   dict

        role_pool = list(role.keys())
        print(role_pool)

        # Check enough players
        if total_player >= 1:
            for key, value in lobby.items():
                # Assign random role and remove from list

                dedicated_role = random.choice(role_pool)
                value['role'] = dedicated_role
                role_pool.remove(dedicated_role)

                # Get user obj and create embed
                user = value['name']
                embed = discord.Embed(
                    title='You are ' + value['role'],
                    colour=discord.Colour.green()
                )
                embed.set_footer(text='این روبات در مرجله تخمی بودن به سر میبرد')
                embed.set_thumbnail(url='https://image.flaticon.com/icons/svg/381/381801.svg')
                embed.set_author(name='Role Assignment',
                                 icon_url='')
                print(value['role'] + ' -----> ' + str(user))
                # find embed pic value from role obj
                for role_key, role_value in role.items():
                    if role_key == dedicated_role:
                        embed.set_image(url=role_value['picture'])
                        await user.send(embed=embed)
                        # await room.send('@'+str(user))
            await ctx.send(
                'Naghsh haru pachidam beyn ' + str(total_player) + ' hatrun\nLotfan be chanelle "game" morajeE konid.')
            # send assigned lobby to game
            game = {'game': lobby,
                    'run': False,
                    'nights': 0,
                    'room': 'room',
                    'vote': 0}
        else:
            await ctx.send('kamid.')

    @commands.command()
    async def start(self, ctx):
        global game
        try:
            print(len(game))
            if not game["run"]:
                game["run"] = True
                result = "game has been started."
            else:
                result = "Already started"
            await ctx.send(result)
        except Exception as e:
            print(e)

    @commands.command()
    async def night(self, ctx):
        global game
        global lobby
        global god
        global live_ps
        # Create list of alive players and sign for poll
        i = 0
        for key, player in lobby.items():
            if player['status']:
                live_ps.append([emoji_list[i], str(player['name'].display_name)])
                i = i + 1
                print('emoji list created')

        # If game is running ,start night and send msg to power users

        if game["run"]:
            game["nights"] += 1
            print(lobby)
            for key, player in lobby.items():
                # If Player is alive , check what he wants

                if player['status']:
                    player_object = player['name']
                    print(str(player['name']) + "--" + str(player['role']))

                    # Check Power and Send Message with Reactions
                    for role_key, role_value in role.items():
                        if role_key == player['role']:

                            question = str(role_value['Question'])
                            print_l = list(map(' : '.join, live_ps))
                            src_msg = await player_object.send(question +
                                                               "\n like target's emoji :\n" + '\n'.join(print_l))

                            god.append({'src_msg': src_msg,
                                        'role': player['role'],
                                        'target': ''
                                        })
                            for i in live_ps:
                                kak = src_msg.channel
                                print('Looking to add reactions appropriate to role id : {}'.format(kak.recipient))
                                await src_msg.add_reaction(i[0])
                            await player_object.send("show mishavad shab shomare {}".format(game["nights"]))

            await ctx.send("People with powers check their DirectMassege")
            # Start a timer to check the reactions.
        t = Timer(15.0, check_result)
        t.start()

    @commands.command()
    async def showcity(self, ctx):
        global role
        embed = discord.Embed(
            title='List players',
            description="There are " + str(len(lobby)) + " player in the game.",
            colour=discord.Colour.blue()
        )
        embed.set_thumbnail(
            url='https://www.pngrepo.com/png/49762/180/city-hall.png')
        for p_id, p_info in lobby.items():
            player = str(p_info['name'])
            role = str(p_info['role']) + "=" + str(p_info['status'])
            embed.add_field(name=player, value=role, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def savel(self, ctx):
        global lobby
        print(lobby)
        with open('data.json', 'w') as fp:
            json.dump(lobby, fp)
        print("list saved")

    @commands.command()
    async def loads(self, ctx):
        global lobby
        with open('data.json', 'r') as fp:
            data = json.load(fp)
        print(data)


def check_result():
    global god
    print('runing check result')
    print(god)
    result = []
    for item in god:
        # Check role and action
        # GodFather

        if item['role'] == 'GodFather':
            for key_lobby, player in lobby.items():
                if player['name'].name == item['target']:
                    player['status'] = 0
                    result.append(str(player['name']) + " Died")

        if item['role'] == 'Doctor':
            for key_lobby, player in lobby.items():
                if player['name'].name == item['target']:
                    player['status'] = 1
                    result.append(str(player['name']) + " healed")

        if item['role'] == 'Detective':
            for key_lobby, player in lobby.items():
                if player['name'].name == item['target']:
                    result.append(str(player['name']) + " spionaged")
    print("result :" + str(result))


def creat_embed(title, desc, field_t, field_v):
    embed = discord.Embed(
        title=title,
        description=desc,
        colour=discord.Colour.blue()

    )
    embed.set_footer(text='Mafia bot is written in Python')
    # embed.set_image(url='https://i.ytimg.com/vi/ml175ol650o/maxresdefault.jpg')
    embed.set_thumbnail(url='https://image.flaticon.com/icons/png/512/2099/premium/2099872.png')
    # embed.set_author(name='پروردگار',
    #                  icon_url='')
    embed.add_field(name=field_t, value=field_v, inline=True)
    print('length of lobby:' + str(len(lobby)))
    return embed


def setup(client):
    client.add_cog(Mafia(client))
