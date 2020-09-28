import paramiko
from time import sleep
import re

def roda_comando_ssh_remoto(endereco, usuario, senha, comando):
    conexao_ssh = paramiko.SSHClient()
    conexao_ssh.load_system_host_keys()
    conexao_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexao_ssh.connect(endereco, username=usuario, password=senha, look_for_keys=False)
    comando = comando
    print(f'Comando a ser executado: {comando}')
    ssh_stdin, ssh_stdout, ssh_stdeer = conexao_ssh.exec_command(comando)
    saida_comando = ssh_stdout.readlines()
    print(f'Saida Comando dentro da sessao ssh: {saida_comando}')
    conexao_ssh.close()
    return saida_comando


def popula_lista_arquivos_md5sum(servidores_remotos):
    for servidor in servidores_remotos:
        lista_temporia_arquivos_md5sum = roda_comando_ssh_remoto(
            servidor['endereco_servidor'], 
            servidor['usuario'],
            servidor['senha'],
            f'md5sum {servidor["diretorio"]}*')
        
        for arquivo_md5sum in lista_temporia_arquivos_md5sum:
            if '.py' or '.sh' in arquivo_md5sum:
                arquivo_temp = {}
                regex_exec = re.search('(.*)(\s\s)(\/tmp\/arquivos\/)(.*)', arquivo_md5sum)
                arquivo_temp['nome_arquivo'] = regex_exec.group(4)
                arquivo_temp['md5sum'] = regex_exec.group(1)
                servidor['lista_arquivos_md5sum'].append(arquivo_temp.copy())
                arquivo_temp.clear()
                
"""      
def popula_lista_arquivos_ultima_alteracao(servidores_remotos):
    for servidor in servidores_remotos:
        lista_temporia_arquivos_ultima_alteracao = roda_comando_ssh_remoto(
            servidor['endereco_servidor'], 
            servidor['usuario'],
            servidor['senha'],
            f'stat {servidor["diretorio"]}*')
        print(f'LISTA_TEMPORARIA_ARQUIVOS_ULTIMA_ALTERACAO: {lista_temporia_arquivos_ultima_alteracao}')
        
        for stat_arquivo in lista_temporia_arquivos_ultima_alteracao:
            if '.py' or '.sh' in stat_arquivo:
                arquivo_temp = {}
                print(f'STAT_ARQUIVO_ANTES_DA_REGEX: {stat_arquivo}')
                regex_exec = re.search("(File:)(\s)(\/tmp\/arquivos\/)(.*)(', '  Size:)(.*)('Modify: )(.*)(',)(\s)('Change: )(.*)", stat_arquivo)
                print(f'LISTA_TEMPORAIA_ARQUIVOS_ULTIMA_ALTERACAO_COM_REGEX: {regex_exec}')
                arquivo_temp['nome_arquivo'] = regex_exec.group(4)
                arquivo_temp['ultima_alteracao'] = regex_exec.group(8)
                servidor['lista_arquivos_ultima_alteracao'].append(arquivo_temp.copy())
                arquivo_temp.clear()
"""


def popular_lista_arquivos_unicos(servidores_remotos):
    lista_unificada_arquivos = []
    
    for servidor in servidores_remotos:
        lista_temporaria_arquivos_unicos = roda_comando_ssh_remoto(
            servidor['endereco_servidor'], 
            servidor['usuario'],
            servidor['senha'],
            f'ls {servidor["diretorio"]}*')
    
        for arquivo in lista_temporaria_arquivos_unicos:
            if '.py' or '.sh' in arquivo:
                #arquivo_temp = {}
                #regex_exec = re.search('(.*)(\s\s)(\/tmp\/arquivos\/)(.*)', arquivo_md5sum)
                #arquivo_temp['nome_arquivo'] = regex_exec.group(4)
                #arquivo_temp['md5sum'] = regex_exec.group(1)
                #servidor['lista_arquivos_md5sum'].append(arquivo_temp.copy())
                #arquivo_temp.clear()
                if arquivo not in lista_unificada_arquivos:
                    arquivo_sem_dir = str(arquivo.replace('/tmp/arquivos/', ''))
                    arquivo_ajustado = arquivo_sem_dir.replace('\n','')
                    print(f'ARQUIVO AJUSTADO: {arquivo_ajustado}')
                    lista_unificada_arquivos.append(arquivo_ajustado)
    
    return lista_unificada_arquivos

    
def main():
    #Gerar uma lista de arquivos e seus md5 para cada servidor.
    print('Gerando lista de arquivos/md5sum para cada servidor.')
    popula_lista_arquivos_md5sum(servidores_remotos)
    sleep(1)
    print('Imprime lista de arquivos por servidor e seus md5:') 
    for servidor in servidores_remotos:
        print(f'Servidor: {servidor["nome_servidor"]}')
        for arquivo_md5sum in servidor['lista_arquivos_md5sum']:
            print(arquivo_md5sum)
        sleep(1)
        print('='*50)
    
    """          
    #Gerar uma lista de arquivos e sua ultima alteracao para cada servidor
    print('Gerando lista de arquivos e sua ultima alteracao para cada servidor.')
    popula_lista_arquivos_ultima_alteracao(servidores_remotos)
    sleep(1)
    print('Imprime lista de arquivos por servidor e sua ultima alteracao:')
    for servidor in servidores_remotos:
        print(f'Servidor: {servidor["nome_servidor"]}')
        for arquivo_ultima_alteracao in servidor['lista_arquivos_ultima_alteracao']:
            print(arquivo_ultima_alteracao)
        sleep(1)
        print('='*50)
    """
    
    #Gerar uma lista unificada de arquivos unicos
    lista_arquivos_unicos = popular_lista_arquivos_unicos(servidores_remotos)
    print(f'LISTA DE ARQUIVOS UNICOS: {lista_arquivos_unicos}')
    
    #Com a lista em maos:
        #Verificar qual servidor nao possui os arquivos
        #Contar quantidade de Md5sum por arquivo:
            #Caso exista mais de um para um arquivo:
                #Criar uma lista com os arquivos/servidores e seus md5sum.
    pass            

servidores_remotos = [
    {
        'nome_servidor': 'localhost',
        'endereco_servidor': 'localhost',
        'usuario': 'ilhanublar',
        'senha': '',
        'diretorio': '/tmp/arquivos/',
        'lista_arquivos_md5sum': [], #nome + md5
        'lista_arquivos_ultima_alteracao': [], #nome + data de ultima alteracao
    },
    {
        'nome_servidor': 'zabbix-server',
        'endereco_servidor': '192.168.0.118',
        'usuario': 'zabbix-server',
        'senha': 'zabbix-server',
        'diretorio': '/tmp/arquivos/',
        'lista_arquivos_md5sum': [],
        'lista_arquivos_ultima_alteracao': []
    }
]


lista_erros = []

main()
