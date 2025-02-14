#!/usr/bin/env python
# coding: utf-8

# # Candidatos a prefeito, doações e doadores
#
# A partir dos dados da prestação de contas das eleições feitas ao Tribunal Superior
# Eleitoral (TSE) analisamos os dados das doações recebidas por candidatos a prefeitura
# de Feira de Santana. Apesar de saber que esse ano as doações vindas de empresas
# não são permitidas, [sabemos que não é o fim delas](https://twitter.com/fecampa/status/1325791183554154498?s=20).
#
# Vale salientar que os dados são atualizados pelo TSE diariamente. Atenção a data
# que essa análise foi publicada e a data de _download_ do arquivo.
#
# ### Instruções download dos dados
#
# A análise foi feita com arquivos do [repositório de dados eleitorais do TSE](https://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais).
#
# Faça o download do arquivo: https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2020.zip (download feito em 16/10/2021)
#
# Siga o seguinte caminho dentro da pasta:
# ```
# Prestação de contas eleitorais > 2020 > Candidatos (formato zip) > receitas_candidatos_2020_BA.csv
# ```
#
# Copie o arquivo do estado desejado (`receitas_candidatos_2020_<estado>.csv`)
# para a pasta `analysis` nesse repositório.
#
# Dicionário de dados: `leiame_receitas-candidatos.pdf`
#
# Observações sobre os dados:
#
# * `#NULO` é o mesmo que `None` ou vazio
# * `#NE` significa que naquele ano a informação não era registrada
# * Campo `UF`: `BR` para nível nacional, `VT` voto em trânsito e `ZZ` para Exterior
# * Campo `NM_UE`, no caso de eleições municipais, é o nome do município

# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scripts.parsers import currency_to_float, is_company

df = pd.read_csv(
    "receitas_candidatos_2020_BA-16.10.2020.csv", encoding="latin", delimiter=";"
)


# In[ ]:


pd.set_option("display.max_rows", None)


# In[ ]:


# In[ ]:


df_feira = df[df["NM_UE"] == "FEIRA DE SANTANA"].copy()


# In[ ]:


df_feira["VR_RECEITA"] = df_feira["VR_RECEITA"].apply(currency_to_float)


# In[ ]:


fields = [
    "NM_CANDIDATO",
    "SG_PARTIDO",
    "DS_FONTE_RECEITA",
    "DS_ORIGEM_RECEITA",
    "NR_CPF_CNPJ_DOADOR",
    "NM_DOADOR",
    "NM_DOADOR_RFB",
    "DS_CARGO",
    "NM_MUNICIPIO_DOADOR",
    "NM_PARTIDO_DOADOR",
    "DT_RECEITA",
    "DS_RECEITA",
    "VR_RECEITA",
]

df_filtered = df_feira[fields]


# Para melhorar a experiência das pessoas na visualização dos dados vamos substituir
# o valor "#NULO#" por vazio.

# In[ ]:


df_filtered = df_filtered.replace("#NULO#", "").copy()
df_filtered[df_filtered["NM_PARTIDO_DOADOR"] == "#NULO#"]


# ## Doações recebidas por candidatos a prefeito
#
# Vamos filtrar as doações feitas para prefeitos.
# Ao final dessa página você poderá ver a lista com todos as doações
# recebidas pelos candidatos a prefeito na cidade de Feira de Santana.
#
# Abaixo uma amostra aleatória de 5 doações recebidas:

# In[ ]:


mayor_df = df_filtered[df_filtered["DS_CARGO"] == "Prefeito"]
mayor_df.sample(5)  # amostra das doações a prefeitos de Feira de Santana


# ### Total, mediana e número de doações recebidas por candidato

# In[ ]:


statistics = (
    mayor_df.groupby(["NM_CANDIDATO"])["VR_RECEITA"]
    .agg(["sum", "median", "count"])
    .sort_values(ascending=False, by=["sum", "NM_CANDIDATO"])
)
statistics


# In[ ]:


ax = sns.histplot(data=statistics, x="sum")
ax.set_xlabel("Valor em R$")
ax.set_ylabel("Número de doações")
ax.set_title("Distribuição das doações recebidas por candidato")
ax.xaxis.get_major_formatter().set_scientific(False)
plt.xticks(rotation=45)


# In[ ]:


ax = sns.barplot(
    x="VR_RECEITA",
    y="NM_CANDIDATO",
    data=mayor_df,
    palette="Blues_d",
    ci=None,
    estimator=sum,
)
ax.set_xlabel("Doações em R$")
ax.set_ylabel("Candidatos")
ax.set_title("Gráfico do total das doações recebidas por candidatos")
ax.xaxis.get_major_formatter().set_scientific(False)
plt.xticks(rotation=45)


# ## Quem são os doadores?

# In[ ]:


mayor_df.groupby(
    [
        "NM_CANDIDATO",
        "NM_DOADOR_RFB",
        "NR_CPF_CNPJ_DOADOR",
        "NM_PARTIDO_DOADOR",
        "NM_MUNICIPIO_DOADOR",
    ]
)["VR_RECEITA"].agg(["sum"])


# ### Qual a origem dos recursos?

# In[ ]:


ax = sns.stripplot(
    x="NM_CANDIDATO", y="VR_RECEITA", hue="DS_ORIGEM_RECEITA", data=mayor_df
)

ax.set_xlabel("Candidato")
ax.set_ylabel("R$")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)


# Entre os candidatos podemos ver diferenças na distribuição da origem das receitas.
#
# O candidato CARLOS MEDEIROS MIRANDA (Novo) recebeu doações diversificadas de pessoas
# físicas. Enquanto DAYANE JAMILLE CARNEIRO DOS SANTOS PIMENTEL recebeu massivamente doações
# vindas do seu partido (PSL), tudo indica que graças ao fundão eleitoral ([o PSL recebeu o segundo
# maior montante dessas eleições, com cerca de 199 milhões de reais](https://www.tse.jus.br/imprensa/noticias-tse/2020/Junho/divulgada-nova-tabela-com-a-divisao-dos-recursos-do-fundo-eleitoral-para-2020)).
#
# A candidata que se destacou no recebimento de recursos de financiamento coletivo,
# modalidade que ainda não é muito popular dentre os outros candidatos, foi a MARCELA PREST (PSOL).
#
# O candidato JOSE CERQUEIRA DE SANTANA NETO foi quem mais investiu em sua campanha a partir de recursos próprios,
# seguido do candidato CARLOS GEILSON DOS SANTOS SILVA.
#
# ### Veja os valores por candidato e origem

# In[ ]:


mayor_df.groupby(["NM_CANDIDATO", "DS_ORIGEM_RECEITA"])["VR_RECEITA"].agg(["sum"])


# ## Ranking de Doadores

# In[ ]:


mayor_df.groupby(["NM_DOADOR_RFB", "NM_DOADOR"])["VR_RECEITA"].agg(["sum"]).sort_values(
    ascending=False, by=["sum", "NM_DOADOR_RFB"]
)


# ## As pessoas que doaram estão ligadas a empresas diretamente?

# In[ ]:


def mask_cpf(cpf):
    """Útil para busca dos sócios em empresas no Brasil.io."""
    cpf = str(cpf)
    return f"***{cpf[3:9]}**"


mayor_df_copy = mayor_df.copy()
mayor_df_copy["DONATED_BY_CNPJ"] = mayor_df_copy["NR_CPF_CNPJ_DOADOR"].apply(is_company)

donated_by_people = mayor_df_copy[mayor_df_copy["DONATED_BY_CNPJ"] == False]
donated_by_people = donated_by_people[
    donated_by_people["NM_CANDIDATO"] != donated_by_people["NM_DOADOR_RFB"]
]
donated_by_people["CPF_MASCARADO"] = mayor_df_copy["NR_CPF_CNPJ_DOADOR"].apply(mask_cpf)
donated_by_people[
    ["NM_CANDIDATO", "NM_DOADOR_RFB", "NR_CPF_CNPJ_DOADOR", "CPF_MASCARADO"]
]


# Para verificar se os doadores são sócios em empresas, basta acessar
# https://brasil.io/dataset/socios-brasil/socios/ e buscar pelo nome completo e CPF mascarado
# campos `Nome/Razão Social do Sócio` e `CPF/CNPJ do Sócio`.
#
# Para confirmar as informações, verifique se o CPF mascarado que você buscou bate com o
# CPF mostrado e com o nome completo da página para confirmar.
#
# Exemplo:
#
# https://brasil.io/dataset/socios-brasil/socios/?search=&cnpj=&razao_social=&cpf_cnpj_socio=***092875**&nome_socio=WILSON+FERREIRA+FALCAO&tipo_socio=&qualificacao_socio=

# ## Qual partido é mais generoso?
#
# As doações feitas por partidas podem ser identificadas pela coluna `NM_PARTIDO_DOADOR`.
# O valor `#NULO#` representa as doações feitas por todas as outras entidades que não são
# partidos (como pessoas e aplicativos de doação).

# In[ ]:


donations_by_party = (
    mayor_df[mayor_df["NM_PARTIDO_DOADOR"] != ""]
    .groupby(["NM_PARTIDO_DOADOR"], as_index=False)["VR_RECEITA"]
    .agg({"Total": sum})
    .sort_values(ascending=False, by=["Total", "NM_PARTIDO_DOADOR"])
)
donations_by_party


# In[ ]:


ax = sns.barplot(
    x="Total", y="NM_PARTIDO_DOADOR", data=donations_by_party, ci=None, estimator=sum
)
ax.set_xlabel("Doações em R$")
ax.set_ylabel("Partidos")
ax.set_title("Gráfico das doações por partido")
ax.xaxis.get_major_formatter().set_scientific(False)
plt.xticks(rotation=45)


# ## Veja todas as doações

# In[ ]:


mayor_df
