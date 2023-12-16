# -*- coding: utf-8 -*-
import pandas as pd
import os


diret = '/musicassdcard.csv'
pontovirg = ';' 
lista = ['File Extension', 'Artistas participantes', 'Álbum', 'Tamanho', 'Artista do Álbum']


base = pd.read_csv(diret, sep=pontovirg).fillna('')

basesemtitulo = base[base['Título'] == '']                 
basesemtitulo = basesemtitulo.drop(columns = lista).reset_index().drop(columns = 'index')
nome = basesemtitulo['Name']
nome = nome.str.replace('.mp3','')

#Criando uma base temporaria com nomes que contém digito 0
nome_num = nome[nome.str.contains('0')==True].reset_index().drop(columns = 'index')  
nome_num = nome_num.drop([11,12]).squeeze()
nome_num = nome_num.str.slice(3)
nome_num[0] = nome_num.str.slice(2)[0]
nome_num[3] = nome_num.str.slice(2)[3]
nome_num[0] = nome_num.str.slice(0,18)[0]
nome_num[3] = nome_num.str.slice(0,13)[3]

#Associando os dados filtrados de volta a base original
i = 0
for n in nome_num:
    for i in (0, len(nome_num) - 1):
        if n == nome_num[4]:
            base['Título'][19] = n
        indice = base[base['Name'].str.contains(n)==True].index
        base['Título'][indice] = n
        
    i = i + 1
    
#Voltando com a base sem título agora atualizada
basesemtitulo = base[base['Título'] == '']                 
basesemtitulo = basesemtitulo.drop(columns = lista).reset_index().drop(columns = 'index')
nome = basesemtitulo['Name']
nome = nome.str.replace('.mp3','')
nome = nome.str.split("-", expand=True)  
nome = nome.rename(columns={0: 'Artista', 1: 'Titulo'})   
nome['Artista'] [0] = nome['Artista'].str.slice(-7)[0]
nome['Artista'][4], nome['Titulo'][4] = nome['Titulo'][4], nome['Artista'][4]
nome['Artista'][32], nome['Titulo'][32] = nome['Titulo'][32], nome['Artista'][32]
nome['Artista'][33], nome['Titulo'][33] =  'Led Zeppelin', nome['Artista'][33]
nome['Titulo'] = nome['Titulo'].fillna('')
nome['Artista'][22], nome['Titulo'][22] = nome['Artista'][22][0:30], nome['Artista'][22][32:50]
nome['Artista'][13], nome['Titulo'][13] = nome['Artista'][13][21:29], nome['Artista'][13][0:20]
nome['Artista'] = nome['Artista'].str.strip()
nome['Titulo'] = nome['Titulo'].str.strip()


#Associando os dados filtrados de volta a base original
basesemtitulo['Título'] = nome['Titulo']
basesemtitulo['Artista'] = nome['Artista']

base_copia = base
base_copia['Cod'] = ''

idx = list(base_copia["Título"][base_copia['Título']==''].index)
j = 0
for j in range(0,37):
    idc = idx[j]
    base_copia["Título"][idc] = basesemtitulo['Título'][j]
    base_copia["Artistas participantes"][idc] = basesemtitulo['Artista'][j]
    j = j + 1

j = 0


bancotitulos = base_copia[['Name','Título']][base_copia['Título'].str.contains('-')]
#Tratando os dados que possuem mais de um - no nome dos títulos
while j < 3:
    for n in bancotitulos['Título']:
        if '--' in n:                
            m = n.replace('--','-')
            bancotitulos['Título'].loc[bancotitulos['Título'] == n] = m
            
        elif n.count('-') > 2:
            m = n.replace('D-Block & S-Te-Fan', 'DBlock & STeFan')
            bancotitulos['Título'].loc[bancotitulos['Título'] == n] = m
            m = n.replace('D-Block & S-te-Fan', 'DBlock & STeFan')
            bancotitulos['Título'].loc[bancotitulos['Título'] == n] = m
            m = n.replace('Black-Eyed', 'Black Eyed')
            bancotitulos['Título'].loc[bancotitulos['Título'] == n] = m
        elif n.count('-') >= 2:
            if n[0] == 'B':
                b = n.replace('(inkl. Songtext)', '')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = b
                b = n.replace('-2)', ')')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = b
                b = n.replace(" - We do '1te Version'",'')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = b
                b = n.replace('Olé schwarz-weiß Olé', 'Olé schwarzweiß Olé')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = b
            elif n[0] == 'C' or n[0] == 'E':
                c = n.replace('Ne-Yo', 'Ne Yo')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = c
                e = n.replace('- Dubstep Violin', ' ')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = e
            elif n[0] == 'F' or n[0] == 'F' or n[0] == 'H':
                f = n.replace('Good Feeling - Seth G. Violin Cover', 'Good Feeling Violin Cover Seth G')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = f
                f = n.replace('FloRida Bach Black Eyed Peas', 'FloRida, Black Eyed Peas')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = f
                h = n.replace('Traduzido e legendado PT - BR', 'Hino da Itália')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = h
                h = n.replace('Hymne Fußball-Club Bayern München (Lyrics) - Hino do Bayern de Munique (letra)', 'Hymne FC Bayern München - Hino do Bayern de Munique')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = h                        
            elif n[0] == 'I' or n[0] == 'K':
                ii = n.replace(' w- Lyrics','')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = ii
                ii = n.replace(' (Official Video) - PUNCH 001','')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = ii
                k = n.replace(' [OFFICIAL VIDEO - HD]','')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = k
            elif n[0] == '[' or n[0] == 'P':
                p = n.replace('[Progressive] - ', '')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = p
                p = n.replace(' [Premiere]', '')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = p
                p = n.replace(' - Official Videoclip','')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = p            
            elif n[0] == 'R' or n[0] == 'R' or n[0] == 'T':
                r = n.replace(' (Official Video HD)','')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = r
                r = n.replace('- A Minecraft Parody of Usher s DJ Got Us Fallin  in Love - Crafted Using Noteblocks', '- Capitain Sparklez')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = r
                r = n.replace('U-Jean','U Jean')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = r
                t = n.replace('Titanium - David Guetta 8-BIT VERSION!','Titanium 8BIT VERSION - David Guetta')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = t
            elif n[0] == 'U' or n[0] == 'W':
                u = n.replace('Um Joystick, Um Violão - 10','Um Joystick, Um Violão')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = u
                u = n.replace('Um Joystick, Um Violão 09','Um Joystick, Um Violão')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = u
                u = n.replace('Coca-Cola', 'Coca Cola')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = u
                w = n.replace(' - Lyrics','')
                bancotitulos['Título'].loc[bancotitulos['Título'] == n] = w
    j += 1                

j = 0
parent = '\('
colch = '\['
#Tratando os dados que não possuem parenteses no nome dos títulos
bancotitulos2 = bancotitulos[~bancotitulos['Título'].str.contains(parent)]

for n in bancotitulos2['Título']:
    if n.count('[') > 0:         
        m = n.replace(']','',1)
        esq, lbracket, dire = m.partition('[')
        descarte, rbracket, resto = m.partition(']')           
        m = esq + ' ' + resto
        bancotitulos2['Título'].loc[bancotitulos2['Título'] == n] = m


for item in bancotitulos['Name']:
    for nome in bancotitulos2['Name']:
        if nome == item:
            bancotitulos['Título'].loc[bancotitulos['Name'] == nome] = bancotitulos2['Título'].loc[bancotitulos2['Name'] == nome]
            
            
            
#Tratando os dados que possuem parenteses e colchetes
bancotitulos2 = bancotitulos[bancotitulos['Título'].str.contains(colch)] 

for n in bancotitulos2['Título']:
    if n.count('In the End') == 1 or n.count('Freaks') == 1:
        konv = n.replace('In the End - Linkin Park (Samba) [KONVERSÃO]', 'Linkin Park feat Konversao - In The End')
        bancotitulos2['Título'].loc[bancotitulos2['Título'] == n] = konv
        nnd = n.replace('NIGGASNERDS [Freaks and Geeks (N²)MIX] - NiggasNerds','NiggasNerds - N² Freaks and Geeks')
        bancotitulos2['Título'].loc[bancotitulos2['Título'] == n] = nnd
    elif n.count('[') > 0:         
         esq, lbracket, dire = n.partition('[')
         m = esq
         bancotitulos2['Título'].loc[bancotitulos2['Título'] == n] = m
         
for item in bancotitulos['Name']:
    for nome in bancotitulos2['Name']:
        if nome == item:
            bancotitulos['Título'].loc[bancotitulos['Name'] == nome] = bancotitulos2['Título'].loc[bancotitulos2['Name'] == nome]
  
#Tratando os dados que possuem parenteses
bancotitulos2 = bancotitulos[bancotitulos['Título'].str.contains(parent)]

for n in bancotitulos2['Título']:
    if n.count('emix') > 0 or n.count('dit') > 0 or n.count('Anti K') > 0 or n.count('ootleg') > 0:
        esq, par, direi = n.partition(')')
        m = esq + ')'
        bancotitulos2['Título'].loc[bancotitulos2['Título'] == n] = m
    else:
         esq, par, direi = n.partition('(')
         m = esq
         bancotitulos2['Título'].loc[bancotitulos2['Título'] == n] = m
        
for item in bancotitulos['Name']:
    for nome in bancotitulos2['Name']:
        if nome == item:
            bancotitulos['Título'].loc[bancotitulos['Name'] == nome] = bancotitulos2['Título'].loc[bancotitulos2['Name'] == nome]
  
#Dividindo a tabela por -
bancotitulos[['Artista','Título']] = bancotitulos['Título'].str.split('-', expand = True)

bancotitulos2 = bancotitulos.loc[bancotitulos['Título'].isnull()]

bancotitulos2['Artista'], bancotitulos2['Título'] = bancotitulos2['Título'], bancotitulos2['Artista']
lista_artistas = ['Die Atzen','Steve Aoki','França', 'Calvin Harris','AS Roma','AC Milan','Juventus','Liverpool Fc','ManU Fc','Violin Instrumental']  

bancotitulos2['Artista'] = lista_artistas

for item in bancotitulos['Name']:
    for nome in bancotitulos2['Name']:
        if nome == item:
            bancotitulos['Título'].loc[bancotitulos['Name'] == nome] = bancotitulos2['Título'].loc[bancotitulos2['Name'] == nome]
            bancotitulos['Artista'].loc[bancotitulos['Name'] == nome] = bancotitulos2['Artista'].loc[bancotitulos2['Name'] == nome]

bancotitulos['Artista'] = bancotitulos['Artista'].str.strip()           
bancotitulos['Título'] = bancotitulos['Título'].str.strip() 

bctitcopia = bancotitulos.reset_index().drop(columns = 'index')
listacorr = ['2', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '2', '0', '1', '1', '1', '1', '1', '2', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '2', '1', '1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '2', '2', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '0', '1', '1', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '0', '1', '0', '1', '1', '1']
#Comando usado para gerar a listacorr acima
# while j <= len(bctitcopia) - 1:
#     print(bctitcopia.loc[j])
#     cespe = input('Coloque 0,1 ou 2: ')
#     listacorr.append(cespe)
#     #Comando para limpar a tela
#     print("\033[H\033[J", end="")
#     j += 1

bctitcopia['Codigo'] = listacorr

#bctitcopia.loc[bctitcopia['Codigo'] == '1']


bctitcopia['Título'][bctitcopia['Codigo']== '0'], bctitcopia['Artista'][bctitcopia['Codigo']== '0'] = bctitcopia['Artista'][bctitcopia['Codigo']== '0'], bctitcopia['Título'][bctitcopia['Codigo']== '0']
bctitcopia['Codigo'][bctitcopia['Codigo'] == '0'] = '1'



bctitcopia['Artista'][bctitcopia['Name'] == "08 Skrillex - Rock N' Roll (Will Take You To The Mountain).mp3"], bctitcopia['Título'][bctitcopia['Name'] == "08 Skrillex - Rock N' Roll (Will Take You To The Mountain).mp3"] = 'Skrillex', 'Rock N Roll'
bctitcopia['Artista'][bctitcopia['Name'] == 'Arash feat. T-Pain  Sex Love Rock N Roll (SLR)  Official Video.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Arash feat. T-Pain  Sex Love Rock N Roll (SLR)  Official Video.mp3'] = 'Arash feat. T Pain', 'Sex Love Rock N Roll'
bctitcopia['Artista'][bctitcopia['Name'] == 'Avicii - Silhouettes .mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Avicii - Silhouettes .mp3'] = 'Avicii', 'Silhouettes'
bctitcopia['Artista'][bctitcopia['Name'] == 'Basshunter - Far Far Away NEW SONG 2013 with Lyrics HD.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Basshunter - Far Far Away NEW SONG 2013 with Lyrics HD.mp3'] = 'Basshunter', 'Far Far Away'        
bctitcopia['Artista'][bctitcopia['Name'] == 'Calvin Harris ft. Florence Welch- Sweet Nothing LYRICS.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Calvin Harris ft. Florence Welch- Sweet Nothing LYRICS.mp3'] = 'Calvin Harris ft. Florence Welch', 'Sweet Nothing'
bctitcopia['Artista'][bctitcopia['Name'] == 'Fallen Kingdom  - A Minecraft Parody of Coldpl.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Fallen Kingdom  - A Minecraft Parody of Coldpl.mp3'] = 'Capitain Sparklez', 'Fallen Kingdom'
bctitcopia['Artista'][bctitcopia['Name'] == 'Fresh Prince of Bel Air - FULL THEME SONG.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Fresh Prince of Bel Air - FULL THEME SONG.mp3'] = 'Will Smith', 'Fresh Prince of Bel Air'
bctitcopia['Artista'][bctitcopia['Name'] == 'Hymne Borussia VFL 1900 (Lyrics) - Hino do Borussia Mönchengladbach (letra).mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Hymne Borussia VFL 1900 (Lyrics) - Hino do Borussia Mönchengladbach (letra).mp3'] = 'B.O.', 'Die elf vom Niederrein'
bctitcopia['Artista'][bctitcopia['Name'] == "ItaloBrothers - Cryin  In The Rain (Official HD Video).mp3"], bctitcopia['Título'][bctitcopia['Name'] == "ItaloBrothers - Cryin  In The Rain (Official HD Video).mp3"] = 'ItaloBrothers', "Cryin' In The Rain"
bctitcopia['Artista'][bctitcopia['Name'] == "ItaloBrothers - Pandora 2012.mp3"], bctitcopia['Título'][bctitcopia['Name'] == "ItaloBrothers - Pandora 2012.mp3"] = 'ItaloBrothers', "Pandora"
bctitcopia['Artista'][bctitcopia['Name'] == "ItaloBrothers - Up  N Away (Re-Load Remix).mp3"], bctitcopia['Título'][bctitcopia['Name'] == "ItaloBrothers - Up  N Away (Re-Load Remix).mp3"] = 'ItaloBrothers', "Up 'n Away"
bctitcopia['Artista'][bctitcopia['Name'] == 'Je ne sais pas Joyce Jonathan- lyrics.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Je ne sais pas Joyce Jonathan- lyrics.mp3'] = 'Joyce Jonathan', 'Je ne sais Pas'
bctitcopia['Artista'][bctitcopia['Name'] == 'Meg & Dia -  Monster  Doghouse Records.mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Meg & Dia -  Monster  Doghouse Records.mp3'] = 'Meg & Dia', 'Monster'
bctitcopia['Artista'][bctitcopia['Name'] == 'Mike Candys feat. Evelyn & Carlprit - Brand New Day (Official Video HD).mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Mike Candys feat. Evelyn & Carlprit - Brand New Day (Official Video HD).mp3'] = 'Mike Candys', 'Brand New Day'            
bctitcopia['Artista'][bctitcopia['Name'] == 'Mike Candys feat. Jenson Vaughan - Bring Back The Love (Official Video HD).mp3'], bctitcopia['Título'][bctitcopia['Name'] == 'Mike Candys feat. Jenson Vaughan - Bring Back The Love (Official Video HD).mp3'] = 'Mike Candys', 'Bring Back the Love'
bctitcopia['Artista'][bctitcopia['Name'] == 'Måns Zelmerlöw - Hereos (Will-Em Remix).m4a'], bctitcopia['Título'][bctitcopia['Name'] == 'Måns Zelmerlöw - Hereos (Will-Em Remix).m4a'] = 'Måns Zelmerlöw', 'Heroes'
bctitcopia['Codigo'][bctitcopia['Codigo'] == '2'] = '1'            

bancotitulos = bctitcopia[['Name', 'Artista','Título']]

for idc in bancotitulos['Name'].index.tolist():
    nome = bancotitulos['Name'][idc]
    titulo = bancotitulos['Título'][idc]
    artista = bancotitulos['Artista'][idc]
    
    for idx in base_copia['Name'].index.tolist():
        n = base_copia['Name'][idx]
        if nome == n:
            base_copia['Título'][idx] = titulo
            base_copia['Artistas participantes'][idx] = artista
            base_copia['Cod'][idx] = '1'

bancoartistas = base_copia[['Name', 'Título', 'Artistas participantes']].loc[base_copia['Cod'] == '']

dicioartistas = {'Linkin Park x Steve Aoki':'A Light That Never Comes (Coone Remix)', 'ERB': 'Obama vs Romney','Basshunter':'All I Ever Wanted',
'Cascada':'Everytime We Touch (Slow Version)','Christina Grimmie':'Demons','erb': 'Cleopatra vs Marilyn Monroe', 'David Guetta': 'Titanium (Violin Cover)',                 
'Dj Gollum vs Empyre One': 'The Bad Touch', 'Um Joystick Um Violão': 'Dragon Quest Caboclo', 'Swedish House Mafia': 'Drinking From the Bottle', 'Madagascar': 'Eu Me Remexo Muito',                 
'Brasil': 'Hino da Independência do Brasil', 'EC Noroeste':'HINO DO NOROESTE DE BAURU', 'SE Palmeiras': 'hino do palmeiras na guitarra', 'Iyaz feat Charice': 'Pyramid',                 
'Il Volo': 'Il Mondo', 'Zaz & Pablo Alboran': 'Sous le ciel de Paris','Erb':'Jobs x Gates','Nintendo': 'Super Mario Theme Dubstep Remix', 'nintendo': 'The Super Mario Song', 'Russian Song': 'Katyusha'}
dicioartistaschaves = list(dicioartistas.keys())
dicioartistasvalores = list(dicioartistas.values())

lista_k = ['Avicii', 'Avicii','Mike Candys','Afrojack','Ivan Gough','R.I.O feat U Jean']

j = 0
k = 0

for idc in bancoartistas['Name'].index.tolist():
    nome = bancoartistas['Name'][idc]
    titulo = bancoartistas['Título'][idc]
    artista = bancoartistas['Artistas participantes'][idc]

    if artista == '':
        if nome[0] == '0' or nome[0] == '1': 
            bancoartistas['Artistas participantes'][idc] = 'Pedra Leticia'
        elif j < 21:
                bancoartistas['Artistas participantes'][idc] = dicioartistaschaves[j]
                bancoartistas['Título'][idc] = dicioartistasvalores[j]
                j += 1
                
    elif artista.count('- www.musicasparabaixar.org') == 1:
        if artista.count('David Guetta') == 1:
              bancoartistas['Artistas participantes'][idc] = artista.replace('- www.musicasparabaixar.org','')              
   
        elif k < len(lista_k):
            bancoartistas['Artistas participantes'][idc] = lista_k[k]
            k += 1                      
        
#Adicionando os últimos valores na tabela base_copia        
for idc in bancoartistas['Name'].index.tolist():
    nome = bancoartistas['Name'][idc]
    titulo = bancoartistas['Título'][idc]
    artista = bancoartistas['Artistas participantes'][idc]
    
    for idx in base_copia['Name'].index.tolist():
        n = base_copia['Name'][idx]
        if nome == n:
            base_copia['Título'][idx] = titulo
            base_copia['Artistas participantes'][idx] = artista
            base_copia['Cod'][idx] = '1'        
        
        
basefinal = base_copia[['Artistas participantes','Título']]
basefinal = basefinal.rename(columns={'Artistas participantes':'Artista'})
basefinal['Genero'] = ''

basefinal['Artista'][304], basefinal['Título'][304] = 'Dj Antoine',"I'm On You"
basefinal['Artista'][368], basefinal['Título'][368] = 'Nerdcast 314',"Especial Dia Dos Namorados 2012"
basefinal['Artista'][457], basefinal['Título'][457] = 'Violin Instrumental',"The Final Countdown"

basefinal['Artista'][146] = 'Lindsey Stirling'
basefinal['Artista'][251] = 'Guns N  Roses'
basefinal['Artista'][360] = 'Skrillex'
basefinal['Artista'][394] = 'Pedra Leticia'
basefinal['Artista'][418] = 'R.I.O Feat. U Jean'
basefinal['Artista'][472] = 'Avicii'

basefinal['Artista'],basefinal['Título'] = basefinal['Artista'].apply(str.title),basefinal['Título'].apply(str.title) 
basefinal['Artista'],basefinal['Título'] = basefinal['Artista'].apply(str.strip),basefinal['Título'].apply(str.strip)


        
artistas_unicos = pd.DataFrame(basefinal['Artista'].unique())
artistas_unicos[1] = artistas_unicos.isnull()

#Preparando o banco de artistas unicos para serem separados por genero musical:      
for n in range(0,len(artistas_unicos)):
    m = artistas_unicos[0][n]
    
    if m.count('Nerdcast') == 1:
        l = m.split(' ')
        artistas_unicos[1][n] = l[0]
    else:        
        m = m.replace(' ','_',1)
        l = m.split(' ')
        artistas_unicos[1][n] = l[0]
            
    n += 1    
                      
lista_filtro = ['_Feat','_Feat.','_&','_Vs','_Ft','_Ft.',',']       
        
for n in range(0,len(artistas_unicos)):
    m = artistas_unicos[1][n]
    for item in lista_filtro:
        if m.count(item) != 0:
            p = m.replace(item,'')
            artistas_unicos[1][n] = p
        
        
artistas_unicos_filtrados = pd.DataFrame(artistas_unicos[1].unique())            
        
#Generos a serem categorizados: Hardstyle, HandsUp, Edm, Rock, Brasileira, Italiana, Pop Gringo, Instrumental, Outros, Podcast
diciogeneros = {'0':'Hardstyle','1':'HandsUp','2':'EDM','3':'Rock','4':'Brasileira','5':'Italiana','6':'Pop Gringo','7':'Instrumental','8':'Outros','9':'Podcast'}
codgenero = ['2', '4', '3', '2', '5', '4', '3', '3', '3', '1', '3', '3', '3', '2', '3', '3', '3', '6', '3', '3', '3', '1', '3', '3', '6', '4', '6', '4', '4', '4', '2', '7', '4', '6', '7', '6', '2', '6', '1', '3', '7', '8', '1', '2', '7', '2', '4', '0', '3', '6', '6', '2', '2', '1', '4', '1', '2', '6', '6', '9', '2', '0', '0', '0', '7', '1', '3', '4', '6', '6', '2', '1', '7', '8', '4', '2', '4', '4', '1', '2', '8', '3', '4', '8', '4', '2', '6', '7', '1', '2', '8', '0', '2', '2', '6', '3', '0', '2', '2', '0', '8', '8', '8', '8', '8', '2', '8', '6', '5', '4', '2', '8', '8', '8', '3', '6', '2', '6', '6', '2', '6', '2', '7', '4', '8', '2', '6', '6', '2', '8', '0', '2', '7', '2', '3', '6', '2', '6', '0', '5', '9', '2', '2', '4', '6', '6', '2', '2', '5', '3', '6', '0', '0', '3', '1', '7', '0', '0', '4', '4', '2', '2', '6', '4', '3', '6', '3', '2', '8', '2', '2', '2', '7', '0', '0', '6', '2', '8', '2', '7', '4', '6', '2', '2', '2', '8']       


#Comando usado para gerar a lista codgenero acima
# j = 0
# while j < len(artistas_unicos_filtrados):
#     print(artistas_unicos_filtrados[0].loc[j])
#     codeg = input('Coloque o codigo do genero: ')
#     codgenero.append(codeg)
#     #Comando para limpar a tela
#     # print("\033[H\033[J", end="")
#     j += 1        
        
artistas_unicos_filtrados[1] = codgenero
listageneros = []
        
for item in codgenero:
    g = diciogeneros[item]
    listageneros.append(g)          
  
artistas_unicos_filtrados['Genero'] = listageneros
artistas_unicos['Genero'] = ''        
        
for n in range(0, len(artistas_unicos)):
    artista = artistas_unicos[0][n]
    artunico = artistas_unicos[1][n]
    
    for a in range(0, len(artistas_unicos_filtrados)):
        artistafilt = artistas_unicos_filtrados[0][a]        
        genfilt = artistas_unicos_filtrados['Genero'][a]
        
        if artunico == artistafilt:
            artistas_unicos['Genero'][n] = genfilt                  
        
#Adicionando Generos à basefinal
for n in range(0, len(basefinal)):
    artista = basefinal['Artista'][n] 
    for a in range(0, len(artistas_unicos)):
        artistaunico = artistas_unicos[0][a]        
        genero = artistas_unicos['Genero'][a]
        
        if artista == artistaunico:
            basefinal['Genero'][n] = genero        
        

#Ajustes finais para o fechamento da basefinal
basefinal['Genero'][0] = 'Hardstyle'
basefinal['Título'][67] = 'Mãe'    
basefinal['Genero'][79] = 'Hardstyle'
basefinal['Artista'][85], basefinal['Título'][85], basefinal['Genero'][85] = 'Aerosmith',"I Don't Want To Miss A Thing",'Rock'
basefinal['Título'][99] = 'Summer 3Rd Mvt Four Seasons'
basefinal['Genero'][103] = 'Hardstyle'
basefinal['Título'][110] = 'Always'
basefinal['Título'][120] = 'Suite For Cello Solo No 1 In G, Bwv 1007 1 Prélude'
basefinal['Artista'][183] = 'Bundesliga Temporada 15 16'
basefinal['Artista'][200], basefinal['Título'][200], basefinal['Genero'][200] = 'Da Tweekaz',"Game Of Thrones",'Hardstyle'
basefinal['Genero'][206] = 'Instrumental'
basefinal['Genero'][219] = 'EDM'
basefinal['Genero'][234] = 'Hardstyle'
basefinal['Genero'][240] = 'EDM'
basefinal['Genero'][246] = 'Hardstyle'
basefinal['Genero'][354] = 'EDM'
basefinal['Título'][374] = 'E Se Ganhássemos Na Loteria'
basefinal['Artista'][395], basefinal['Título'][395], basefinal['Genero'][395] = 'Pegboard Nerds Feat. Elizaveta',"Hero (Da Tweekaz Remix)",'Hardstyle'
basefinal['Título'][427] = 'Samba Em Prelúdio'
basefinal['Título'][478] = "Si Jamais J'Oublie"
basefinal['Genero'][482] = 'Hardstyle'

basefinal['Nome'] = ''
basefinal['Nome'] = basefinal['Artista'] + ' - ' + basefinal['Título']
basefinal['Nome Original'] = base_copia['Name']
basefinal['Extensao'] = base_copia['File Extension']

#Gerando uma planilha Excel com os dados tratados
#basefinal.to_excel('/musicas_sdcard_tratada.xlsx', index = False)

path = '/Todas as Musicas' #Este é o caminho das musicas salvas em meu computador
nomes_originais = os.listdir(path)
sigla_generos = {'Hardstyle': ' (Hard)', 'HandsUp': ' (HUp)', 'EDM': ' (EDM)', 'Rock': ' (Rock)', 'Brasileira': ' (Bra)', 'Italiana': ' (Ita)', 'Pop Gringo': ' (Pop G)', 'Instrumental': ' (Inst)', 'Outros': ' (Out)', 'Podcast': ' (Pod)'}

for n in range(0,len(basefinal)):
    nome = basefinal['Nome'][n].replace(':','')
    sigla = sigla_generos[basefinal['Genero'][n]]
    extensao = basefinal['Extensao'][n]
    basefinal['Nome'][n] = nome + sigla + extensao
    
    
nomes_trocados = pd.DataFrame(nomes_originais)
nomes_trocados['Nome Trocado'] = ''
      
def trocar_nomes():
    for i in range(0, len(nomes_originais)):
        name = nomes_originais[i]    
        for n in range(0,len(basefinal)):
            nome = basefinal['Nome Original'][n]
            nome_trocado = basefinal['Nome'][n]
            if nome == name:
                nomes_trocados['Nome Trocado'][i] = nome_trocado
            elif nomes_trocados['Nome Trocado'][i] == '':
                nomes_trocados['Nome Trocado'][i] = name                 
    return 
                                 
trocar_nomes()
        

def renomear_arquivos():  
        for n in range(0, len(nomes_originais)):
            m = nomes_originais[n]
            p = nomes_trocados['Nome Trocado'][n]
            try:
                os.rename(path + f'/{m}', path + f'/{p}')
            except FileExistsError:
                pass
                        
            
            
renomear_arquivos()















