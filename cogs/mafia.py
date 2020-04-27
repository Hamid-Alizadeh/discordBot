import discord
from discord.ext import commands, tasks
from threading import Timer
import random

lobby = game = god = dict()
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

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('ping!')

    @commands.command()
    async def join(self, ctx):
        await ctx.send('Joinr to kunet ?!')

    @commands.command()
    async def team(self, ctx):
        global lobby
        embed = discord.Embed(
            title='به شیراز خوش امدید',
            description="به شهر گشاد شیراز خوش امدید",
            colour=discord.Colour.blue()

        )
        embed.set_footer(text='این روبات در مرجله تخمی بودن به سر میبرد')
        # embed.set_image(url='https://i.ytimg.com/vi/ml175ol650o/maxresdefault.jpg')
        embed.set_thumbnail(url='https://image.flaticon.com/icons/png/512/2099/premium/2099872.png')
        # embed.set_author(name='پروردگار',
        #                  icon_url='')
        total_player = len(lobby)
        list_players = []
        player = {'name': ctx.author,
                  "role": "Citizen",
                  "status": True,
                  "time": 120,
                  "side": 0}
        if total_player == 0:
            print('Lobby was empty. First entry')
            lobby.update({"player " + str(total_player+1): player})
        else:
            print('Number of players in Lobby: ' + str(total_player))
            for p_id, p_info in lobby.items():
                if ctx.author == p_info['name']:
                    print('double registration')
                    await ctx.send('درخواست شهروندی ' + str(ctx.author) + ' قبلا ثبت شده')
                    return

            lobby.update({"player " + str(total_player+1): player})
            print('lobby updated.')

        total_player = len(lobby)
        for key, value in lobby.items():
            list_players.append(str(value['name']))
            print(value['name'])

        embed.add_field(name='players(' + str(total_player) + ")", value='\n'.join(list_players), inline=True)
        print('length of lobby:' + str(len(lobby)))
        await ctx.send(embed=embed)

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
                embed.set_author(name='خدا',
                                 icon_url='')
                print(value['role'] + ' -----> ' + str(user))
                # find embed pic value from role obj
                for role_key, role_value in role.items():
                    if role_key == dedicated_role:
                        embed.set_image(url=role_value['picture'])
                        await user.send(embed=embed)
                        # await room.send('@'+str(user))
            await ctx.send('Naghsh haru pachidam beyn ' + str(total_player) + ' hatrun\nLotfan be chanelle "game" morajeE konid.')
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
        if not game["run"]:
            game["run"] = True
            result = "game has been started."
        else:
            result = "Already started"
        await ctx.send(result)

    @commands.command()
    async def night(self, ctx):
        global game
        global lobby
        global god_task
        global god
        live_ps = []

        # Create list of alive players and sign for poll
        i = 0
        for key, player in lobby.items():
            if player['status'] == 1:
                live_ps.append([emoji_list[i], str(player['name'])])
                i = i + 1

        # If game is running ,start night and send msg to power users

        if not game["run"]:
            game["nights"] += 1
            for key, player in lobby.items():

                # If Player is alive , check what he wants

                if player['status'] == 1:
                    player_object = player['name']
                    print(str(player['name']) + "--" + str(player['role']))
                    j = 0

                    # Check Power and Send Message with Reactions

                    for role_key, role_value in role.items():
                        if role_key == player['role']:
                            j = j + 1
                            question = str(role_value['Question'])
                            print_l = list(map(' : '.join, live_ps))
                            src_msg = await player_object.send(question +
                                                               "\n like target's emoji :\n" + '\n'.join(print_l))
                            god_task['src_msg'] = src_msg
                            god_task['role'] = player['role']
                            god_task['target'] = player['name']
                            god = {j: god_task}
                            print('Looping to add reactions appropriate to role')

                            for i in live_ps:
                                await src_msg.add_reaction(i[0])

            await ctx.send("People with powers check their DirectMassege")
            # Start a timer to check the reactions.
            # t = Timer(10.0, check_result)
            # t.start()
            await src_msg.send("show mishavad {}")

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
            role = str(p_info['role'])
            embed.add_field(name=player, value=role, inline=False)
        await ctx.send(embed=embed)


def check_result(reaction, user):
    global god
    print('runing check result')
    print(str(reaction) + "HHHHHH " + str(user))
    result = []
    for key, role_value in god.items():
        # Check role and action
        # GodFather
        if role_value['role'] == 'GodFather':
            for key_lobby, player in lobby.items():
                if player['name'] == role_value['target']:
                    player['status'] = 0
                    result.append(str(player['name']))

        if role_value['role'] == 'Doctor':
            for key_lobby, player in lobby.items():
                if player['name'] == role_value['target']:
                    player['status'] = 1
                    result.append(str(player['name']))

        if role_value['role'] == 'Detective':
            for key_lobby, player in lobby.items():
                if player['name'] == role_value['target']:
                    result.append(str(player['name']))
    print(result)
    return True



def setup(client):
    client.add_cog(Mafia(client))


