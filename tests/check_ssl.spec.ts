import { test } from '@playwright/test';
import { execSync } from 'child_process';

// Lista de domínios a testar
const dominios = [
    "https://raumil.brisanet.net.br"
];

test.describe('Verificar segurança SSL dos sistemas', () => {
    for (const dominio of dominios) {
        test(`🔍 Testando SSL de: ${dominio}`, async () => {
            console.log(`\n🔍 Testando: ${dominio}`);

            // Executa o testssl.sh e captura a saída do terminal
            const output = execSync(`./testssl/testssl.sh -S -p -U ${dominio}`, { encoding: 'utf-8' });

            // Extrai os dados importantes da saída
            const certCommonNameMatch = output.match(/Common Name \(CN\)\s+([\S]+)/);
            const certDaysLeftMatch = output.match(/expires < \d+ days \((\d+)\)/);
            const certTrustStatusMatch = output.match(/Trust \(hostname\)\s+(.+)/);
            
            // Processa os dados capturados
            const certCommonName = certCommonNameMatch ? certCommonNameMatch[1] : "N/A";
            const certDaysLeft = certDaysLeftMatch ? certDaysLeftMatch[1] : "N/A";
            const certTrustStatus = certTrustStatusMatch ? certTrustStatusMatch[1].trim() : "N/A";

            // Exibe os resultados (sem duplicação)
            console.log("\n✅ **Resumo do Teste SSL** ✅");
            console.log(`- Host: ${dominio}`);
            console.log(`- Certificado Comum: ${certCommonName}`);
            console.log(`- Dias até Expiração: ${certDaysLeft}`);
            console.log(`- Status de Confiança: ${certTrustStatus}`);

            // Captura vulnerabilidades reais (sem "OK")
            const vulnerabilities = [...output.matchAll(/(potentially NOT ok|not vulnerable|vulnerable).*/g)]
                .map(match => match[0])
                .filter(v => !v.includes("(OK)")); // Remove linhas que contêm "(OK)"

            if (vulnerabilities.length > 0) {
                console.log("\n⚠ **Vulnerabilidades Encontradas:**");
                vulnerabilities.forEach(vuln => console.log(`- ${vuln.trim()}`));
            } else {
                console.log("\n✅ Nenhuma vulnerabilidade crítica encontrada.");
            }
        });
    }
});
