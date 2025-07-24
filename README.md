# http_status_counter.py

Script para realizar múltiplas requisições HTTP a uma URL, contabilizando os códigos de status recebidos, tempos de resposta e exibindo um resumo detalhado ao final.

## Funcionalidades
- Suporte a múltiplas threads, com divisão automática das requisições entre elas.
- Suporte a keep-alive (reaproveitamento de conexões HTTP via `requests.Session`).
- Suporte a IPv4, IPv6 ou escolha automática.
- Exibição do tempo de resposta de cada requisição.
- Exibição da data/hora de início e fim do teste no resumo.
- Resumo tabulado dos códigos de status HTTP recebidos.

## Uso

```bash
python http_status_counter.py URL QUANTIDADE [opções]
```

### Parâmetros obrigatórios
- `URL` — Endereço a ser acessado.
- `QUANTIDADE` — Número total de requisições a serem realizadas.

### Opções
- `-i`, `--intervalo` `<segundos>` — Tempo (em segundos) entre as requisições de cada thread (padrão: 0).
- `-t`, `--threads` `<n>` — Número de threads simultâneas (padrão: 1). As requisições são divididas igualmente entre as threads.
- `--keep-alive` — Ativa o reaproveitamento de conexões HTTP (cada thread mantém sua própria sessão).
- `--ipver` `<4|6|auto>` — Força o uso de IPv4, IPv6 ou deixa automático (padrão: auto).

### Exemplos

Requisições simples:
```bash
python http_status_counter.py "https://exemplo.com" 10
```

Com 5 threads, keep-alive e intervalo de 1 segundo entre requisições de cada thread:
```bash
python http_status_counter.py "https://exemplo.com" 20 -t 5 --keep-alive -i 1
```

Forçando IPv6:
```bash
python http_status_counter.py "https://exemplo.com" 10 --ipver 6
```

## Resumo exibido ao final
- URL testada
- Threads utilizadas
- Keep-alive ativado
- Versão IP
- **Data/hora início**
- **Data/hora fim**
- Tempo total do teste
- Tempo médio de resposta
- Tabela de códigos de status HTTP recebidos

## Observações
- O tempo de resposta exibido é o tempo real de ida e volta da requisição, não incluindo o tempo de espera do intervalo.
- O parâmetro `--keep-alive` faz com que cada thread mantenha uma sessão HTTP, reaproveitando conexões para maior eficiência.
- As requisições são divididas igualmente entre as threads. Se o total não for divisível, as primeiras threads recebem uma requisição extra. 