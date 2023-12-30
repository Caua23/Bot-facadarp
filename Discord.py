import discord
from discord.ext import tasks, commands
from discord import app_commands
import aiohttp
import requests
import random
# Configurações do bot
TOKEN_DISCORD = '#'
TOKEN_TWITCH = '#'
CANAL_DISCORD_ID = 
NOME_STREAMER = '#'  # Substitua pelo nome do streamer desejado
TOKEN_DO_LUCAS = '#'
client_id = '#'
client_secret = '#'
id_do_servidor =
# Código de autenticação do Twitch
auth_params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials',
}

auth_url = 'https://id.twitch.tv/oauth2/token'
response = requests.post(auth_url, params=auth_params)

if response.status_code == 200:
    access_token = response.json().get('access_token', '')
    print(f'Token de Acesso: {access_token}')
else:
    print(f'Falha ao obter o Token de Acesso. Código de status: {response.status_code}')

# Crie a instância do cliente Discord
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Fizemos login como {client.user}')
    # Inicie a tarefa para monitorar os streams da Twitch
    check_streams.start()


@tasks.loop(seconds=300, count=1)  # Verifique apenas uma vez após 5 minutos
async def check_streams():
    try:
        headers = {'Client-ID': client_id, 'Authorization': f'Bearer {access_token}'}
        params = {'login': NOME_STREAMER}

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.twitch.tv/helix/users', headers=headers, params=params) as resp:
                user_data = await resp.json()

        if 'data' in user_data and user_data['data']:
            user_id = user_data['data'][0]['id']

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.twitch.tv/helix/streams?user_id={user_id}', headers=headers) as resp:
                    stream_data = await resp.json()

            if 'data' in stream_data and stream_data['data']:
                # O stream está online, enviar mensagem apenas se não foi enviado antes
                if not check_streams.has_sent_message:
                    channel = client.get_channel(CANAL_DISCORD_ID)
                    await channel.send(
                        f'O streamer {NOME_STREAMER} está ao vivo! Assista em: https://www.twitch.tv/{NOME_STREAMER} ||@everyone||')

                    # Enviar mensagem direta para o usuário com o ID TOKEN_DO_Inimigo
                    user = await client.fetch_user(int(TOKEN_DO_LUCAS))
                    if user:
                        await user.send(
                            f'Eu te disse que estaria aqui não é mesmo?? Live do {NOME_STREAMER} está on, Assista em: https://www.twitch.tv/{NOME_STREAMER}. Não duvide de mim, ok??')

                check_streams.has_sent_message = True
            else:
                # O stream está offline, resetar a flag
                check_streams.has_sent_message = False
    except Exception as e:
        print(f'Erro ao verificar o stream: {e}')

check_streams.has_sent_message = False

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados
            await tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = MyClient()
tree = app_commands.CommandTree(aclient)

@tree.command(guild=discord.Object(id=id_do_servidor), name='facada_esta_online', description='verifica se o facada esta online')

async def slash_online(interaction: discord.Interaction):
    try:
        headers = {'Client-ID': client_id, 'Authorization': f'Bearer {access_token}'}
        params = {'login': NOME_STREAMER}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.twitch.tv/helix/users', headers=headers, params=params) as resp:
                user_data = await resp.json()

        if 'data' in user_data and user_data['data']:
            user_id = user_data['data'][0]['id']

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.twitch.tv/helix/streams?user_id={user_id}', headers=headers) as resp:
                    stream_data = await resp.json()

            if 'data' in stream_data and stream_data['data']:
                await interaction.response.send_message(f'O {NOME_STREAMER} está em live! Assista em: https://www.twitch.tv/{NOME_STREAMER} ||{interaction.user.mention}||', ephemeral=True)

            else:
                await interaction.response.send_message(f'O {NOME_STREAMER} não está em live no momento.', ephemeral=True)
    except Exception as e:
        print(f'Erro ao verificar o stream: {e}'),

@tree.command(guild=discord.Object(id=id_do_servidor), name='sorteie_um_hl', description='vai sortiar um hl facada aleatoria')
async def slash_sorteie_hl(interaction: discord.Interaction):
        
        numero_girado = random.randint(1, 39)
        Videos = [
            
            'https://www.youtube.com/watch?v=icNtYKx_M4U&t=2s'
            
        ]

        if 1 <= numero_girado <=len(Videos):
            video_selecionado = Videos[numero_girado - 1]
            await interaction.response.send_message(f'O Hl escolhido Foi {video_selecionado} o Facada é superior no Game')

        else:
            await interaction.response.send_message('Erro: Número fora da faixa permitida, Gire denovo.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='frase_do', description='ele fala uma frase aleatoria do facada')
async def slash_frase(interaction: discord.Interaction):
    numero_giradoFrase = random.randint(1, 10)
    Frases = [
            'Frases Aqui'
        ]
    if 1 <= numero_giradoFrase <=len(Frases):
        Frase_selecionada = Frases[numero_giradoFrase - 1]
        await interaction.response.send_message(f'{Frase_selecionada}')
    else:
        await interaction.response.send_message('Erro: Número fora da faixa permitida, Gire denovo.', ephemeral=True)

    
# Substitua 'SEU_TOKEN_DO_DISCORD' pelo token real do seu bot do Discord
aclient.run(TOKEN_DISCORD)