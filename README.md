# Bitsoft — Site institucional

Site de página única da **BIT SOFT DESENVOLVIMENTO DE SOFTWARE LTDA** — *Soluções em aplicações web*.
Endereço: [www.bitsoft.dev.br](https://www.bitsoft.dev.br/).

## Identidade visual

| Cor | Hex | Uso |
| --- | --- | --- |
| Navy | `#0B1026` | Fundo principal |
| Azul Tech | `#0EA5E9` | Links, ações, tecnologia |
| Violeta | `#7C3AED` | Destaques, inovação |
| Neutro | `#F8FAFC` | Texto e fundos claros |

- O gradiente azul → violeta é a assinatura da marca: use com moderação (logo, CTA principal, destaques).
- Tipografia: **Inter** (principal) e **JetBrains Mono** (detalhes técnicos).
- Slogan: **SOLUÇÕES EM APLICAÇÕES WEB**.

### Arquivos de marca (`assets/brand/`)

| Arquivo | Uso |
| --- | --- |
| `logo-horizontal.svg` / `-light.svg` | Logo completo com slogan (fundo escuro / claro) |
| `logo-compact.svg` / `-light.svg` | Símbolo + nome, sem slogan (cabeçalhos, tamanhos pequenos) |
| `logo-vertical.svg` / `-light.svg` | Símbolo acima do nome e do slogan |
| `icon.svg` / `icon-light-bg.svg` | Símbolo colorido (código branco / navy) |
| `icon-white.svg`, `icon-dark.svg`, `icon-mono-*.svg` | Versões monocromáticas |
| `app-icon*.svg` | Ícone em quadrado arredondado (avatar, redes sociais, WhatsApp) |
| `png/` | Exportações PNG transparentes em alta resolução |

Os SVGs são gerados por `docs/brand/gen.py` (textos convertidos em curvas, sem dependência de fonte).
A referência original (prancha e conversa do ChatGPT) e os prompts para gerar versões raster estão em `docs/brand/`.

## Estrutura

- `index.html`, `404.html`, `styles.css`, `script.js` — o site;
- `assets/` — marca, favicon, ícones PWA e imagem de compartilhamento (`og-image.png`);
- `favicon.ico`, `site.webmanifest`, `robots.txt`, `sitemap.xml` — favicon, SEO e PWA;
- `waba/policy.html` — política para o WhatsApp Business API (WABA);
- `docs/` — materiais de marca (não publicados);
- `build.sh` — monta a pasta `dist/` publicada no Cloudflare Pages;
- `_headers` — headers de segurança e cache (formato Cloudflare Pages).

## Google (SEO)

O site já tem favicon nos formatos aceitos pelo Google (`/favicon.ico` 48px e PNGs múltiplos de 48),
dados estruturados (`WebSite` + `Organization`), `robots.txt`, `sitemap.xml`, URL canônica
`https://www.bitsoft.dev.br/` e página 404.

Após o deploy:

1. Configure o redirecionamento do domínio sem www (veja **Deploy no Cloudflare Pages**).
2. No [Google Search Console](https://search.google.com/search-console), adicione a propriedade
   do tipo **Domínio** `bitsoft.dev.br` e valide pelo registro TXT no DNS.
3. Em **Sitemaps**, envie `https://www.bitsoft.dev.br/sitemap.xml`.
4. Em **Inspeção de URL**, inspecione `https://www.bitsoft.dev.br/` e clique em **Solicitar indexação**.
5. Valide os dados estruturados em https://search.google.com/test/rich-results.

Ao alterar o conteúdo, atualize o `<lastmod>` do `sitemap.xml`.

## Formulário de contato (Web3Forms)

O formulário "Fale conosco" envia as mensagens pelo [Web3Forms](https://web3forms.com)
(plano gratuito: 250 envios/mês, sem backend). Para ativar:

1. Acesse https://web3forms.com, informe `contato@bitsoft.dev.br` em **Create your Access Key**.
2. Copie a Access Key recebida por e-mail e cole em `WEB3FORMS_ACCESS_KEY` no `script.js`.
3. (Opcional) No painel do Web3Forms, restrinja a chave ao domínio `bitsoft.dev.br`.

As mensagens chegam no e-mail cadastrado, com o remetente configurado como "responder para".
Enquanto a chave estiver vazia, o botão "Enviar mensagem" abre o programa de e-mail do visitante
com a mensagem já preenchida. O formulário tem proteção anti-spam por campo oculto (honeypot).

## WhatsApp

Defina o número em `script.js` (`WHATSAPP_NUMBER`, só dígitos com DDI e DDD, ex.: `5511999999999`).
Enquanto estiver vazio, os botões de WhatsApp ficam ocultos.

## Executar localmente

```bash
python3 -m http.server 8080
```

Acesse http://localhost:8080.

## Deploy no Cloudflare Pages

1. No painel do Cloudflare, em **Workers & Pages › Create › Pages**, conecte o repositório Git.
2. Configuração do build:
   - Framework preset: **None**
   - Build command: `sh build.sh`
   - Build output directory: `dist`
3. Em **Custom domains** do projeto, adicione `www.bitsoft.dev.br` e também `bitsoft.dev.br`.
4. Redirecione o domínio sem www para o www (o `_redirects` do Pages não faz redirecionamento entre domínios).
   Em **Rules › Redirect Rules** da zona `bitsoft.dev.br`, crie a regra:
   - Quando: *Hostname* igual a `bitsoft.dev.br`
   - Então: redirecionamento dinâmico para `concat("https://www.bitsoft.dev.br", http.request.uri.path)`,
     status **301**, preservando a query string.
5. Em **SSL/TLS › Edge Certificates**, ative **Always Use HTTPS**.

O `build.sh` copia só os arquivos públicos para `dist/`, então `docs/` não vai ao ar.
Como existe um `404.html`, o Pages responde com status 404 para endereços inexistentes.

> Dica: se a opção **Scrape Shield › Email Address Obfuscation** estiver ativa, o Cloudflare
> reescreve os links `mailto:`. Desative-a se preferir manter o e-mail como está no HTML.
