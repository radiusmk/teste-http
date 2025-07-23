# Test-HTTP

Script em Python para realizar múltiplas requisições HTTP a uma URL, contabilizar os códigos de status recebidos e exibir um resumo dos resultados em formato de tabela.

## Objetivo

Este projeto permite testar endpoints HTTP realizando várias requisições simultâneas, contabilizando os retornos HTTP (status code) e exibindo um resumo ao final, incluindo tempo total do teste, URL testada e número de threads utilizadas.

## Instalação

1. Clone este repositório ou baixe os arquivos.
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Uso

Execute o script passando a URL, a quantidade de requisições e, opcionalmente, o intervalo entre as requisições e o número de threads:

```bash
python http_status_counter.py <URL> <QUANTIDADE> [--intervalo SEGUNDOS] [-t THREADS]
```

### Parâmetros

- `<URL>`: Endereço HTTP/HTTPS a ser testado (obrigatório)
- `<QUANTIDADE>`: Número total de requisições a serem realizadas (obrigatório)
- `-i`: Intervalo (em segundos) entre as requisições (opcional, padrão: 0)
- `-t`, `--threads`: Número de threads simultâneas (opcional, padrão: 1)

### Exemplos

Requisições sequenciais:
```bash
python http_status_counter.py https://httpbin.org/status/200 10
```

Requisições simultâneas com 5 threads:
```bash
python http_status_counter.py https://httpbin.org/status/200 50 -t 5
```

Requisições com intervalo de 2 segundos entre cada:
```bash
python http_status_counter.py https://httpbin.org/status/200 10 -i 2
```

## Saída

Ao final do teste, será exibido um resumo contendo:
- URL testada
- Número de threads utilizadas
- Tempo total do teste (hh:mm:ss)
- Tabela com a contagem de cada código de status HTTP recebido

---

Sinta-se à vontade para contribuir ou sugerir melhorias! 