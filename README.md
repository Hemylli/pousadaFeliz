# pousadaFeliz
Projeto de Desenvolvimento Rápido em Python - RAD Python para a Faculdade com a proposta de montar um sistema de gestão de pousada utilizando Python, Tkinter e SQLite.

# 🏨 Pousada Feliz - Sistema de Gestão

Sistema de gerenciamento para uma pousada, desenvolvido em Python com interface gráfica usando Tkinter e banco de dados SQLite.

## 🗂️ Estrutura do Projeto

pousada_feliz/
│
├── app/ # 🖥️ Interface gráfica e modelos
│ ├── init.py
│ ├── models/ # 🎭 Modelos: Hospede, Quarto, Reserva
│ │ ├── init.py
│ │ ├── hospede.py
│ │ ├── quarto.py
│ │ └── reserva.py
│ │
│ └── gui/ # 🎨 Interface gráfica com Tkinter
│ ├── init.py
│ ├── main_window.py
│ ├── tela_login.py
│ ├── tela_reservas.py
│ ├── tela_quartos.py
│ └── tela_clientes.py
│
├── controller/ # 🔌 Conexão e operações com o banco de dados
│ ├── init.py
│ └── database.py
│
├── data/ # 📁 Banco de dados e arquivos de dados
│ └── dados.db
│
├── main.py # 🚀 Arquivo principal
└── README.md # 📄 Documentação


## 🚀 Funcionalidades

- Tela de Login
- Gerenciamento de Reservas
- Gerenciamento de Quartos
- Gerenciamento de Clientes
- Visualização de dados em tabelas
- Caixa de envio de mensagens para clientes (simulação)

## 🛠️ Tecnologias

- Python 3.x
- Tkinter (Interface gráfica)
- SQLite (Banco de dados local)

## 📦 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pousada-feliz.git
Acesse a pasta do projeto:

bash
Copiar
Editar
cd pousada-feliz
Instale os requisitos (nenhum externo, usa apenas bibliotecas padrão do Python).

Execute o projeto:

bash
Copiar
Editar
python main.py
🔐 Login de Acesso
Usuário: admin

Senha: admin

📚 Melhorias Futuras
Relatórios em PDF

Envio real de e-mails

Dashboard com gráficos

Histórico de clientes e reservas

👨‍💻 Desenvolvedor
💼 Projeto educacional

✉️ contato: https://www.linkedin.com/in/hemylli/
