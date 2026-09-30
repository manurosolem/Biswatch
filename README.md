# Biswatch — cuidado que acompanha o tempo

## Interface pública

Foi adicionada uma landing page independente e responsiva na raiz do projeto:

- `index.html`: estrutura e conteúdo da página.
- `styles.css`: identidade visual, responsividade e modo escuro.
- `script.js`: menu mobile, tema e simulação de alerta.
- `server.py`: servidor local simples com endpoint `/api/health`.

Para visualizar:

```bash
python3 server.py
```

Depois, abra `http://localhost:8000` no navegador.

Biswatch é um protótipo funcional de uma plataforma para um relógio inteligente multifunções, voltado principalmente a pessoas idosas, pacientes e seus responsáveis/cuidadores. Além de organizar remédios, consultas e datas importantes, o produto foi pensado para ajudar com GPS, ligações para números escolhidos, voz, sensores e uma rede de segurança.

> **Importante:** esta versão é um protótipo de software. A simulação de alerta não substitui serviços de emergência, não faz diagnóstico médico e não afirma que uma mensagem foi enviada sem confirmação de um provedor oficial.

## O que já funciona

- Página pública em português, responsiva e com modo claro/escuro.
- Login e criação de conta reais via Manus OAuth; o app não cria senha falsa nem armazena senha localmente.
- Perfil de paciente ou responsável/cuidador, com nome e relação configuráveis.
- CRUD persistente de lembretes de remédios, consultas e datas importantes, incluindo edição, ativação/desativação e remoção.
- Apresentação de GPS/localização e chamadas rápidas como funções centrais do Biswatch; a integração com o relógio físico e a discagem nativa ficam preparadas para a próxima etapa.
- CRUD persistente de contatos de emergência, com relação, WhatsApp, prioridade e status ativo/pausado.
- Painel com resumo do dia, próximos lembretes e rede de segurança.
- Histórico de alertas manuais, de voz e de queda/pancada simulados.
- Configuração de voz da IA, velocidade, volume, idioma, tema e cor de destaque.
- Adaptador de WhatsApp por webhook protegido por variáveis de ambiente. Sem as variáveis, o alerta fica como **configuração pendente**.
- Manifesto de rotas em `client/public/manus-routes.json`.

## Stack

React, TypeScript, Vite, Express, tRPC, Drizzle ORM, MySQL-compatible database, Tailwind CSS e Vitest.

## Rodar localmente

Pré-requisitos: Node.js 22 ou compatível, pnpm 10.18 e uma instância MySQL-compatible quando quiser testar persistência.

```bash
pnpm install
cp .env.example .env
pnpm db:migrate
pnpm dev
```

O servidor inicia na porta `3000` por padrão e respeita a variável `PORT`.

Comandos úteis:

```bash
pnpm check       # TypeScript
pnpm test        # testes existentes
pnpm build       # build frontend + backend
pnpm start       # servir o build
pnpm db:migrate  # aplicar migrações versionadas
pnpm db:push     # gerar/aplicar mudanças Drizzle durante desenvolvimento
```

## Variáveis de ambiente

A plataforma gerenciada fornece `DATABASE_URL`, `MANUS_PROJECT_ID`, `MANUS_OAUTH_PORTAL_URL`, `MANUS_OAUTH_API_URL` e `MANUS_JWT_SECRET` no runtime. Para outro ambiente, configure esses nomes conforme o provedor escolhido.

Para preparar o envio por WhatsApp, configure somente no servidor:

```env
WHATSAPP_WEBHOOK_URL=https://seu-provedor-oficial.example/messages
WHATSAPP_API_TOKEN=seu-token-no-servidor
```

O adaptador envia um JSON no formato `{ "to": "+55...", "message": "..." }` quando a futura rotina de dispositivo chamar `sendWhatsAppMessage`. A simulação do painel não dispara mensagens reais; ela registra o evento e informa se a configuração está pendente.

Nunca coloque `.env`, tokens, dados de pacientes ou números reais de emergência no GitHub.

## Estrutura principal

- `client/src/App.tsx`: rotas, landing page, painel e telas de domínio.
- `client/src/index.css`: identidade visual Biswatch e responsividade.
- `server/routers.ts`: procedures protegidas de conta, lembretes, contatos e alertas.
- `server/db.ts`: conexão e queries com escopo do usuário/vínculos.
- `server/integrations/whatsapp.ts`: status e adaptador de mensagens.
- `drizzle/schema.ts`: tabelas de usuários, perfis, vínculos, lembretes, contatos e alertas.
- `client/public/manus-routes.json`: contrato de rotas da aplicação.
- `ideas.md`: direção visual aprovada.
- `.env.example`: nomes das variáveis sem segredos.

## Subir ao GitHub

Dentro desta pasta:

```bash
git init
git add .
git commit -m "feat: criar prototipo Biswatch"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/biswatch.git
git push -u origin main
```

Se o repositório já existir, use o remote dele e não versiona `node_modules`, `dist` ou `.env`; o `.gitignore` já cobre esses arquivos.

## Próximas etapas recomendadas

1. Escolher um provedor oficial de WhatsApp e configurar suas credenciais no servidor.
2. Criar o endpoint autenticado que receberá eventos assinados do relógio.
3. Integrar transcrição de áudio e uma regra de detecção de palavras de ajuda com confirmação do paciente para reduzir falsos positivos.
4. Integrar acelerômetro/giroscópio para quedas, com janela de cancelamento e confirmação.
5. Implementar consentimentos, auditoria, retenção de dados e revisão jurídica/regulatória antes de uso real.
