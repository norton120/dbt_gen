SELECT
    {{ mid_template_generate('%%DBT_GEN_DATABASE%%', '%%DBT_GEN_SCHEMA%%', '%%DBT_GEN_TABLE%%',except=[%%DBT_GEN_EXCEPTIONS%%]) }}

FROM
    "%%DBT_GEN_DATABASE%%"."%%DBT_GEN_SCHEMA%%"."%%DBT_GEN_TABLE%%"
