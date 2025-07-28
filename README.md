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
  - Suporta a tag `<count>` que será substituída pelo número da requisição
- `<QUANTIDADE>`: Número total de requisições a serem realizadas (obrigatório)
- `-i`, `--intervalo`: Intervalo (em segundos) entre as requisições (opcional, padrão: 0)
- `-t`, `--threads`: Número de threads simultâneas (opcional, padrão: 1)
- `--keep-alive`: Reaproveita conexões HTTP usando keep-alive (opcional)
- `--ipver`: Versão do IP a ser utilizada: `4` (IPv4), `6` (IPv6) ou `auto` (padrão, deixa o sistema escolher)

### Funcionalidades Especiais

#### Tag `<count>` na URL
Você pode usar a tag `<count>` na URL para gerar URLs únicas para cada requisição. O `<count>` será substituído pelo número da requisição (começando em 1).

**Exemplos:**
```bash
# Cada requisição acessará uma URL diferente
python http_status_counter.py "https://api.exemplo.com/user/<count>" 10

# Com parâmetros na URL
python http_status_counter.py "https://api.exemplo.com/test?id=<count>&type=load" 50
```

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

Requisições com URLs únicas usando `<count>`:
```bash
python http_status_counter.py "https://httpbin.org/status/<count>" 10
```

## Saída

Durante a execução, para cada requisição, será exibido:
- Número da requisição
- Código de status HTTP
- Tempo de resposta (em segundos)
- URL utilizada (especialmente útil quando usando a tag `<count>`)

**Exemplo de saída:**
```
Iniciando 10 requisições para https://httpbin.org/status/<count> usando 1 thread(s)...
Keep-alive ativado: Não
Versão IP: Auto
Requisição 1/10: Status 200 | Tempo de resposta: 0.245 s | URL: https://httpbin.org/status/1
Requisição 2/10: Status 200 | Tempo de resposta: 0.198 s | URL: https://httpbin.org/status/2
...
```

Ao final do teste, será exibido um resumo contendo:
- URL testada
- Número de threads utilizadas
- Keep-alive ativado ou não
- Versão IP utilizada
- Data/hora de início e fim
- Tempo total do teste (hh:mm:ss)
- Tempo médio de resposta (em segundos)
- Tabela com a contagem de cada código de status HTTP recebido

## Características

- **Progresso em tempo real**: Mostra o resultado de cada requisição assim que é concluída
- **Suporte a múltiplas threads**: Permite executar requisições simultâneas
- **Keep-alive**: Opção para reaproveitar conexões HTTP
- **Forçar IPv4/IPv6**: Controle sobre a versão do IP utilizada
- **URLs dinâmicas**: Suporte à tag `<count>` para URLs únicas por requisição
- **Intervalo configurável**: Possibilidade de adicionar delay entre requisições

---

Sinta-se à vontade para contribuir ou sugerir melhorias! 