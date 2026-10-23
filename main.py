from fastapi import FastAPI

app = FastAPI(title="Mi API de Golf")

@app.get("/")
def inicio():
    return {"mensaje": "Hola, esta es mi API de golf"}

palos = [
    {"id": 1,  "nombre": "Driver",
     "distancias": {"mar_verano": 250, "mar_invierno": 230, "madrid_verano": 260, "madrid_invierno": 240}},
    {"id": 2,  "nombre": "Madera 4",
     "distancias": {"mar_verano": 200, "mar_invierno": 195, "madrid_verano": 210, "madrid_invierno": 205}},
    {"id": 3,  "nombre": "Hierro 5",
     "distancias": {"mar_verano": 185, "mar_invierno": 175, "madrid_verano": 190, "madrid_invierno": 180}},
    {"id": 4,  "nombre": "Hierro 6",
     "distancias": {"mar_verano": 175, "mar_invierno": 165, "madrid_verano": 180, "madrid_invierno": 170}},
    {"id": 5,  "nombre": "Hierro 7",
     "distancias": {"mar_verano": 165, "mar_invierno": 155, "madrid_verano": 170, "madrid_invierno": 160}},
    {"id": 6,  "nombre": "Hierro 8",
     "distancias": {"mar_verano": 155, "mar_invierno": 145, "madrid_verano": 160, "madrid_invierno": 150}},
    {"id": 7,  "nombre": "Hierro 9",
     "distancias": {"mar_verano": 145, "mar_invierno": 135, "madrid_verano": 150, "madrid_invierno": 140}},
    {"id": 8,  "nombre": "Pitch",
     "distancias": {"mar_verano": 135, "mar_invierno": 125, "madrid_verano": 140, "madrid_invierno": 130}},
    {"id": 9,  "nombre": "Gap",
     "distancias": {"mar_verano": 125, "mar_invierno": 115, "madrid_verano": 130, "madrid_invierno": 120}},
    {"id": 10, "nombre": "52 grados",
     "distancias": {"mar_verano": 115, "mar_invierno": 105, "madrid_verano": 120, "madrid_invierno": 110}},
    {"id": 11, "nombre": "56 grados",
     "distancias": {"mar_verano": 105, "mar_invierno": 95, "madrid_verano": 110, "madrid_invierno": 100}},
]

@app.get("/palos")
def listar_palos():
    return palos

from fastapi.responses import FileResponse

@app.get("/bolsa")
def ver_bolsa():
    return FileResponse("pagina.html")

from typing import Literal

VIENTO = {
    "sin": 0,
    "favor_poco": 0.03,  "favor_medio": 0.06,  "favor_mucho": 0.10,
    "contra_poco": -0.05, "contra_medio": -0.10, "contra_mucho": -0.18,
    "lado_poco": -0.01,  "lado_medio": -0.03,  "lado_mucho": -0.06,
}

DESNIVEL = {
    "llano": 0,
    "arriba_poco": 5,   "arriba_medio": 10,  "arriba_mucho": 20,
    "abajo_poco": -5,   "abajo_medio": -10,  "abajo_mucho": -20,
}

@app.get("/recomendar")
def recomendar(
    metros: float,
    escenario: Literal["mar_verano", "mar_invierno", "madrid_verano", "madrid_invierno"] = "mar_verano",
    viento: Literal[tuple(VIENTO)] = "sin",
    desnivel: Literal[tuple(DESNIVEL)] = "llano",
):
    # ¿A cuántos metros "juega" realmente el golpe?
    juega = metros * (1 - VIENTO[viento]) + DESNIVEL[desnivel]

    # El palo cuya distancia se acerca más
    mejor = min(palos, key=lambda p: abs(p["distancias"][escenario] - juega))

    consejo = ""
    if viento.startswith("lado"):
        consejo = "Apunta un poco hacia el lado del que viene el viento."

    return {
        "metros_reales": metros,
        "juega_como": round(juega),
        "palo": mejor["nombre"],
        "palo_id": mejor["id"],
        "distancia_palo": mejor["distancias"][escenario],
        "consejo": consejo,
    }