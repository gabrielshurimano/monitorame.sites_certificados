import { defineConfig, devices } from '@playwright/test';

/**
 * Configuração do Playwright para execução eficiente de testes automatizados.
 * Esse arquivo define o comportamento dos testes, como timeout, paralelismo e geração de relatórios.
 */

export default defineConfig({
  // 📂 Diretório onde estão localizados os arquivos de teste.
  testDir: './tests',

  // ⏳ Tempo máximo permitido para a execução TOTAL de todos os testes (aumentado para 5 minutos).
  globalTimeout: 300000, // 300000 ms = 5 minutos

  // 🚀 Define se os testes devem rodar totalmente em paralelo.
  fullyParallel: true, // Se "true", todos os testes são distribuídos entre os workers.

  // 🔄 Número de processos simultâneos para execução dos testes.
  // Quanto maior esse número, mais testes rodam ao mesmo tempo, acelerando a execução.
  // Se o computador for fraco, pode ser necessário reduzir esse valor.
  workers: 2, // Executa 4 testes simultaneamente

  // 📝 Define qual tipo de relatório será gerado após os testes.
  // O relatório HTML facilita a análise dos resultados.
  reporter: 'html', // Gera um relatório visual interativo em HTML

  use: {
    // 🔎 Ativa a captura de rastreamento (trace) em caso de falha para análise detalhada.
    trace: 'on-first-retry', // Só captura o trace na primeira falha, economizando recursos.

    // ⏱️ Define o tempo máximo que cada página pode levar para carregar antes de falhar.
    // Se um site demorar mais de 15s para responder, o teste será encerrado e marcado como erro.
    navigationTimeout: 30000, 
  },

  // 🌍 Configuração dos navegadores onde os testes serão executados.
  projects: [
    {
      name: 'chromium', // Executa os testes no Google Chrome
      use: { ...devices['Desktop Chrome'] }, // Configuração para ambiente de desktop
    }
  ],
});
