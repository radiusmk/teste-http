import argparse
import requests
import time
from collections import Counter
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed


def fazer_requisicao(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception:
        return 'erro'


def main():
    parser = argparse.ArgumentParser(description='Conta códigos de status HTTP de múltiplas requisições.')
    parser.add_argument('url', type=str, help='URL a ser acessada')
    parser.add_argument('quantidade', type=int, help='Quantidade de requisições a serem realizadas')
    parser.add_argument('--intervalo', type=float, default=0, help='Tempo (em segundos) entre as requisições (opcional)')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Quantidade de threads simultâneas (opcional, padrão=1)')
    args = parser.parse_args()

    status_counter = Counter()
    total = args.quantidade
    url = args.url
    intervalo = args.intervalo
    n_threads = args.threads

    def worker(idx):
        if intervalo > 0 and idx > 0:
            time.sleep(intervalo * idx)
        return fazer_requisicao(url)

    print(f'Iniciando {total} requisições para {url} usando {n_threads} thread(s)...')

    import datetime
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(fazer_requisicao, url) for _ in range(total)]
        for i, future in enumerate(as_completed(futures)):
            status = future.result()
            status_counter[status] += 1
            print(f'Requisição {i+1}/{total}: Status {status}')
    fim = time.time()
    tempo_total = fim - inicio
    tempo_formatado = str(datetime.timedelta(seconds=int(tempo_total)))

    print('\nResumo dos códigos de status recebidos:')
    print(f'URL testada: {url}')
    print(f'Threads utilizadas: {n_threads}')
    print(f'Tempo total do teste: {tempo_formatado}')
    tabela = [[str(status), count] for status, count in status_counter.items()]
    print(tabulate(tabela, headers=['Status HTTP', 'Quantidade'], tablefmt='grid'))


if __name__ == '__main__':
    main() 