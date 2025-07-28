# Test-HTTP

Script em Python para realizar múltiplas requisições HTTP a uma URL, contabilizar os códigos de status recebidos e exibir um resumo dos resultados em formato de tabela.

## Objetivo

Este projeto permite testar endpoints HTTP realizando várias requisições simultâneas, contabilizando os retornos HTTP (status code) e exibindo um resumo ao final, incluindo tempo total do teste, URL testada, número de threads utilizadas, tempo médio de resposta e outras informações úteis.

## Instalação

1. Clone este repositório ou baixe os arquivos.
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Uso

Execute o script passando a URL, a quantidade de requisições e, opcionalmente, o intervalo entre as requisições, o número de threads, o reaproveitamento de conexões e a versão do IP:

```bash
python http_status_counter.py <URL> <QUANTIDADE> [--intervalo SEGUNDOS] [-t THREADS] [--keep-alive] [--ipver 4|6|auto]
```

### Parâmetros

- `<URL>`: Endereço HTTP/HTTPS a ser testado (obrigatório)
- `<QUANTIDADE>`: Número total de requisições a serem realizadas (obrigatório)
- `-i`: Intervalo (em segundos) entre as requisições (opcional, padrão: 0)
- `-t`, `--threads`: Número de threads simultâneas (opcional, padrão: 1)
- `--keep-alive`: Reaproveita conexões HTTP usando keep-alive (opcional)
- `--ipver`: Versão do IP a ser utilizada: `4` (IPv4), `6` (IPv6) ou `auto` (padrão, deixa o sistema escolher)

### Exemplos

Requisições sequenciais:
```bash
python http_status_counter.py https://httpbin.org/status/200 10
```

Requisições simultâneas com 5 threads e keep-alive:
```bash
python http_status_counter.py https://httpbin.org/status/200 50 -t 5 --keep-alive
```

Requisições forçando IPv6:
```bash
python http_status_counter.py https://httpbin.org/status/200 10 --ipver 6
```

Requisições com intervalo de 2 segundos entre cada:
```bash
python http_status_counter.py https://httpbin.org/status/200 10 -i 2
```

## Saída

Durante a execução, para cada requisição, será exibido:
- Número da requisição
- Código de status HTTP
- Tempo de resposta (em segundos)

Ao final do teste, será exibido um resumo contendo:
- URL testada
- Número de threads utilizadas
- Keep-alive ativado ou não
- Versão IP utilizada
- Tempo total do teste (hh:mm:ss)
- Tempo médio de resposta (em segundos)
- Tabela com a contagem de cada código de status HTTP recebido

---

Sinta-se à vontade para contribuir ou sugerir melhorias! 