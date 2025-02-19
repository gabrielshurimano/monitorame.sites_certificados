# 🔍 Monitoramento de Status de Sistemas com Playwright

Este projeto utiliza **Playwright** para testar o status de múltiplos sistemas, verificando se eles estão online (`HTTP 200`). Ele carrega um arquivo **JSON** contendo a lista de sistemas e executa os testes de forma sequencial, garantindo eficiência mesmo em máquinas com menos recursos.

---

## 🚀 **Como Rodar o Projeto**

### 📌 **1. Pré-requisitos**
Antes de rodar o projeto, certifique-se de que você tem instalado:
- **Node.js** (versão 16 ou superior) → [Baixar aqui](https://nodejs.org/)
- **Playwright** instalado globalmente
- **WSL2** ou um ambiente Linux/macOS (se estiver no Windows)

### 📌 **2. Instalação do Projeto**
1️⃣ **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2️⃣ **Instale as dependências do projeto:**
```bash
npm install
```

3️⃣ **Instale os navegadores necessários para o Playwright:**
```bash
npx playwright install
```

---

## ⚙ **Configurações**
O projeto já está otimizado para rodar **com qualquer número de sistemas**, porém, algumas configurações podem ser ajustadas no arquivo **`playwright.config.ts`**.

| Configuração            | Padrão   | Descrição |
|------------------------|---------|-----------|
| `workers`             | `1`     | Número de testes executados simultaneamente (roda sequencialmente). |
| `globalTimeout`       | `300000` | Tempo máximo para execução de todos os testes (5 minutos). |
| `navigationTimeout`   | `15000`  | Tempo máximo que cada site pode levar para responder (15 segundos). |
| `reporter`           | `'html'` | Gera um relatório visual ao final dos testes. |

Se precisar modificar esses valores, edite **`playwright.config.ts`**.

---

## 📂 **Estrutura do Projeto**
```
📂 projeto-playwright
 ├── 📂 json
 │    ├── dominios.json  ✅ <--- Contém a lista de sistemas a serem testados
 ├── 📂 tests
 │    ├── status_sistemas.spec.ts  ✅ <--- Código principal dos testes
 ├── playwright.config.ts  ✅ <--- Arquivo de configuração do Playwright
 ├── package.json  ✅ <--- Dependências do projeto
 ├── README.md  ✅ <--- Documentação do projeto
```

---

## 📜 **Como Adicionar Sistemas para Teste**
Os sistemas a serem testados ficam no arquivo **`json/dominios.json`**.  
Cada sistema deve ser adicionado no formato abaixo:

```json
[
  { "nome": "Google", "url": "https://www.google.com" },
  { "nome": "YouTube", "url": "https://www.youtube.com" },
  { "nome": "GitHub", "url": "https://github.com" }
]
```
📌 **Adicione quantos sistemas quiser**, o Playwright irá gerenciar automaticamente os testes.

---

## 🏃 **Executando os Testes**
Para rodar os testes, basta executar o seguinte comando no terminal:
```bash
npx playwright test
```
➡ O Playwright irá rodar todos os testes e gerar um relatório ao final.

---

## 📊 **Gerando Relatório**
Após a execução, um relatório HTML será gerado automaticamente.  
Para visualizar o relatório, execute:
```bash
npx playwright show-report
```
Isso abrirá o relatório no navegador, mostrando quais sistemas passaram ou falharam no teste.

---

## 🛠 **Possíveis Erros e Soluções**
### ❌ Erro: `Error: duplicate test title "Verificando undefined"`
✅ **Solução:** Certifique-se de que o JSON está formatado corretamente e que as chaves dos sistemas estão como `"nome"` e `"url"`.  

### ❌ Erro: `ENOENT: no such file or directory, open '../json/dominios.json'`
✅ **Solução:** O arquivo `json/dominios.json` está faltando. Crie o arquivo e adicione sistemas no formato JSON.

### ❌ Erro: `Timeout Exceeded`
✅ **Solução:** Se os sites forem lentos, aumente `navigationTimeout` no `playwright.config.ts`, por exemplo:
```typescript
navigationTimeout: 30000, // Agora cada site tem até 30 segundos para responder
```

---

## 📌 **Personalizações**
Se desejar modificar o comportamento do teste, você pode:
- **Alterar o tempo máximo de execução dos testes:**  
  ```typescript
  globalTimeout: 600000, // Agora os testes podem rodar por até 10 minutos
  ```
- **Incluir novos sistemas:**  
  Basta editar o arquivo `json/dominios.json` e adicionar novas URLs.

---

## 💡 **Contribuindo**
Se quiser contribuir para o projeto:
1️⃣ **Faça um fork do repositório.**  
2️⃣ **Crie uma branch:**  
```bash
git checkout -b minha-feature
```
3️⃣ **Faça as modificações e commite:**  
```bash
git commit -m "Adicionando nova funcionalidade"
```
4️⃣ **Envie um pull request!**  

---

## 🏆 **Créditos**
Este projeto foi desenvolvido para **monitoramento de status de sistemas** de forma **rápida e eficiente**, utilizando **Playwright** para automação. Se gostou do projeto, **deixe uma estrela ⭐ no repositório!**

---

## 📩 **Contato**
📌 Se precisar de ajuda, entre em contato pelo e-mail:  
✉️ **seuemail@email.com**  
```

