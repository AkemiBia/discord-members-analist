import discord
import sqlite3
from discord.ext import commands

# Configuração do bot
intents = discord.Intents.default()
intents.members = True  # Permite acesso à lista de membros
intents.presences = True  # Permite acessar status online
bot = commands.Bot(command_prefix="!", intents=intents)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("membros.db")
cursor = conn.cursor()

# Criar tabela para armazenar informações dos membros (com campo bio)
cursor.execute('''CREATE TABLE IF NOT EXISTS membros (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    apelido TEXT,
                    avatar TEXT,
                    status TEXT,
                    atividade TEXT,
                    cargos TEXT,
                    data_entrada TEXT,
                    data_criacao TEXT,
                    bio TEXT)''')
conn.commit()

# Comando para analisar e salvar os membros no banco
@bot.command()
async def analisar(ctx):
    guild = ctx.guild
    for member in guild.members:
        if not member.bot:  # Ignorar bots
            nome = member.name
            apelido = member.nick if member.nick else "Sem apelido"
            avatar = member.avatar if isinstance(member.avatar, str) else "Sem avatar"  # Verifica se é uma string
            status = str(member.status)  # online, offline, dnd, idle
            atividade = member.activity.name if member.activity else "Nenhuma"
            cargos = ", ".join([role.name for role in member.roles if role.name != "@everyone"])
            data_entrada = member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Desconhecida"
            data_criacao = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
            bio = "Sem bio"  # Bio inicial vazia

            # Salvar no banco de dados
            cursor.execute("INSERT OR REPLACE INTO membros (id, nome, apelido, avatar, status, atividade, cargos, data_entrada, data_criacao, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (member.id, nome, apelido, avatar, status, atividade, cargos, data_entrada, data_criacao, bio))
            conn.commit()
            print(f"Salvo: {nome} ({apelido})")

    await ctx.send("Análise concluída! Dados salvos no banco.")


# Evento para salvar novos membros automaticamente
@bot.event
async def on_member_join(member):
    nome = member.name
    apelido = member.nick if member.nick else "Sem apelido"
    avatar = member.avatar_url if member.avatar else "Sem avatar"
    status = str(member.status)
    atividade = member.activity.name if member.activity else "Nenhuma"
    cargos = ", ".join([role.name for role in member.roles if role.name != "@everyone"])
    data_entrada = member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Desconhecida"
    data_criacao = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
    bio = "Sem bio"

    # Salvar no banco de dados
    cursor.execute("INSERT OR REPLACE INTO membros (id, nome, apelido, avatar, status, atividade, cargos, data_entrada, data_criacao, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (member.id, nome, apelido, avatar, status, atividade, cargos, data_entrada, data_criacao, bio))
    conn.commit()
    print(f"Novo membro salvo: {nome} ({apelido})")

# Comando para os membros definirem suas próprias bios
@bot.command()
async def set_bio(ctx, *, bio):
    cursor.execute("UPDATE membros SET bio = ? WHERE id = ?", (bio, ctx.author.id))
    conn.commit()
    await ctx.send(f"Bio de {ctx.author.name} atualizada!")

# Comando para consultar um perfil salvo
@bot.command()
async def perfil(ctx, membro: discord.Member = None):
    membro = membro or ctx.author  # Se nenhum membro for especificado, mostra o perfil do próprio usuário
    cursor.execute("SELECT nome, apelido, avatar, status, atividade, cargos, data_entrada, data_criacao, bio FROM membros WHERE id = ?", (membro.id,))
    dados = cursor.fetchone()

    if dados:
        nome, apelido, avatar, status, atividade, cargos, data_entrada, data_criacao, bio = dados
        embed = discord.Embed(title=f"Perfil de {nome}", color=discord.Color.blue())
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Apelido", value=apelido, inline=True)
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Atividade", value=atividade, inline=True)
        embed.add_field(name="Cargos", value=cargos if cargos else "Nenhum", inline=False)
        embed.add_field(name="Entrou no servidor", value=data_entrada, inline=True)
        embed.add_field(name="Conta criada em", value=data_criacao, inline=True)
        embed.add_field(name="Bio", value=bio, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Perfil não encontrado!")

bot.run("token")
