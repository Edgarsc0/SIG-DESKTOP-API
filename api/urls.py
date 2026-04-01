from django.urls import path
from . import views

urlpatterns = [
    path(
        "subir-movimientos-chunk/",
        views.subir_movimientos_chunk,
        name="subir_movimientos_chunk",
    ),
    path("cargar-domicilios-csv/", views.cargar_domicilios_csv),
    path("cargar-familiar-csv/", views.cargar_familiar_csv),
    path("truncar-tabla/", views.truncar_tabla),
    path("bulk-insert-movpos/", views.bulk_insert_movpos),
    path("deduplicar-tabla/", views.deduplicar_tabla),
    path("insertar-movimientos/", views.insertar_movimientos),
    path("eliminar-registros-movimientos/", views.eliminar_registros_movimientos),
]
