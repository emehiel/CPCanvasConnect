import canvasapi as Canvas
import CPCanvasConnect as cc
import os

api_key = os.getenv("CANVAS_API_KEY")
canvas = cc.groups.get_canvas_client(api_key=api_key)

print(canvas)