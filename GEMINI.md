# Diretrizes e Invariantes do JobRadar

Este projeto é um monitor autônomo de vagas customizado para o perfil de **Igor Braga Palhano** (Engenheiro de Sistemas Embarcados e Telecomunicações).

## 1. Arquitetura de Processos e Serviços (Systemd)
- **Modo de Execução:** O JobRadar NÃO deve rodar como daemon contínuo em loop infinito (`while True`). Scrapers com Playwright/Chromium tendem a acumular subprocessos e vazar memória.
- **Oneshot + Timer:** A execução local deve sempre operar no modelo `Type=oneshot` (`main.py --perfil internacional brasil --once`) acionado por `jobradar.timer` com `OnUnitInactiveSec=3h` e `OnBootSec=1min`.
- **Consumo Zero em Repouso:** Ao finalizar a varredura, o processo deve sair com status 0 para que o systemd destrua o cgroup e libere 100% da memória RAM (0 MB ocioso entre ciclos).
- **Sem Loops com Restart:** Não usar `Restart=always` no systemd sem backoff seguro, prevenindo repetições em curto intervalo que spammam o Telegram.

## 2. Mensageria e Notificações (Telegram Bot API)
- **Escape Obrigatório de HTML:** Em qualquer mensagem com `parse_mode="HTML"`, todo campo dinâmico (`titulo`, `empresa`, `link`, `motivo`, `salario`, etc.) DEVE passar por `html.escape(str(campo))` para evitar que caracteres como `<`, `>`, `&` causem `HTTP 400 Bad Request`.
- **Tamanho de Mensagens:** O limite da API do Telegram é de 4096 caracteres. Mensagens agrupadas (digests) devem ser particionadas respeitando margem segura (máximo 3500 chars).

## 3. Critérios de Relevância e Perfil
- **Foco Técnico:** Sistemas Embarcados, Firmware, Telecomunicações (5G/6G, RF, DSP), C/C++, FreeRTOS, Linux Embarcado, Visão Computacional e Edge AI.
- **Regras de Pontuação:**
  - +1 ponto se a vaga for prestação de serviço / contractor / PJ.
  - +1 ponto se a vaga informar valor ou faixa salarial.
- **Deduplicação:** Toda vaga deve ser validada tanto pelo hash do link (`id`) quanto pela combinação normalizada `empresa|titulo` (`chave_secundaria`), garantindo que vagas repetidas em fontes diferentes não sejam reenviadas.
