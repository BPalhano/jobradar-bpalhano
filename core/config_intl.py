
# Configuração do programa internacional do JobRadar calibrada para o perfil
# de Igor Braga Palhano (Engenharia de Sistemas Embarcados e Telecomunicações).
#
# Foco: Oportunidades 100% remotas pagando em moeda forte (USD, EUR, GBP, CAD, etc.),
# em regime de contratação direta, prestação de serviços (Contractor, B2B, PJ Internacional)
# ou contratação global.

from core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DB_PATH, CIDADES_EUROPA_IBERICA  # noqa: F401

# Cargos Fortes Internacionais: títulos em inglês e francês que confirmam
# diretamente o alinhamento com Sistemas Embarcados, Firmware, C/C++, DSP,
# Telecomunicações e IA Embarcada.
KEYWORDS_INTL = [
    # Sistemas Embarcados & Firmware
    "Embedded Systems Engineer",
    "Embedded Software Engineer",
    "Embedded Software Developer",
    "Firmware Engineer",
    "Firmware Developer",
    "Embedded Firmware Engineer",
    "Embedded Engineer",
    "Embedded C Engineer",
    "Embedded C++ Engineer",
    "Embedded C++ Developer",
    "Embedded Linux Engineer",
    "Embedded Linux Developer",
    "RTOS Software Engineer",
    "IoT Software Engineer",
    "IoT Firmware Engineer",
    "IoT Engineer",
    # C++ & Software Core
    "C++ Software Engineer",
    "C++ Developer",
    "C++ Engineer",
    "C/C++ Software Engineer",
    "C/C++ Developer",
    # Telecomunicações, Wireless & Processamento de Sinais (DSP)
    "DSP Engineer",
    "Signal Processing Engineer",
    "Digital Signal Processing Engineer",
    "Wireless Systems Engineer",
    "Wireless Communications Engineer",
    "Wireless Engineer",
    "RF Software Engineer",
    "Telecommunications Engineer",
    "Telecom Engineer",
    "5G Systems Engineer",
    "6G Research Engineer",
    # Edge AI, Computer Vision & Machine Learning
    "Edge AI Engineer",
    "Embedded AI Engineer",
    "TinyML Engineer",
    "Computer Vision Engineer",
    # Nomenclatura em Francês (Mercado França, Suíça, Bélgica, Canadá)
    "Ingénieur Systèmes Embarqués",
    "Ingénieur Logiciel Embarqué",
    "Ingénieur Firmware",
    "Ingénieur Développement C++",
    "Ingénieur Traitement du Signal",
    "Ingénieur Télécoms",
    "Ingénieur Télécommunication",
    "Ingénieur Vision par Ordinateur",
    "Ingénieur IA Embarquée",
]

# Cargos Ambíguos no cenário internacional (exigem qualificador de tecnologia)
KEYWORDS_INTL_AMBIGUO = [
    "Software Engineer",
    "Systems Engineer",
    "Research Engineer",
    "Algorithm Engineer",
    "Robotics Engineer",
]

# Qualificadores necessários quando o cargo for ambíguo
QUALIFICADORES_INTL = [
    "embedded",
    "firmware",
    "c++",
    "dsp",
    "wireless",
    "telecom",
    "5g",
    "6g",
    "rtos",
    "freertos",
    "microcontroller",
    "stm32",
    "esp32",
    "arm",
    "nxp",
    "ble",
    "bluetooth",
    "iot",
    "fpga",
    "vhdl",
    "edge ai",
    "tinyml",
    "computer vision",
    "signal processing",
    "traitement du signal",
    "embarqué",
    "embarque",
]

# Ferramentas no título da vaga
FERRAMENTAS_INTL_TITULO = [
    "C++",
    "C/C++",
    "FreeRTOS",
    "RTOS",
    "Embedded Linux",
    "ESP32",
    "STM32",
    "ARM",
    "DSP",
    "SDR",
    "GNU Radio",
    "PyTorch",
    "TinyML",
    "Edge AI",
    "Computer Vision",
]

QUALIFICADORES_CARGO_INTL = [
    "engineer",
    "developer",
    "ingénieur",
    "ingenieur",
    "développeur",
    "developpeur",
    "programmer",
    "specialist",
    "contractor",
    "consultant",
    "architect",
    "intern",
    "junior",
    "mid",
    "lead",
    "freelance",
    "freelancer",
    "development",
    "project",
    "firmware",
    "embedded",
]

# Termos de consulta para varredura internacional no LinkedIn e agregadores
TERMOS_BUSCA_INTL = [
    "embedded software engineer remote",
    "firmware engineer remote",
    "embedded systems engineer remote",
    "c++ software engineer remote",
    "c++ developer remote",
    "dsp engineer remote",
    "signal processing engineer remote",
    "wireless engineer remote",
    "edge ai engineer remote",
    "computer vision engineer remote",
    "embedded linux remote",
    "iot firmware engineer remote",
    "freertos remote",
    "embedded c remote",
    "telecommunications engineer remote",
    "ingénieur systèmes embarqués télétravail",
    "ingénieur logiciel embarqué remote",
]

# Quantidade de termos buscados por ciclo de execução
TERMOS_POR_CICLO_INTL = 8

# Mercados / Países pesquisados no LinkedIn
LOCATIONS_INTL = [
    "United States",
    "United Kingdom",
    "Germany",
    "France",
    "Canada",
    "Netherlands",
    "Switzerland",
]

# Modalidades de localização aceitas (100% Remoto em inglês, francês e português)
CIDADES_INTL = ["Remote", "Remoto", "Télétravail", "Teletravail", "Home Office"]

# Mercados de onde a vaga remota é aceita (moedas fortes, Europa, América do Norte e contratação global)
MERCADOS_REMOTO_ACEITOS_INTL = [
    "Estados Unidos",
    "Reino Unido",
    "Alemanha",
    "França",
    "Canadá",
    "Holanda",
    "Suíça",
    "Austrália",
    "Portugal",
    "Espanha",
    "Irlanda",
    "Bélgica",
    "Suécia",
    "Dinamarca",
    "Noruega",
    "Finlândia",
    "Áustria",
    "Itália",
    "México",
    "Colômbia",
    "Argentina",
    "Chile",
    "Brasil",
    "LATAM",
    "Europa",
    "EMEA",
    "Worldwide",
    "Global",
    "Anywhere",
]

# Não restringir idioma por texto no título: o usuário tem fluência em inglês
# e francês, e os anúncios internacionais de tecnologia já são publicados em inglês.
IDIOMAS_EXIGIDOS_INTL = None

# Toggle para o eixo ibérico (vagas presenciais/híbridas em Portugal/Espanha)
ATIVAR_EIXO_IBERICO = False

# Domínios Indeed para varredura internacional
DOMINIOS_INDEED_INTL = {
    "Estados Unidos": "www.indeed.com",
    "Reino Unido": "uk.indeed.com",
    "França": "fr.indeed.com",
    "Alemanha": "de.indeed.com",
    "Canadá": "ca.indeed.com",
}
