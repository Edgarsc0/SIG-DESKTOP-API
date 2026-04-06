from django.urls import path
from django.http import JsonResponse
from . import views

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", health),
    # Endpoints existentes
    path("subir-movimientos-chunk/", views.subir_movimientos_chunk, name="subir_movimientos_chunk"),
    path("cargar-domicilios-csv/", views.cargar_domicilios_csv),
    path("cargar-familiar-csv/", views.cargar_familiar_csv),
    path("truncar-tabla/", views.truncar_tabla),
    path("bulk-insert-movpos/", views.bulk_insert_movpos),
    path("deduplicar-tabla/", views.deduplicar_tabla),
    path("insertar-movimientos/", views.insertar_movimientos),
    path("eliminar-registros-movimientos/", views.eliminar_registros_movimientos),

    # Nuevos endpoints — automatización web
    path("ejecutar-descarga/", views.ejecutar_descarga),
    path("obtener-archivo/<str:session_id>/<path:nombre>/", views.obtener_archivo),
    path("cancelar-descarga/", views.cancelar_descarga),
]
