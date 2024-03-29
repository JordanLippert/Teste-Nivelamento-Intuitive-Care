SELECT 
    relatorio_cadop.Razao_Social AS Operadora,
    SUM(dados_tabela.VL_SALDO_FINAL - dados_tabela.VL_SALDO_INICIAL) AS Despesas
FROM 
    dados_tabela
INNER JOIN 
    relatorio_cadop ON dados_tabela.REG_ANS = relatorio_cadop.Registro_ANS
WHERE 
    (LOWER(dados_tabela.DESCRICAO) COLLATE utf8mb4_unicode_ci LIKE '%eventos/ sinistros conhecidos%' OR 
    LOWER(dados_tabela.DESCRICAO) COLLATE utf8mb4_unicode_ci LIKE '%avisados de assistencia a saude medico hospitalar%') AND 
    dados_tabela.DATA >= '2023-07-01'
GROUP BY 
    relatorio_cadop.Razao_Social
ORDER BY 
    Despesas DESC
LIMIT 
    10;