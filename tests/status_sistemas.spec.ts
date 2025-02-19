// import { test, expect } from '@playwright/test';
// import fs from 'fs';
// //com ele vamos manupular o caminho para sempre termos o caminho absoluto de alguns arquivos
// import path from 'path'; 

// //AQUI NÓS VAMOS LER O JSON ONDE CONTEM OS DOMINIOS E SEM SEGUIDA CONVERTER EM UM ARRAY
// const localPath = path.join(__dirname, '../json/dominios.json');
// const jsondominios = fs.readFileSync(localPath,'utf8');
// const sistemas: {sistema: string; url: string} [] = JSON.parse(jsondominios);

// //TESTE ONDE DE FATO OCORRE A VALIDAÇÃO DE STATUS DE CADA SISTEMA
// test.describe('verificando status dos sistemas', () => {
//     for (const sistema of sistemas) {
//         test(`Verificando ${sistema.sistema}`, async ({page}) => {
//             const response = await page.goto(sistema.url);

//             //VALINDO O STATUS DA PÁGINA
//             expect(response).not.toBeNull();
//             expect(response?.status()).toBe(200);

//             console.log(`${sistema.sistema} está no ar`);
//         });
//     }
// });