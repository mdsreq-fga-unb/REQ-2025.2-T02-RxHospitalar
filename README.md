# REQ-2025.2-T02-RxHospitalar

![Contributors](https://img.shields.io/github/contributors/mdsreq-fga-unb/REQ-2025.2-T02-RxHospitalar)
![Stars](https://img.shields.io/github/stars/mdsreq-fga-unb/REQ-2025.2-T02-RxHospitalar)
![Last Commit](https://img.shields.io/github/last-commit/mdsreq-fga-unb/REQ-2025.2-T02-RxHospitalar)
![Forks](https://img.shields.io/github/forks/mdsreq-fga-unb/REQ-2025.2-T02-RxHospitalar)

Somos estudantes da **Universidade de Brasília (UnB) | Faculdade de Ciências e Tecnologias em Engenharia (FCTE)** e este projeto está sendo desenvolvido no contexto da disciplina de **Requisitos de Software**, ministrada pelo professor e doutor **George Marsicano Correia**. Nosso grupo, denominado **BASED**, tem como objetivo aplicar conceitos e práticas de engenharia de software em um caso real, em parceria com a empresa **RX Hospitalar**. A RX Hospitalar é uma distribuidora de produtos médicos e oftalmológicos que enfrenta desafios significativos relacionados à gestão de dados, estoque e processos operacionais. Nesse cenário, nosso projeto busca propor e desenvolver um **sistema de gestão inteligente**, capaz de otimizar análises, reduzir riscos operacionais, melhorar a integração entre setores e apoiar a tomada de decisão estratégica, contribuindo para a modernização e eficiência da empresa.

## Integrantes do grupo BASED:


| <img src="https://github.com/AmandaaMoura.png" width="150"/> | <img src="https://github.com/BeatrizSants.png" width="150"/> | <img src="https://github.com/daviegito.png" width="150"/> |
|:------------------------------------------------------------:|:------------------------------------------------------------:|:---------------------------------------------------------:|
| **[Amanda de Moura](https://github.com/AmandaaMoura)**       | **[Beatriz Figueiredo dos Santos](https://github.com/BeatrizSants)** | **[Davi Marques do Egito Coelho](https://github.com/daviegito)** |
| <img src="https://github.com/Tridudys.png" width="120"/>     | <img src="https://github.com/gabrielaugusto23.png" width="120"/> | <img src="https://github.com/samuelvlobo.png" width="120"/> |
| **[Eduardo Oliveira Valadares](https://github.com/Tridudys)** | **[Gabriel Augusto V. V. Rocha](https://github.com/gabrielaugusto23)** | **[Samuel Rodrigues Viana Lobo](https://github.com/samuelvlobo)** |

# 🚀 Rodando o Docusaurus localmente

Aqui explicaremos como **instalar o Node.js** e **rodar o site da documentação Docusaurus localmente** usando **npm**.  



## 🧩 Pré‑requisitos

O Docusaurus requer:
- **Node.js** versão **>= 18.0.0**
- **npm** (instalado automaticamente com o Node)

Verifique se você já possui o Node instalado:

```bash
node -v
npm -v
```

Se esses comandos não funcionarem, siga as instruções abaixo.

---

## 🪟 Instalação no Windows

1. Baixe o instalador do Node.js no site oficial:  
   👉 https://nodejs.org/
2. Escolha a versão **LTS (Long Term Support)**.
3. Siga o instalador padrão (ele também instalará o `npm` automaticamente).
4. Após a instalação, confirme que o Node está disponível:
   ```bash
   node -v
   npm -v
   ```

---

## 🐧 Instalação no Linux (Ubuntu / WSL)

Execute os seguintes comandos no terminal:

```bash
# Atualize os pacotes
sudo apt update

# Instale o Node.js e npm
sudo apt install -y nodejs npm

# (Opcional, mas recomendado) instale o nvm para gerenciar versões do Node:
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
# source ~/.bashrc
# nvm install --lts
```

Verifique a instalação:
```bash
node -v
npm -v
```

---

## ⚙️ Instalando as dependências do Docusaurus

1. No terminal, navegue até a pasta onde está a documentação do projeto, pasta `docs`:

```bash
cd docs
```

2. Instale as dependências do Node:
> Dentro da pasta `docs`, insira o comando:
```bash
npm install
```
---

## ▶️ Rodando o servidor local

Depois de instalar as dependências, inicie o servidor de desenvolvimento:

```bash
npm run start
```

Normalmente o Docusaurus abrirá automaticamente no seu navegador, geralmente em:

👉 http://localhost:3000

Se não abrir automaticamente, abra o link manualmente.

---

## 🧹 Dicas úteis

- Para parar o servidor, pressione **Ctrl + C** no terminal.
- Caso ocorram erros de dependência, tente limpar o cache e reinstalar:

```bash
rm -rf node_modules
npm cache clean --force
npm install
```

---

## ✅ Resumo rápido (comandos)

```bash
# Verificar node/npm
node -v
npm -v

# (Windows) instalar via nodejs.org -> LTS
# (Ubuntu/WSL) instalar via apt ou usar nvm (recomendado)

# Entrar na pasta de docs do projeto
cd docs

# Instalar dependências
npm install

# Rodar localmente
npm run start
```
