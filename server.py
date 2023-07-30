from fastapi import FastAPI
import seoul_people as sp
import SPH
import numpy as np

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/seoul_get_all")
async def seoul_get_all():
    return sp.getAll()


@app.get("/seoul_get/{placeNM}")
async def seoul_get(placeNM: str):
    return sp.send(placeNM)


@app.get("/seoul_get_size/{placeNM}")
async def seoul_get_size(placeNM: str):
    return {"size": sp.getPlaceSize(placeNM)}


@app.get("/sph/{placeNM}")
async def sph(placeNM: str):
    ppl_count = (int(sp.send(placeNM)["AREA_PPLTN_MIN"]) + int(sp.send(placeNM)["AREA_PPLTN_MAX"])) // 2
    size = sp.getPlaceSize(placeNM)
    width = int(np.sqrt(size))
    height = int(np.sqrt(size))
    return SPH.SPH(ppl_count, width, height)

