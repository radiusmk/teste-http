import argparse
import requests
import time
from collections import Counter
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import socket
from requests.adapters import HTTPAdapter
from urllib3.util import connection

# Adaptador customizado para forçar IPv4 ou IPv6
class IPAdapter(HTTPAdapter):
    def __init__(self, ipver=None, *args, **kwargs):
        self.ipver = ipver
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        self._set_ip_family()
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        self._set_ip_family()
        return super().proxy_manager_for(*args, **kwargs)

    def _set_ip_family(self):
        if self.ipver == 4:
            connection.allowed_gai_family = lambda: socket.AF_INET
        elif self.ipver == 6:
            connection.allowed_gai_family = lambda: socket.AF_INET6
        else:
            # Restaura comportamento padrão
            if hasattr(connection, '_allowed_gai_family'):
                connection.allowed_gai_family = connection._allowed_gai_family


def fazer_requisicao(url, session=None):
    try:
        inicio = time.time()
        if session:
            response = session.get(url)
        else:
            response = requests.get(url)
        fim = time.time()
        tempo_resposta = fim - inicio
        return response.status_code, tempo_resposta
    except Exception:
        return 'erro', None


def main():
    parser = argparse.ArgumentParser(description='Conta códigos de status HTTP de múltiplas requisições.')
    parser.add_argument('url', type=str, help='URL a ser acessada')
    parser.add_argument('quantidade', type=int, help='Quantidade de requisições a serem realizadas')
    parser.add_argument('--intervalo', type=float, default=0, help='Tempo (em segundos) entre as requisições (opcional)')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Quantidade de threads simultâneas (opcional, padrão=1)')
    parser.add_argument('--keep-alive', action='store_true', help='Reaproveitar conexões HTTP (keep-alive) usando requests.Session')
    parser.add_argument('--ipver', choices=['4', '6', 'auto'], default='auto', help='Versão IP a ser usada: 4 (IPv4), 6 (IPv6) ou auto (padrão)')
    args = parser.parse_args()

    status_counter = Counter()
    total = args.quantidade
    url = args.url
    intervalo = args.intervalo
    n_threads = args.threads
    keep_alive = args.keep_alive
    ipver = args.ipver
    ipver_str = {'4': 'IPv4', '6': 'IPv6', 'auto': 'Auto'}[ipver]
    ipver_num = {'4': 4, '6': 6, 'auto': None}[ipver]

    print(f'Iniciando {total} requisições para {url} usando {n_threads} thread(s)...')
    print(f'Keep-alive ativado: {"Sim" if keep_alive else "Não"}')
    print(f'Versão IP: {ipver_str}')

    inicio = time.time()

    tempos_resposta = []

    if keep_alive:
        # Uma sessão por thread para reaproveitar conexões
        thread_sessions = []
        for _ in range(n_threads):
            session = requests.Session()
            if ipver != 'auto':
                session.mount('http://', IPAdapter(ipver=ipver_num))
                session.mount('https://', IPAdapter(ipver=ipver_num))
            thread_sessions.append(session)
        def thread_worker(idx):
            session = thread_sessions[idx % n_threads]
            if intervalo > 0 and idx > 0:
                time.sleep(intervalo * idx)
            return fazer_requisicao(url, session=session)
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = [executor.submit(thread_worker, i) for i in range(total)]
            for i, future in enumerate(as_completed(futures)):
                status, tempo = future.result()
                status_counter[status] += 1
                if tempo is not None:
                    tempos_resposta.append(tempo)
                    print(f'Requisição {i+1}/{total}: Status {status} | Tempo de resposta: {tempo:.3f} s')
                else:
                    print(f'Requisição {i+1}/{total}: Status {status} | Tempo de resposta: erro')
        for session in thread_sessions:
            session.close()
    else:
        def worker(idx):
            if intervalo > 0 and idx > 0:
                time.sleep(intervalo * idx)
            if ipver != 'auto':
                session = requests.Session()
                session.mount('http://', IPAdapter(ipver=ipver_num))
                session.mount('https://', IPAdapter(ipver=ipver_num))
                result = fazer_requisicao(url, session=session)
                session.close()
                return result
            else:
                return fazer_requisicao(url)
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = [executor.submit(worker, i) for i in range(total)]
            for i, future in enumerate(as_completed(futures)):
                status, tempo = future.result()
                status_counter[status] += 1
                if tempo is not None:
                    tempos_resposta.append(tempo)
                    print(f'Requisição {i+1}/{total}: Status {status} | Tempo de resposta: {tempo:.3f} s')
                else:
                    print(f'Requisição {i+1}/{total}: Status {status} | Tempo de resposta: erro')

    fim = time.time()
    tempo_total = fim - inicio
    tempo_formatado = str(datetime.timedelta(seconds=int(tempo_total)))

    tempo_medio = sum(tempos_resposta) / len(tempos_resposta) if tempos_resposta else 0

    print('\nResumo dos códigos de status recebidos:')
    print(f'URL testada: {url}')
    print(f'Threads utilizadas: {n_threads}')
    print(f'Keep-alive ativado: {"Sim" if keep_alive else "Não"}')
    print(f'Versão IP: {ipver_str}')
    print(f'Tempo total do teste: {tempo_formatado}')
    print(f'Tempo médio de resposta: {tempo_medio:.3f} s')
    tabela = [[str(status), count] for status, count in status_counter.items()]
    print(tabulate(tabela, headers=['Status HTTP', 'Quantidade'], tablefmt='grid'))


if __name__ == '__main__':
    main() 