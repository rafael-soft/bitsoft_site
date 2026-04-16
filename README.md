# Bit soft - Site Institucional

Site institucional de página única desenvolvido para divulgação da **BIT SOFT DESENVOLVIMENTO DE SOFTWARE LTDA**, com foco em serviços de desenvolvimento de software WEB.

## Objetivo

Apresentar a empresa de forma clara e moderna, destacando:

- serviços genéricos de desenvolvimento WEB;
- tecnologias principais: PHP, React e JavaScript;
- contato comercial por e-mail.

## Contato

- rafael.oliveira.roa@gmail.com

## Estrutura do projeto

- `index.html`: estrutura da página única;
- `styles.css`: estilos visuais, layout responsivo e identidade visual;
- `script.js`: animações de entrada/reveal dos blocos;
- `assets/logo.svg`: logo principal da Bit soft;
- `assets/favicon.svg`: favicon do site;
- `netlify.toml`: configuração de publicação para Netlify.

## Como executar localmente

Como é um site estático, você pode abrir diretamente o arquivo `index.html` no navegador.

Se preferir rodar com servidor local:

1. Acesse a pasta do projeto.
2. Execute:

   ```bash
   python3 -m http.server 8080
   ```

3. Abra no navegador:

   http://localhost:8080

## Características da interface

- layout moderno e responsivo (desktop e mobile);
- identidade visual com gradientes e elementos suaves;
- seção de serviços e tecnologias;
- animações leves para melhor experiência visual.

## Deploy no Netlify

Este projeto já está preparado para deploy no Netlify com o arquivo `netlify.toml`.

### Opção 1: Deploy pelo Git (recomendado)

1. Envie o projeto para um repositório GitHub/GitLab/Bitbucket.
2. No Netlify, clique em **Add new site** > **Import an existing project**.
3. Conecte o repositório e selecione o projeto.
4. O Netlify vai usar automaticamente:
   - Publish directory: `.`
   - Sem comando de build (site estático)
5. Clique em **Deploy site**.

### Opção 2: Deploy manual (drag and drop)

1. No painel do Netlify, acesse **Sites**.
2. Arraste a pasta do projeto para a área de deploy manual.
3. Aguarde a publicação.

### Observação sobre rotas

O `netlify.toml` inclui um redirect para `index.html`, garantindo funcionamento correto em acesso direto a rotas.

## Observações

- Não há backend neste projeto;
- Não há dependências externas de build;
- Ideal para uso como landing page institucional simples.
