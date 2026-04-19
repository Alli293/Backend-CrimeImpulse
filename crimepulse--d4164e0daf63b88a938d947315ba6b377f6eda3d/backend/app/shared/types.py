"""Modelos de datos para CrimePulse."""

from typing import Literal

CrimeType = Literal[
    "homicidio",
    "femicidio",
    "agresión",
    "robo",
    "hurto",
    "tráfico_de_drogas",
    "posesión_de_drogas",
    "secuestro",
    "trata_de_personas",
    "extorsión",
    "fraude",
    "violencia_doméstica",
    "agresión_sexual",
    "robo_de_vehículo",
    "allanamiento",
    "vandalismo",
    "crimen_organizado",
    "corrupción",
    "persona_desaparecida",
    "otro",
]
