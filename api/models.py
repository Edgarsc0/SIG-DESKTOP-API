# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CatPtoFunc(models.Model):
    cd_pto_funcional = models.CharField(db_column='Cd Pto Funcional', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nombre_puesto_funcional = models.CharField(db_column='Nombre Puesto Funcional', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cdnorm = models.CharField(db_column='CdNorm', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CAT_PTO_FUNC'


class Familiar(models.Model):
    hr_id_persona = models.CharField(db_column='HR_ID_PERSONA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    emplid = models.CharField(db_column='EMPLID', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_curp = models.CharField(db_column='HR_CURP', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_nombre = models.CharField(db_column='HR_NOMBRE', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    last_name100 = models.CharField(db_column='LAST_NAME100', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_secnd_last_name = models.CharField(db_column='HR_SECND_LAST_NAME', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    parentesco = models.CharField(db_column='PARENTESCO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    mismo_domicilio = models.CharField(db_column='MISMO_DOMICILIO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    correo_electrónico = models.CharField(db_column='CORREO_ELECTRÓNICO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    teléfono_particular = models.CharField(db_column='TELÉFONO_PARTICULAR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    teléfono_celular = models.CharField(db_column='TELÉFONO_CELULAR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    codigo_postal = models.CharField(db_column='CODIGO_POSTAL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    colonia = models.CharField(db_column='COLONIA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    asentamiento = models.CharField(db_column='ASENTAMIENTO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='PAIS', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    entidad = models.CharField(db_column='ENTIDAD', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='CIUDAD', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ciudad_1 = models.CharField(db_column='CIUDAD_1', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    ciudad_2 = models.CharField(db_column='CIUDAD_2', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FAMILIAR'


class Mov2022(models.Model):
    posición = models.TextField(db_column='Posición', blank=True, null=True)  # Field name made lowercase.
    id_empl = models.TextField(db_column='Id_empl', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    paterno = models.TextField(db_column='Paterno', blank=True, null=True)  # Field name made lowercase.
    apellido_matern = models.TextField(db_column='Apellido Matern', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acción = models.TextField(db_column='Acción', blank=True, null=True)  # Field name made lowercase.
    acción_nombre_field = models.TextField(db_column='Acción (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    motivo = models.TextField(db_column='Motivo', blank=True, null=True)  # Field name made lowercase.
    motivo_nombre_field = models.TextField(db_column='Motivo (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    f_efva = models.TextField(db_column='F/Efva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sec = models.TextField(db_column='Sec', blank=True, null=True)  # Field name made lowercase.
    f_captura = models.TextField(db_column='F/Captura', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    est_hr = models.TextField(db_column='Est HR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_pago = models.TextField(db_column='Estado Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ptda_ptal = models.TextField(db_column='Ptda Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    un = models.TextField(db_column='UN', blank=True, null=True)  # Field name made lowercase.
    u_admva = models.TextField(db_column='U/Admva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_depto = models.TextField(db_column='Id/Depto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_drt = models.TextField(db_column='Depnd Drt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.TextField(db_column='Plan Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.TextField(db_column='Grado', blank=True, null=True)  # Field name made lowercase.
    esc = models.TextField(db_column='Esc', blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.TextField(db_column='Puesto Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel_tabular = models.TextField(db_column='Nivel Tabular', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.TextField(db_column='Gp Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.TextField(db_column='Prog Beneficios', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sal_base = models.TextField(db_column='Sal Base', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.TextField(db_column='Cd Puesto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.TextField(db_column='Ubicación', blank=True, null=True)  # Field name made lowercase.
    id_estbl = models.TextField(db_column='ID Estbl', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slda_prevista = models.TextField(db_column='Slda Prevista', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.TextField(db_column='F/H Últ Actz', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.TextField(db_column='Por', blank=True, null=True)  # Field name made lowercase.
    últ_inicio = models.TextField(db_column='Últ Inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_inicial = models.TextField(db_column='F/Inicial', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_trabajo = models.TextField(db_column='Gp Trabajo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.TextField(db_column='Grupo Cd Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    antig_empr = models.TextField(db_column='Antig Empr', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.TextField(db_column='RFC', blank=True, null=True)  # Field name made lowercase.
    curp = models.TextField(db_column='CURP', blank=True, null=True)  # Field name made lowercase.
    id_persona = models.TextField(db_column='Id Persona', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga = models.TextField(db_column='Descr Larga', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niv_jerarquico = models.TextField(db_column='Niv# Jerarquico', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga1 = models.TextField(db_column='Descr Larga1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    género = models.TextField(db_column='Género', blank=True, null=True)  # Field name made lowercase.
    fecha_entrada = models.TextField(db_column='Fecha Entrada', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_posición = models.TextField(db_column='F Posición', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    año = models.CharField(db_column='AÑO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOV_2022'


class Mov2023(models.Model):
    posición = models.TextField(db_column='Posición', blank=True, null=True)  # Field name made lowercase.
    id_empl = models.TextField(db_column='Id_empl', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    paterno = models.TextField(db_column='Paterno', blank=True, null=True)  # Field name made lowercase.
    apellido_matern = models.TextField(db_column='Apellido Matern', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acción = models.TextField(db_column='Acción', blank=True, null=True)  # Field name made lowercase.
    acción_nombre_field = models.TextField(db_column='Acción (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    motivo = models.TextField(db_column='Motivo', blank=True, null=True)  # Field name made lowercase.
    motivo_nombre_field = models.TextField(db_column='Motivo (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    f_efva = models.TextField(db_column='F/Efva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sec = models.TextField(db_column='Sec', blank=True, null=True)  # Field name made lowercase.
    f_captura = models.TextField(db_column='F/Captura', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    est_hr = models.TextField(db_column='Est HR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_pago = models.TextField(db_column='Estado Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ptda_ptal = models.TextField(db_column='Ptda Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    un = models.TextField(db_column='UN', blank=True, null=True)  # Field name made lowercase.
    u_admva = models.TextField(db_column='U/Admva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_depto = models.TextField(db_column='Id/Depto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_drt = models.TextField(db_column='Depnd Drt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.TextField(db_column='Plan Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.TextField(db_column='Grado', blank=True, null=True)  # Field name made lowercase.
    esc = models.TextField(db_column='Esc', blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.TextField(db_column='Puesto Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel_tabular = models.TextField(db_column='Nivel Tabular', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.TextField(db_column='Gp Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.TextField(db_column='Prog Beneficios', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sal_base = models.TextField(db_column='Sal Base', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.TextField(db_column='Cd Puesto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.TextField(db_column='Ubicación', blank=True, null=True)  # Field name made lowercase.
    id_estbl = models.TextField(db_column='ID Estbl', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slda_prevista = models.TextField(db_column='Slda Prevista', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.TextField(db_column='F/H Últ Actz', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.TextField(db_column='Por', blank=True, null=True)  # Field name made lowercase.
    últ_inicio = models.TextField(db_column='Últ Inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_inicial = models.TextField(db_column='F/Inicial', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_trabajo = models.TextField(db_column='Gp Trabajo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.TextField(db_column='Grupo Cd Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    antig_empr = models.TextField(db_column='Antig Empr', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.TextField(db_column='RFC', blank=True, null=True)  # Field name made lowercase.
    curp = models.TextField(db_column='CURP', blank=True, null=True)  # Field name made lowercase.
    id_persona = models.TextField(db_column='Id Persona', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga = models.TextField(db_column='Descr Larga', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niv_jerarquico = models.TextField(db_column='Niv# Jerarquico', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga1 = models.TextField(db_column='Descr Larga1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    género = models.TextField(db_column='Género', blank=True, null=True)  # Field name made lowercase.
    fecha_entrada = models.TextField(db_column='Fecha Entrada', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_posición = models.TextField(db_column='F Posición', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    año = models.CharField(db_column='AÑO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOV_2023'


class Mov2024(models.Model):
    posición = models.TextField(db_column='Posición', blank=True, null=True)  # Field name made lowercase.
    id_empl = models.TextField(db_column='Id_empl', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    paterno = models.TextField(db_column='Paterno', blank=True, null=True)  # Field name made lowercase.
    apellido_matern = models.TextField(db_column='Apellido Matern', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acción = models.TextField(db_column='Acción', blank=True, null=True)  # Field name made lowercase.
    acción_nombre_field = models.TextField(db_column='Acción (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    motivo = models.TextField(db_column='Motivo', blank=True, null=True)  # Field name made lowercase.
    motivo_nombre_field = models.TextField(db_column='Motivo (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    f_efva = models.TextField(db_column='F/Efva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sec = models.TextField(db_column='Sec', blank=True, null=True)  # Field name made lowercase.
    f_captura = models.TextField(db_column='F/Captura', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    est_hr = models.TextField(db_column='Est HR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_pago = models.TextField(db_column='Estado Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ptda_ptal = models.TextField(db_column='Ptda Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    un = models.TextField(db_column='UN', blank=True, null=True)  # Field name made lowercase.
    u_admva = models.TextField(db_column='U/Admva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_depto = models.TextField(db_column='Id/Depto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_drt = models.TextField(db_column='Depnd Drt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.TextField(db_column='Plan Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.TextField(db_column='Grado', blank=True, null=True)  # Field name made lowercase.
    esc = models.TextField(db_column='Esc', blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.TextField(db_column='Puesto Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel_tabular = models.TextField(db_column='Nivel Tabular', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.TextField(db_column='Gp Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.TextField(db_column='Prog Beneficios', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sal_base = models.TextField(db_column='Sal Base', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.TextField(db_column='Cd Puesto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.TextField(db_column='Ubicación', blank=True, null=True)  # Field name made lowercase.
    id_estbl = models.TextField(db_column='ID Estbl', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slda_prevista = models.TextField(db_column='Slda Prevista', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.TextField(db_column='F/H Últ Actz', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.TextField(db_column='Por', blank=True, null=True)  # Field name made lowercase.
    últ_inicio = models.TextField(db_column='Últ Inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_inicial = models.TextField(db_column='F/Inicial', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_trabajo = models.TextField(db_column='Gp Trabajo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.TextField(db_column='Grupo Cd Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    antig_empr = models.TextField(db_column='Antig Empr', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.TextField(db_column='RFC', blank=True, null=True)  # Field name made lowercase.
    curp = models.TextField(db_column='CURP', blank=True, null=True)  # Field name made lowercase.
    id_persona = models.TextField(db_column='Id Persona', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga = models.TextField(db_column='Descr Larga', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niv_jerarquico = models.TextField(db_column='Niv# Jerarquico', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga1 = models.TextField(db_column='Descr Larga1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    género = models.TextField(db_column='Género', blank=True, null=True)  # Field name made lowercase.
    fecha_entrada = models.TextField(db_column='Fecha Entrada', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_posición = models.TextField(db_column='F Posición', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    año = models.CharField(db_column='AÑO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOV_2024'


class Mov2025(models.Model):
    posición = models.CharField(db_column='Posición', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_empl = models.CharField(db_column='Id_empl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paterno = models.CharField(db_column='Paterno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    apellido_matern = models.CharField(db_column='Apellido Matern', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acción = models.CharField(db_column='Acción', max_length=255, blank=True, null=True)  # Field name made lowercase.
    acción_nombre_field = models.CharField(db_column='Acción (Nombre)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    motivo = models.CharField(db_column='Motivo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    motivo_nombre_field = models.CharField(db_column='Motivo (Nombre)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    f_efva = models.CharField(db_column='F/Efva', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sec = models.CharField(db_column='Sec', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f_captura = models.CharField(db_column='F/Captura', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    est_hr = models.CharField(db_column='Est HR', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_pago = models.CharField(db_column='Estado Pago', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ptda_ptal = models.CharField(db_column='Ptda Ptal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    un = models.CharField(db_column='UN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    u_admva = models.CharField(db_column='U/Admva', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_depto = models.CharField(db_column='Id/Depto', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_drt = models.CharField(db_column='Depnd Drt', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.CharField(db_column='Plan Sal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.CharField(db_column='Grado', max_length=255, blank=True, null=True)  # Field name made lowercase.
    esc = models.CharField(db_column='Esc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.CharField(db_column='Puesto Ptal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel_tabular = models.CharField(db_column='Nivel Tabular', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.CharField(db_column='Gp Pago', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.CharField(db_column='Prog Beneficios', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sal_base = models.CharField(db_column='Sal Base', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.CharField(db_column='Cd Puesto', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.CharField(db_column='Ubicación', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_estbl = models.CharField(db_column='ID Estbl', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slda_prevista = models.CharField(db_column='Slda Prevista', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.CharField(db_column='F/H Últ Actz', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.CharField(db_column='Por', max_length=255, blank=True, null=True)  # Field name made lowercase.
    últ_inicio = models.CharField(db_column='Últ Inicio', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_inicial = models.CharField(db_column='F/Inicial', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_trabajo = models.CharField(db_column='Gp Trabajo', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.CharField(db_column='Grupo Cd Sal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    antig_empr = models.CharField(db_column='Antig Empr', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.CharField(db_column='RFC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    curp = models.CharField(db_column='CURP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_persona = models.CharField(db_column='Id Persona', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga = models.CharField(db_column='Descr Larga', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niv_jerarquico = models.CharField(db_column='Niv# Jerarquico', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga1 = models.CharField(db_column='Descr Larga1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    género = models.CharField(db_column='Género', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_entrada = models.CharField(db_column='Fecha Entrada', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_posición = models.CharField(db_column='F Posición', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    año = models.CharField(db_column='AÑO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOV_2025'


class Mov2026(models.Model):
    posición = models.CharField(db_column='Posición', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_empl = models.CharField(db_column='Id_empl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paterno = models.CharField(db_column='Paterno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    apellido_matern = models.CharField(db_column='Apellido Matern', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acción = models.CharField(db_column='Acción', max_length=255, blank=True, null=True)  # Field name made lowercase.
    acción_nombre_field = models.CharField(db_column='Acción (Nombre)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    motivo = models.CharField(db_column='Motivo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    motivo_nombre_field = models.CharField(db_column='Motivo (Nombre)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    f_efva = models.CharField(db_column='F/Efva', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sec = models.CharField(db_column='Sec', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f_captura = models.CharField(db_column='F/Captura', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    est_hr = models.CharField(db_column='Est HR', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_pago = models.CharField(db_column='Estado Pago', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ptda_ptal = models.CharField(db_column='Ptda Ptal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    un = models.CharField(db_column='UN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    u_admva = models.CharField(db_column='U/Admva', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_depto = models.CharField(db_column='Id/Depto', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_drt = models.CharField(db_column='Depnd Drt', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.CharField(db_column='Plan Sal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.CharField(db_column='Grado', max_length=255, blank=True, null=True)  # Field name made lowercase.
    esc = models.CharField(db_column='Esc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.CharField(db_column='Puesto Ptal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel_tabular = models.CharField(db_column='Nivel Tabular', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.CharField(db_column='Gp Pago', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.CharField(db_column='Prog Beneficios', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sal_base = models.CharField(db_column='Sal Base', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.CharField(db_column='Cd Puesto', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.CharField(db_column='Ubicación', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_estbl = models.CharField(db_column='ID Estbl', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slda_prevista = models.CharField(db_column='Slda Prevista', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.CharField(db_column='F/H Últ Actz', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.CharField(db_column='Por', max_length=255, blank=True, null=True)  # Field name made lowercase.
    últ_inicio = models.CharField(db_column='Últ Inicio', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_inicial = models.CharField(db_column='F/Inicial', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_trabajo = models.CharField(db_column='Gp Trabajo', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.CharField(db_column='Grupo Cd Sal', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    antig_empr = models.CharField(db_column='Antig Empr', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.CharField(db_column='RFC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    curp = models.CharField(db_column='CURP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_persona = models.CharField(db_column='Id Persona', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga = models.CharField(db_column='Descr Larga', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niv_jerarquico = models.CharField(db_column='Niv# Jerarquico', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga1 = models.CharField(db_column='Descr Larga1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    género = models.CharField(db_column='Género', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fecha_entrada = models.CharField(db_column='Fecha Entrada', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_posición = models.CharField(db_column='F Posición', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    año = models.CharField(db_column='AÑO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOV_2026'


class MovPos(models.Model):
    nº_pos_actual = models.CharField(db_column='Nº Pos Actual', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_efva = models.CharField(db_column='F Efva', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_psn = models.CharField(db_column='Estado Psn', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_captura = models.CharField(db_column='Fecha Captura', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_motivo = models.CharField(db_column='Cd Motivo', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    motivo = models.CharField(db_column='Motivo', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    cd_un = models.CharField(db_column='Cd UN', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unidad_de_negocio = models.CharField(db_column='Unidad de Negocio', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unidad_adva_field = models.CharField(db_column='Unidad Adva#', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cd_departamento = models.CharField(db_column='Cd Departamento', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.CharField(db_column='Cd Puesto', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_ptal = models.CharField(db_column='Estado Ptal', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fecha_est = models.CharField(db_column='Fecha Est', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    máximo = models.CharField(db_column='Máximo', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    depnd_drt = models.CharField(db_column='Depnd Drt', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_indrt = models.CharField(db_column='Depnd Indrt', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.CharField(db_column='Ubicación', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    nvl_direc = models.CharField(db_column='Nvl Direc', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.CharField(db_column='Plan Sal', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.CharField(db_column='Grado', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    esc = models.CharField(db_column='Esc', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.CharField(db_column='Puesto Ptal', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    partida_ptal = models.CharField(db_column='Partida Ptal', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.CharField(db_column='Gp Pago', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.CharField(db_column='Prog Beneficios', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.CharField(db_column='F/H Últ Actz', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.CharField(db_column='Por', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_estd_semn = models.CharField(db_column='Hr Estd/Semn', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr = models.CharField(db_column='Descr', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    gp_trabajo = models.CharField(db_column='Gp Trabajo', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    org_code = models.CharField(db_column='Org Code', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.CharField(db_column='Grupo Cd Sal', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    formaldesc = models.CharField(db_column='FormalDesc', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    pto_compt = models.CharField(db_column='Pto Compt', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    posn_clv = models.CharField(db_column='Posn Clv', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    presupuesto = models.CharField(db_column='Presupuesto', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    nombre_puesto = models.CharField(db_column='Nombre Puesto', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'MOV_POS'


class MovTotal(models.Model):
    posición = models.TextField(db_column='Posición', blank=True, null=True)  # Field name made lowercase.
    id_empl = models.TextField(db_column='Id_empl', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    paterno = models.TextField(db_column='Paterno', blank=True, null=True)  # Field name made lowercase.
    apellido_matern = models.TextField(db_column='Apellido Matern', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acción = models.TextField(db_column='Acción', blank=True, null=True)  # Field name made lowercase.
    acción_nombre_field = models.TextField(db_column='Acción (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    motivo = models.TextField(db_column='Motivo', blank=True, null=True)  # Field name made lowercase.
    motivo_nombre_field = models.TextField(db_column='Motivo (Nombre)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    f_efva = models.TextField(db_column='F/Efva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sec = models.TextField(db_column='Sec', blank=True, null=True)  # Field name made lowercase.
    f_captura = models.TextField(db_column='F/Captura', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    est_hr = models.TextField(db_column='Est HR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado_pago = models.TextField(db_column='Estado Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ptda_ptal = models.TextField(db_column='Ptda Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    un = models.TextField(db_column='UN', blank=True, null=True)  # Field name made lowercase.
    u_admva = models.TextField(db_column='U/Admva', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_depto = models.TextField(db_column='Id/Depto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depnd_drt = models.TextField(db_column='Depnd Drt', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plan_sal = models.TextField(db_column='Plan Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grado = models.TextField(db_column='Grado', blank=True, null=True)  # Field name made lowercase.
    esc = models.TextField(db_column='Esc', blank=True, null=True)  # Field name made lowercase.
    puesto_ptal = models.TextField(db_column='Puesto Ptal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel_tabular = models.TextField(db_column='Nivel Tabular', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_pago = models.TextField(db_column='Gp Pago', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prog_beneficios = models.TextField(db_column='Prog Beneficios', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sal_base = models.TextField(db_column='Sal Base', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_puesto = models.TextField(db_column='Cd Puesto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.TextField(db_column='Ubicación', blank=True, null=True)  # Field name made lowercase.
    id_estbl = models.TextField(db_column='ID Estbl', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slda_prevista = models.TextField(db_column='Slda Prevista', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_h_últ_actz = models.TextField(db_column='F/H Últ Actz', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    por = models.TextField(db_column='Por', blank=True, null=True)  # Field name made lowercase.
    últ_inicio = models.TextField(db_column='Últ Inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_inicial = models.TextField(db_column='F/Inicial', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gp_trabajo = models.TextField(db_column='Gp Trabajo', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grupo_cd_sal = models.TextField(db_column='Grupo Cd Sal', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    antig_empr = models.TextField(db_column='Antig Empr', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.TextField(db_column='RFC', blank=True, null=True)  # Field name made lowercase.
    curp = models.TextField(db_column='CURP', blank=True, null=True)  # Field name made lowercase.
    id_persona = models.TextField(db_column='Id Persona', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga = models.TextField(db_column='Descr Larga', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niv_jerarquico = models.TextField(db_column='Niv# Jerarquico', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descr_larga1 = models.TextField(db_column='Descr Larga1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    género = models.TextField(db_column='Género', blank=True, null=True)  # Field name made lowercase.
    fecha_entrada = models.TextField(db_column='Fecha Entrada', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    f_posición = models.TextField(db_column='F Posición', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    año = models.CharField(db_column='AÑO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MOV_TOTAL'


class Domicilios(models.Model):
    no_empleado = models.CharField(db_column='NO_EMPLEADO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_id_persona = models.CharField(db_column='HR_ID_PERSONA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    position_nbr = models.CharField(db_column='POSITION_NBR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    nombre_completo = models.CharField(db_column='NOMBRE_COMPLETO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    rfc = models.CharField(db_column='RFC', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    curp = models.CharField(db_column='CURP', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    puesto_estructural = models.CharField(db_column='PUESTO_ESTRUCTURAL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    puesto_funcional = models.CharField(db_column='PUESTO_FUNCIONAL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    puesto = models.CharField(db_column='PUESTO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    escolaridad_tipo = models.CharField(db_column='ESCOLARIDAD_TIPO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    escolaridad_nivrl = models.CharField(db_column='ESCOLARIDAD_NIVRL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    escolaridad_area = models.CharField(db_column='ESCOLARIDAD_AREA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    carrera = models.CharField(db_column='CARRERA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    centro_escolar = models.CharField(db_column='CENTRO_ESCOLAR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    humanos_status = models.CharField(db_column='HUMANOS_STATUS', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    estatus_nomina = models.CharField(db_column='ESTATUS_NOMINA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='PHONE1', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    calle = models.CharField(db_column='CALLE', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_numero_exterior = models.CharField(db_column='HR_NUMERO_EXTERIOR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_numero_interior = models.CharField(db_column='HR_NUMERO_INTERIOR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    postal = models.CharField(db_column='POSTAL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    colonia = models.CharField(db_column='COLONIA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    hr_municipio = models.CharField(db_column='HR_MUNICIPIO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    email_addr2 = models.CharField(db_column='EMAIL_ADDR2', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    email_addr = models.CharField(db_column='EMAIL_ADDR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    deptid = models.CharField(db_column='DEPTID', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    unidad_administrativa = models.CharField(db_column='UNIDAD_ADMINISTRATIVA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'domicilios'


class PlantillaFinBackup20251231124825(models.Model):
    posición = models.CharField(db_column='Posición', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    estado_nómina = models.CharField(db_column='Estado Nómina', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    num_empleado = models.CharField(db_column='Num Empleado', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rfc = models.CharField(db_column='RFC', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    curp = models.CharField(db_column='CURP', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    motivo = models.CharField(db_column='Motivo', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    fecha_efectiva_personal_field = models.CharField(db_column='Fecha efectiva (Personal)', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    fecha_de_captura = models.CharField(db_column='Fecha de captura', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    qna_field = models.CharField(db_column='Qna#', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    fecha_prevista_de_salida = models.CharField(db_column='Fecha prevista de salida', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nj = models.CharField(db_column='NJ', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    código_presupuestal = models.CharField(db_column='Código Presupuestal', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nivel = models.CharField(db_column='Nivel', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    escala = models.CharField(db_column='Escala', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    smb = models.CharField(db_column='SMB', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    smn = models.DecimalField(db_column='SMN', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    partida = models.CharField(db_column='Partida', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    tipo_de_contratación = models.CharField(db_column='Tipo de Contratación', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_un = models.CharField(db_column='Cd UN', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unidad_de_negocio = models.CharField(db_column='Unidad de Negocio', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_ua = models.CharField(db_column='Cd UA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unidad_administrativa = models.CharField(db_column='Unidad Administrativa', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cd_pto_funcional = models.CharField(db_column='Cd Pto Funcional', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nombre_puesto_funcional = models.CharField(db_column='Nombre Puesto Funcional', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    id_departamento = models.CharField(db_column='Id Departamento', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    departamento = models.CharField(db_column='Departamento', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    dependencia_directa = models.CharField(db_column='Dependencia Directa', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    observaciones = models.CharField(db_column='Observaciones', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    programa = models.CharField(db_column='Programa', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    num_empleado1 = models.CharField(db_column='Num empleado1', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    posición1 = models.CharField(db_column='Posición1', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    especialidad = models.CharField(db_column='Especialidad', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    entidad_federativa = models.CharField(db_column='Entidad Federativa', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_aduana = models.CharField(db_column='Tipo de Aduana', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ubicación = models.CharField(db_column='Ubicación', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    descripción_ubicación = models.CharField(db_column='Descripción ubicación', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    posición_civil_sedena_semar = models.CharField(db_column='Posición _Civil / SEDENA / SEMAR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    personal_militar_o_civil = models.CharField(db_column='Personal Militar o Civil', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_personal_sedena_semar = models.CharField(db_column='Tipo de personal SEDENA / SEMAR', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rango = models.CharField(db_column='Rango', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    fecha_de_ingreso = models.CharField(db_column='Fecha de ingreso', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dg_o_aduana_compactada = models.CharField(db_column='DG o Aduana compactada', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    depuración_vacancia = models.CharField(db_column='Depuración Vacancia', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    proyecto_2025_337_plazas_para_autorización_shcp = models.CharField(db_column='Proyecto 2025 337 plazas para autorización SHCP', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    plazas_propuestas_para_conversión_eventuales_y_permanenes_p33_a = models.CharField(db_column='Plazas propuestas para conversión_ Eventuales y Permanenes P33 A', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_1er_escalón_y_46_reingresos_sgtos_sedena = models.CharField(db_column='1er Escalón y 46 reingresos Sgtos SEDENA', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    validando_de_posición_por_documento = models.CharField(db_column='Validando de posición por documento', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reportada = models.CharField(db_column='Reportada', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    foto = models.TextField(blank=True, null=True)
    costo_plaza_anual = models.CharField(db_column='COSTO_PLAZA_ANUAL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    costo_plaza_mensual = models.CharField(db_column='COSTO_PLAZA_MENSUAL', max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'plantilla_fin_backup_20251231_124825'
