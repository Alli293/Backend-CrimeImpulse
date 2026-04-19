"""Geolocations for Costa Rica."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class AlajuelaAlajuelaLocation(BaseModel):
    """Location for Alajuela, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Alajuela"] = "Alajuela"
    district: (
        list[
            Literal[
                "Alajuela",
                "San José",
                "Carrizal",
                "San Antonio",
                "Guácima",
                "San Isidro",
                "Sabanilla",
                "San Rafael",
                "Río Segundo",
                "Desamparados",
                "Turrúcares",
                "Tambor",
                "Garita",
                "Sarapiquí",
            ]
        ]
        | None
    ) = None


class AlajuelaSanRamonLocation(BaseModel):
    """Location for San Ramón, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["San Ramón"] = "San Ramón"
    district: (
        list[
            Literal[
                "San Ramón",
                "Santiago",
                "San Juan",
                "Piedades Norte",
                "Piedades Sur",
                "San Rafael",
                "San Isidro",
                "Ángeles",
                "Alfaro",
                "Volio",
                "Concepción",
                "Zapotal",
                "Peñas Blancas",
                "San Lorenzo",
            ]
        ]
        | None
    ) = None


class AlajuelaGreciaLocation(BaseModel):
    """Location for Grecia, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Grecia"] = "Grecia"
    district: (
        list[
            Literal[
                "Grecia",
                "San Isidro",
                "San José",
                "San Roque",
                "Tacares",
                "Puente de Piedra",
                "Bolívar",
            ]
        ]
        | None
    ) = None


class AlajuelaSanMateoLocation(BaseModel):
    """Location for San Mateo, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["San Mateo"] = "San Mateo"
    district: (
        list[Literal["San Mateo", "Desmonte", "Jesús María", "Labrador"]] | None
    ) = None


class AlajuelaAtenasLocation(BaseModel):
    """Location for Atenas, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Atenas"] = "Atenas"
    district: (
        list[
            Literal[
                "Atenas",
                "Jesús",
                "Mercedes",
                "San Isidro",
                "Concepción",
                "San José",
                "Santa Eulalia",
                "Escobal",
            ]
        ]
        | None
    ) = None


class AlajuelaNaranjoLocation(BaseModel):
    """Location for Naranjo, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Naranjo"] = "Naranjo"
    district: (
        list[
            Literal[
                "Naranjo",
                "San Miguel",
                "San José",
                "Cirrí Sur",
                "San Jerónimo",
                "San Juan",
                "El Rosario",
                "Palmitos",
            ]
        ]
        | None
    ) = None


class AlajuelaPalmaresLocation(BaseModel):
    """Location for Palmares, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Palmares"] = "Palmares"
    district: (
        list[
            Literal[
                "Palmares",
                "Zaragoza",
                "Buenos Aires",
                "Santiago",
                "Candelaria",
                "Esquipulas",
                "La Granja",
            ]
        ]
        | None
    ) = None


class AlajuelaPoasLocation(BaseModel):
    """Location for Poás, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Poás"] = "Poás"
    district: (
        list[
            Literal[
                "San Pedro", "San Juan", "San Rafael", "Carrillos", "Sabana Redonda"
            ]
        ]
        | None
    ) = None


class AlajuelaOrotinaLocation(BaseModel):
    """Location for Orotina, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Orotina"] = "Orotina"
    district: (
        list[Literal["Orotina", "El Mastate", "Hacienda Vieja", "Coyolar", "La Ceiba"]]
        | None
    ) = None


class AlajuelaSanCarlosLocation(BaseModel):
    """Location for San Carlos, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["San Carlos"] = "San Carlos"
    district: (
        list[
            Literal[
                "Quesada",
                "Florencia",
                "Buenavista",
                "Aguas Zarcas",
                "Venecia",
                "Pital",
                "La Fortuna",
                "La Tigra",
                "La Palmera",
                "Venado",
                "Cutris",
                "Monterrey",
                "Pocosol",
            ]
        ]
        | None
    ) = None


class AlajuelaZarceroLocation(BaseModel):
    """Location for Zarcero, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Zarcero"] = "Zarcero"
    district: (
        list[
            Literal[
                "Zarcero",
                "Laguna",
                "Tapesco",
                "Guadalupe",
                "Palmira",
                "Zapote",
                "Brisas",
            ]
        ]
        | None
    ) = None


class AlajuelaSarchiLocation(BaseModel):
    """Location for Sarchí, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Sarchí"] = "Sarchí"
    district: (
        list[
            Literal[
                "Sarchí Norte", "Sarchí Sur", "Toro Amarillo", "San Pedro", "Rodríguez"
            ]
        ]
        | None
    ) = None


class AlajuelaUpalaLocation(BaseModel):
    """Location for Upala, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Upala"] = "Upala"
    district: (
        list[
            Literal[
                "Upala",
                "Aguas Claras",
                "San José",
                "Bijagua",
                "Delicias",
                "Dos Ríos",
                "Yolillal",
                "Canalete",
            ]
        ]
        | None
    ) = None


class AlajuelaLosChilesLocation(BaseModel):
    """Location for Los Chiles, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Los Chiles"] = "Los Chiles"
    district: (
        list[Literal["Los Chiles", "Caño Negro", "El Amparo", "San Jorge"]] | None
    ) = None


class AlajuelaGuatusoLocation(BaseModel):
    """Location for Guatuso, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Guatuso"] = "Guatuso"
    district: list[Literal["San Rafael", "Buenavista", "Cote", "Katira"]] | None = None


class AlajuelaRioCuartoLocation(BaseModel):
    """Location for Río Cuarto, Alajuela."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Alajuela"] = "Alajuela"
    canton: Literal["Río Cuarto"] = "Río Cuarto"
    district: list[Literal["Río Cuarto", "Santa Rita", "Santa Isabel"]] | None = None


class CartagoCartagoLocation(BaseModel):
    """Location for Cartago, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["Cartago"] = "Cartago"
    district: (
        list[
            Literal[
                "Oriental",
                "Occidental",
                "Carmen",
                "San Nicolás",
                "Aguacaliente",
                "Guadalupe",
                "Corralillo",
                "Tierra Blanca",
                "Dulce Nombre",
                "Llano Grande",
                "Quebradilla",
            ]
        ]
        | None
    ) = None


class CartagoParaisoLocation(BaseModel):
    """Location for Paraíso, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["Paraíso"] = "Paraíso"
    district: (
        list[
            Literal[
                "Paraíso",
                "Santiago",
                "Orosi",
                "Cachí",
                "Llanos de Santa Lucía",
                "Birrisito",
            ]
        ]
        | None
    ) = None


class CartagoLaUnionLocation(BaseModel):
    """Location for La Unión, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["La Unión"] = "La Unión"
    district: (
        list[
            Literal[
                "Tres Ríos",
                "San Diego",
                "San Juan",
                "San Rafael",
                "Concepción",
                "Dulce Nombre",
                "San Ramón",
                "Río Azul",
            ]
        ]
        | None
    ) = None


class CartagoJimenezLocation(BaseModel):
    """Location for Jiménez, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["Jiménez"] = "Jiménez"
    district: (
        list[Literal["Juan Viñas", "Tucurrique", "Pejibaye", "La Victoria"]] | None
    ) = None


class CartagoTurrialbaLocation(BaseModel):
    """Location for Turrialba, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["Turrialba"] = "Turrialba"
    district: (
        list[
            Literal[
                "Turrialba",
                "La Suiza",
                "Peralta",
                "Santa Cruz",
                "Santa Teresita",
                "Pavones",
                "Tuis",
                "Tayutic",
                "Santa Rosa",
                "Tres Equis",
                "La Isabel",
                "Chirripó",
            ]
        ]
        | None
    ) = None


class CartagoAlvaradoLocation(BaseModel):
    """Location for Alvarado, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["Alvarado"] = "Alvarado"
    district: list[Literal["Pacayas", "Cervantes", "Capellades"]] | None = None


class CartagoOreamunoLocation(BaseModel):
    """Location for Oreamuno, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["Oreamuno"] = "Oreamuno"
    district: (
        list[Literal["San Rafael", "Cot", "Potrero Cerrado", "Cipreses", "Santa Rosa"]]
        | None
    ) = None


class CartagoElGuarcoLocation(BaseModel):
    """Location for El Guarco, Cartago."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Cartago"] = "Cartago"
    canton: Literal["El Guarco"] = "El Guarco"
    district: (
        list[Literal["El Tejar", "San Isidro", "Tobosi", "Patio de Agua"]] | None
    ) = None


class GuanacasteLiberiaLocation(BaseModel):
    """Location for Liberia, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Liberia"] = "Liberia"
    district: (
        list[Literal["Liberia", "Cañas Dulces", "Mayorga", "Nacascolo", "Curubandé"]]
        | None
    ) = None


class GuanacasteNicoyaLocation(BaseModel):
    """Location for Nicoya, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Nicoya"] = "Nicoya"
    district: (
        list[
            Literal[
                "Nicoya",
                "Mansión",
                "San Antonio",
                "Quebrada Honda",
                "Sámara",
                "Nosara",
                "Belén de Nosarita",
            ]
        ]
        | None
    ) = None


class GuanacasteSantaCruzLocation(BaseModel):
    """Location for Santa Cruz, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Santa Cruz"] = "Santa Cruz"
    district: (
        list[
            Literal[
                "Santa Cruz",
                "Bolsón",
                "Veintisiete de Abril",
                "Tempate",
                "Cartagena",
                "Cuajiniquil",
                "Diriá",
                "Cabo Velas",
                "Tamarindo",
            ]
        ]
        | None
    ) = None


class GuanacasteBagacesLocation(BaseModel):
    """Location for Bagaces, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Bagaces"] = "Bagaces"
    district: list[Literal["Bagaces", "La Fortuna", "Mogote", "Río Naranjo"]] | None = (
        None
    )


class GuanacasteCarrilloLocation(BaseModel):
    """Location for Carrillo, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Carrillo"] = "Carrillo"
    district: list[Literal["Filadelfia", "Palmira", "Sardinal", "Belén"]] | None = None


class GuanacasteCanasLocation(BaseModel):
    """Location for Cañas, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Cañas"] = "Cañas"
    district: (
        list[Literal["Cañas", "Palmira", "San Miguel", "Bebedero", "Porozal"]] | None
    ) = None


class GuanacasteAbangaresLocation(BaseModel):
    """Location for Abangares, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Abangares"] = "Abangares"
    district: list[Literal["Las Juntas", "Sierra", "San Juan", "Colorado"]] | None = (
        None
    )


class GuanacasteTilaranLocation(BaseModel):
    """Location for Tilarán, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Tilarán"] = "Tilarán"
    district: (
        list[
            Literal[
                "Tilarán",
                "Quebrada Grande",
                "Tronadora",
                "Santa Rosa",
                "Líbano",
                "Tierras Morenas",
                "Arenal",
                "Cabeceras",
            ]
        ]
        | None
    ) = None


class GuanacasteNandayureLocation(BaseModel):
    """Location for Nandayure, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Nandayure"] = "Nandayure"
    district: (
        list[
            Literal[
                "Carmona", "Santa Rita", "Zapotal", "San Pablo", "Porvenir", "Bejuco"
            ]
        ]
        | None
    ) = None


class GuanacasteLaCruzLocation(BaseModel):
    """Location for La Cruz, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["La Cruz"] = "La Cruz"
    district: (
        list[Literal["La Cruz", "Santa Cecilia", "La Garita", "Santa Elena"]] | None
    ) = None


class GuanacasteHojanchaLocation(BaseModel):
    """Location for Hojancha, Guanacaste."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Guanacaste"] = "Guanacaste"
    canton: Literal["Hojancha"] = "Hojancha"
    district: (
        list[Literal["Hojancha", "Monte Romo", "Puerto Carrillo", "Huacas", "Matambú"]]
        | None
    ) = None


class HerediaHerediaLocation(BaseModel):
    """Location for Heredia, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Heredia"] = "Heredia"
    district: (
        list[Literal["Heredia", "Mercedes", "San Francisco", "Ulloa", "Varablanca"]]
        | None
    ) = None


class HerediaBarvaLocation(BaseModel):
    """Location for Barva, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Barva"] = "Barva"
    district: (
        list[
            Literal[
                "Barva",
                "San Pedro",
                "San Pablo",
                "San Roque",
                "Santa Lucía",
                "San José de la Montaña",
                "Puente Salas",
            ]
        ]
        | None
    ) = None


class HerediaSantoDomingoLocation(BaseModel):
    """Location for Santo Domingo, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Santo Domingo"] = "Santo Domingo"
    district: (
        list[
            Literal[
                "Santo Domingo",
                "San Vicente",
                "San Miguel",
                "Paracito",
                "Santo Tomás",
                "Santa Rosa",
                "Tures",
                "Pará",
            ]
        ]
        | None
    ) = None


class HerediaSantaBarbaraLocation(BaseModel):
    """Location for Santa Bárbara, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Santa Bárbara"] = "Santa Bárbara"
    district: (
        list[
            Literal[
                "Santa Bárbara",
                "San Pedro",
                "San Juan",
                "Jesús",
                "Santo Domingo",
                "Purabá",
            ]
        ]
        | None
    ) = None


class HerediaSanRafaelLocation(BaseModel):
    """Location for San Rafael, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["San Rafael"] = "San Rafael"
    district: (
        list[Literal["San Rafael", "San Josecito", "Santiago", "Ángeles", "Concepción"]]
        | None
    ) = None


class HerediaSanIsidroLocation(BaseModel):
    """Location for San Isidro, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["San Isidro"] = "San Isidro"
    district: (
        list[Literal["San Isidro", "San José", "Concepción", "San Francisco"]] | None
    ) = None


class HerediaBelenLocation(BaseModel):
    """Location for Belén, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Belén"] = "Belén"
    district: list[Literal["San Antonio", "La Ribera", "La Asunción"]] | None = None


class HerediaFloresLocation(BaseModel):
    """Location for Flores, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Flores"] = "Flores"
    district: list[Literal["San Joaquín", "Barrantes", "Llorente"]] | None = None


class HerediaSanPabloLocation(BaseModel):
    """Location for San Pablo, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["San Pablo"] = "San Pablo"
    district: list[Literal["San Pablo", "Rincón de Sabanilla"]] | None = None


class HerediaSarapiquiLocation(BaseModel):
    """Location for Sarapiquí, Heredia."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Heredia"] = "Heredia"
    canton: Literal["Sarapiquí"] = "Sarapiquí"
    district: (
        list[
            Literal[
                "Puerto Viejo",
                "La Virgen",
                "Las Horquetas",
                "Llanuras del Gaspar",
                "Cureña",
            ]
        ]
        | None
    ) = None


class LimonLimonLocation(BaseModel):
    """Location for Limón, Limón."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Limón"] = "Limón"
    canton: Literal["Limón"] = "Limón"
    district: (
        list[Literal["Limón", "Valle La Estrella", "Río Blanco", "Matama"]] | None
    ) = None


class LimonPocociLocation(BaseModel):
    """Location for Pococí, Limón."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Limón"] = "Limón"
    canton: Literal["Pococí"] = "Pococí"
    district: (
        list[
            Literal[
                "Guápiles",
                "Jiménez",
                "Rita",
                "Roxana",
                "Cariari",
                "Colorado",
                "La Colonia",
            ]
        ]
        | None
    ) = None


class LimonSiquirresLocation(BaseModel):
    """Location for Siquirres, Limón."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Limón"] = "Limón"
    canton: Literal["Siquirres"] = "Siquirres"
    district: (
        list[
            Literal[
                "Siquirres",
                "Pacuarito",
                "Florida",
                "Germania",
                "El Cairo",
                "Alegría",
                "Reventazón",
            ]
        ]
        | None
    ) = None


class LimonTalamancaLocation(BaseModel):
    """Location for Talamanca, Limón."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Limón"] = "Limón"
    canton: Literal["Talamanca"] = "Talamanca"
    district: list[Literal["Bratsi", "Sixaola", "Cahuita", "Telire"]] | None = None


class LimonMatinaLocation(BaseModel):
    """Location for Matina, Limón."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Limón"] = "Limón"
    canton: Literal["Matina"] = "Matina"
    district: list[Literal["Matina", "Batán", "Carrandi"]] | None = None


class LimonGuacimoLocation(BaseModel):
    """Location for Guácimo, Limón."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Limón"] = "Limón"
    canton: Literal["Guácimo"] = "Guácimo"
    district: (
        list[Literal["Guácimo", "Mercedes", "Pocora", "Río Jiménez", "Duacarí"]] | None
    ) = None


class PuntarenasPuntarenasLocation(BaseModel):
    """Location for Puntarenas, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Puntarenas"] = "Puntarenas"
    district: (
        list[
            Literal[
                "Puntarenas",
                "Pitahaya",
                "Chomes",
                "Lepanto",
                "Paquera",
                "Manzanillo",
                "Guacimal",
                "Barranca",
                "Isla del Coco",
                "Cóbano",
                "Chacarita",
                "Chira",
                "Acapulco",
                "El Roble",
                "Arancibia",
            ]
        ]
        | None
    ) = None


class PuntarenasEsparzaLocation(BaseModel):
    """Location for Esparza, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Esparza"] = "Esparza"
    district: (
        list[
            Literal[
                "Espíritu Santo",
                "San Juan Grande",
                "Macacona",
                "San Rafael",
                "San Jerónimo",
                "Caldera",
            ]
        ]
        | None
    ) = None


class PuntarenasBuenosAiresLocation(BaseModel):
    """Location for Buenos Aires, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Buenos Aires"] = "Buenos Aires"
    district: (
        list[
            Literal[
                "Buenos Aires",
                "Volcán",
                "Potrero Grande",
                "Boruca",
                "Pilas",
                "Colinas",
                "Chánguena",
                "Biolley",
                "Brunka",
            ]
        ]
        | None
    ) = None


class PuntarenasMontesdeOroLocation(BaseModel):
    """Location for Montes de Oro, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Montes de Oro"] = "Montes de Oro"
    district: list[Literal["Miramar", "La Unión", "San Isidro"]] | None = None


class PuntarenasOsaLocation(BaseModel):
    """Location for Osa, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Osa"] = "Osa"
    district: (
        list[
            Literal[
                "Puerto Cortés",
                "Palmar",
                "Sierpe",
                "Bahía Ballena",
                "Piedras Blancas",
                "Bahía Drake",
            ]
        ]
        | None
    ) = None


class PuntarenasQueposLocation(BaseModel):
    """Location for Quepos, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Quepos"] = "Quepos"
    district: list[Literal["Quepos", "Savegre", "Naranjito"]] | None = None


class PuntarenasGolfitoLocation(BaseModel):
    """Location for Golfito, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Golfito"] = "Golfito"
    district: list[Literal["Golfito", "Guaycará", "Pavón"]] | None = None


class PuntarenasCotoBrusLocation(BaseModel):
    """Location for Coto Brus, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Coto Brus"] = "Coto Brus"
    district: (
        list[
            Literal[
                "San Vito",
                "Sabalito",
                "Aguabuena",
                "Limoncito",
                "Pittier",
                "Gutiérrez Braun",
            ]
        ]
        | None
    ) = None


class PuntarenasParritaLocation(BaseModel):
    """Location for Parrita, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Parrita"] = "Parrita"
    district: list[Literal["Parrita"]] | None = None


class PuntarenasCorredoresLocation(BaseModel):
    """Location for Corredores, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Corredores"] = "Corredores"
    district: list[Literal["Corredor", "La Cuesta", "Canoas", "Laurel"]] | None = None


class PuntarenasGarabitoLocation(BaseModel):
    """Location for Garabito, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Garabito"] = "Garabito"
    district: list[Literal["Jacó", "Tárcoles"]] | None = None


class PuntarenasMonteverdeLocation(BaseModel):
    """Location for Monteverde, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Monteverde"] = "Monteverde"
    district: list[Literal["Monteverde"]] | None = None


class PuntarenasPuertoJimenezLocation(BaseModel):
    """Location for Puerto Jiménez, Puntarenas."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["Puntarenas"] = "Puntarenas"
    canton: Literal["Puerto Jiménez"] = "Puerto Jiménez"
    district: list[Literal["Puerto Jiménez"]] | None = None


class SanJoseSanJoseLocation(BaseModel):
    """Location for San José, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["San José"] = "San José"
    district: (
        list[
            Literal[
                "Carmen",
                "Merced",
                "Hospital",
                "Catedral",
                "Zapote",
                "San Francisco de Dos Ríos",
                "Uruca",
                "Mata Redonda",
                "Pavas",
                "Hatillo",
                "San Sebastián",
            ]
        ]
        | None
    ) = None


class SanJoseEscazuLocation(BaseModel):
    """Location for Escazú, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Escazú"] = "Escazú"
    district: list[Literal["Escazú", "San Antonio", "San Rafael"]] | None = None


class SanJoseDesamparadosLocation(BaseModel):
    """Location for Desamparados, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Desamparados"] = "Desamparados"
    district: (
        list[
            Literal[
                "Desamparados",
                "San Miguel",
                "San Juan de Dios",
                "San Rafael Arriba",
                "San Antonio",
                "Frailes",
                "Patarrá",
                "San Cristóbal",
                "Rosario",
                "Damas",
                "San Rafael Abajo",
                "Gravilias",
                "Los Guido",
            ]
        ]
        | None
    ) = None


class SanJosePuriscalLocation(BaseModel):
    """Location for Puriscal, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Puriscal"] = "Puriscal"
    district: (
        list[
            Literal[
                "Santiago",
                "Mercedes Sur",
                "Barbacoas",
                "Grifo Alto",
                "San Rafael",
                "Candelarita",
                "Desamparaditos",
                "San Antonio",
                "Chires",
            ]
        ]
        | None
    ) = None


class SanJoseTarrazuLocation(BaseModel):
    """Location for Tarrazú, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Tarrazú"] = "Tarrazú"
    district: list[Literal["San Marcos", "San Lorenzo", "San Carlos"]] | None = None


class SanJoseAserriLocation(BaseModel):
    """Location for Aserrí, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Aserrí"] = "Aserrí"
    district: (
        list[
            Literal[
                "Aserrí",
                "Tarbaca",
                "Vuelta de Jorco",
                "San Gabriel",
                "Legua",
                "Monterrey",
                "Salitrillos",
            ]
        ]
        | None
    ) = None


class SanJoseMoraLocation(BaseModel):
    """Location for Mora, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Mora"] = "Mora"
    district: (
        list[
            Literal[
                "Colón",
                "Guayabo",
                "Tabarcia",
                "Piedras Negras",
                "Picagres",
                "Jaris",
                "Quitirrisí",
            ]
        ]
        | None
    ) = None


class SanJoseGoicoecheaLocation(BaseModel):
    """Location for Goicoechea, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Goicoechea"] = "Goicoechea"
    district: (
        list[
            Literal[
                "Guadalupe",
                "San Francisco",
                "Calle Blancos",
                "Mata de Plátano",
                "Ipís",
                "Rancho Redondo",
                "Purral",
            ]
        ]
        | None
    ) = None


class SanJoseSantaAnaLocation(BaseModel):
    """Location for Santa Ana, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Santa Ana"] = "Santa Ana"
    district: (
        list[Literal["Santa Ana", "Salitral", "Pozos", "Uruca", "Piedades", "Brasil"]]
        | None
    ) = None


class SanJoseAlajuelitaLocation(BaseModel):
    """Location for Alajuelita, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Alajuelita"] = "Alajuelita"
    district: (
        list[
            Literal[
                "Alajuelita", "San Josecito", "San Antonio", "Concepción", "San Felipe"
            ]
        ]
        | None
    ) = None


class SanJoseVazquezdeCoronadoLocation(BaseModel):
    """Location for Vázquez de Coronado, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Vázquez de Coronado"] = "Vázquez de Coronado"
    district: (
        list[
            Literal[
                "San Isidro",
                "San Rafael",
                "Dulce Nombre de Jesús",
                "Patalillo",
                "Cascajal",
            ]
        ]
        | None
    ) = None


class SanJoseAcostaLocation(BaseModel):
    """Location for Acosta, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Acosta"] = "Acosta"
    district: (
        list[Literal["San Ignacio", "Guaitil", "Palmichal", "Cangrejal", "Sabanillas"]]
        | None
    ) = None


class SanJoseTibasLocation(BaseModel):
    """Location for Tibás, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Tibás"] = "Tibás"
    district: (
        list[
            Literal[
                "San Juan", "Cinco Esquinas", "Anselmo Llorente", "León XIII", "Colima"
            ]
        ]
        | None
    ) = None


class SanJoseMoraviaLocation(BaseModel):
    """Location for Moravia, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Moravia"] = "Moravia"
    district: list[Literal["San Vicente", "San Jerónimo", "La Trinidad"]] | None = None


class SanJoseMontesdeOcaLocation(BaseModel):
    """Location for Montes de Oca, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Montes de Oca"] = "Montes de Oca"
    district: (
        list[Literal["San Pedro", "Sabanilla", "Mercedes", "San Rafael"]] | None
    ) = None


class SanJoseTurrubaresLocation(BaseModel):
    """Location for Turrubares, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Turrubares"] = "Turrubares"
    district: (
        list[
            Literal["San Pablo", "San Pedro", "San Juan de Mata", "San Luis", "Carara"]
        ]
        | None
    ) = None


class SanJoseDotaLocation(BaseModel):
    """Location for Dota, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Dota"] = "Dota"
    district: list[Literal["Santa María", "Jardín", "Copey"]] | None = None


class SanJoseCurridabatLocation(BaseModel):
    """Location for Curridabat, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Curridabat"] = "Curridabat"
    district: (
        list[Literal["Curridabat", "Granadilla", "Sánchez", "Tirrases"]] | None
    ) = None


class SanJosePerezZeledonLocation(BaseModel):
    """Location for Pérez Zeledón, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["Pérez Zeledón"] = "Pérez Zeledón"
    district: (
        list[
            Literal[
                "San Isidro de El General",
                "El General",
                "Daniel Flores",
                "Rivas",
                "San Pedro",
                "Platanares",
                "Pejibaye",
                "Cajón",
                "Barú",
                "Río Nuevo",
                "Páramo",
                "La Amistad",
            ]
        ]
        | None
    ) = None


class SanJoseLeonCortesCastroLocation(BaseModel):
    """Location for León Cortés Castro, San José."""

    model_config = ConfigDict(extra="forbid")

    province: Literal["San José"] = "San José"
    canton: Literal["León Cortés Castro"] = "León Cortés Castro"
    district: (
        list[
            Literal[
                "San Pablo",
                "San Andrés",
                "Llano Bonito",
                "San Isidro",
                "Santa Cruz",
                "San Antonio",
            ]
        ]
        | None
    ) = None


# Discriminated union of all locations
LocationData = Annotated[
    AlajuelaAlajuelaLocation
    | AlajuelaSanRamonLocation
    | AlajuelaGreciaLocation
    | AlajuelaSanMateoLocation
    | AlajuelaAtenasLocation
    | AlajuelaNaranjoLocation
    | AlajuelaPalmaresLocation
    | AlajuelaPoasLocation
    | AlajuelaOrotinaLocation
    | AlajuelaSanCarlosLocation
    | AlajuelaZarceroLocation
    | AlajuelaSarchiLocation
    | AlajuelaUpalaLocation
    | AlajuelaLosChilesLocation
    | AlajuelaGuatusoLocation
    | AlajuelaRioCuartoLocation
    | CartagoCartagoLocation
    | CartagoParaisoLocation
    | CartagoLaUnionLocation
    | CartagoJimenezLocation
    | CartagoTurrialbaLocation
    | CartagoAlvaradoLocation
    | CartagoOreamunoLocation
    | CartagoElGuarcoLocation
    | GuanacasteLiberiaLocation
    | GuanacasteNicoyaLocation
    | GuanacasteSantaCruzLocation
    | GuanacasteBagacesLocation
    | GuanacasteCarrilloLocation
    | GuanacasteCanasLocation
    | GuanacasteAbangaresLocation
    | GuanacasteTilaranLocation
    | GuanacasteNandayureLocation
    | GuanacasteLaCruzLocation
    | GuanacasteHojanchaLocation
    | HerediaHerediaLocation
    | HerediaBarvaLocation
    | HerediaSantoDomingoLocation
    | HerediaSantaBarbaraLocation
    | HerediaSanRafaelLocation
    | HerediaSanIsidroLocation
    | HerediaBelenLocation
    | HerediaFloresLocation
    | HerediaSanPabloLocation
    | HerediaSarapiquiLocation
    | LimonLimonLocation
    | LimonPocociLocation
    | LimonSiquirresLocation
    | LimonTalamancaLocation
    | LimonMatinaLocation
    | LimonGuacimoLocation
    | PuntarenasPuntarenasLocation
    | PuntarenasEsparzaLocation
    | PuntarenasBuenosAiresLocation
    | PuntarenasMontesdeOroLocation
    | PuntarenasOsaLocation
    | PuntarenasQueposLocation
    | PuntarenasGolfitoLocation
    | PuntarenasCotoBrusLocation
    | PuntarenasParritaLocation
    | PuntarenasCorredoresLocation
    | PuntarenasGarabitoLocation
    | PuntarenasMonteverdeLocation
    | PuntarenasPuertoJimenezLocation
    | SanJoseSanJoseLocation
    | SanJoseEscazuLocation
    | SanJoseDesamparadosLocation
    | SanJosePuriscalLocation
    | SanJoseTarrazuLocation
    | SanJoseAserriLocation
    | SanJoseMoraLocation
    | SanJoseGoicoecheaLocation
    | SanJoseSantaAnaLocation
    | SanJoseAlajuelitaLocation
    | SanJoseVazquezdeCoronadoLocation
    | SanJoseAcostaLocation
    | SanJoseTibasLocation
    | SanJoseMoraviaLocation
    | SanJoseMontesdeOcaLocation
    | SanJoseTurrubaresLocation
    | SanJoseDotaLocation
    | SanJoseCurridabatLocation
    | SanJosePerezZeledonLocation
    | SanJoseLeonCortesCastroLocation,
    Field(discriminator="canton"),
]
