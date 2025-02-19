import {test, expect} from '@playwright/test';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

//BUSCANDO O JSON COM TODOS OS DOMINIONS QUE VAMOS QUERER TESTAR
const dominiospath = path.join(__dirname, '../json/dominios.json');

const dominiosJson = JSON.parse(fs.readFileSync(dominiospath, 'utf8'));
const dominios = dominiosJson.url;


test('Verificar segurança SSL dos sistemas', async ({}) => {
    for (const dominio of dominios ) {
        console.log(`Testando ${dominio}`);

        const jsonssl = `${dominio}_p443-*.json`;
        //RODANDO O TESTE
        execSync(`testssl.sh -S -p -U --json ${dominio}`, { stdio: 'inherit' });

         // Identifica o arquivo JSON gerado
        const files = fs.readdirSync('.').filter(file => file.match(new RegExp(jsonssl)));
        if (files.length === 0) {
            console.error(` Erro: Nenhum JSON gerado para ${dominio}`);
            continue;
        }

        const latestJson = files[0];
        console.log(`📂 Arquivo JSON identificado: ${latestJson}`);

         // Lê o JSON e extrai os dados necessários
         const jsonData = JSON.parse(fs.readFileSync(latestJson, 'utf8'));
         const scanResult = jsonData.scanResult[0];
 
         // Extrai as informações principais
         const host = scanResult.targetHost || "Desconhecido";
         const certCommonName = scanResult.serverDefaults.find(item => item.id === "cert_commonName")?.finding || "N/A";
         const certExpiration = scanResult.serverDefaults.find(item => item.id === "cert_expirationStatus")?.finding || "N/A";
         const certTrustStatus = scanResult.serverDefaults.find(item => item.id === "cert_trust")?.finding || "N/A";
 
         // Extrai vulnerabilidades encontradas
         const vulnerabilities = scanResult.vulnerabilities
             .filter(vuln => vuln.severity !== "OK") // Filtra apenas vulnerabilidades encontradas
             .map(vuln => ({ id: vuln.id, severity: vuln.severity, finding: vuln.finding }));
 
         // Exibe os resultados no console
         console.log("\n✅ **Resumo do Teste SSL** ✅");
         console.log(`- Host: ${host}`);
         console.log(`- Certificado Comum: ${certCommonName}`);
         console.log(`- Dias até Expiração: ${certExpiration}`);
         console.log(`- Status de Confiança: ${certTrustStatus}`);
 
         if (vulnerabilities.length > 0) {
             console.log("\n **Vulnerabilidades Encontradas:**");
             vulnerabilities.forEach(vuln => console.log(`- ${vuln.id} [${vuln.severity}]: ${vuln.finding}`));
         } else {
             console.log("\n✅ Nenhuma vulnerabilidade crítica encontrada.");
         }
 
         // Deleta o arquivo JSON gerado para manter o diretório limpo
         fs.unlinkSync(latestJson);
         console.log(`\n🗑️ Arquivo ${latestJson} removido.`);

    }
});