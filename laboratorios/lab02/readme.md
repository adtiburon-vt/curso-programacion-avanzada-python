# 🧭 Laboratorio 2 — Pipelines de transformación de datos

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 2 (Funciones lambda, list comprehensions, zip, any, all, map, filter, reduce)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Diseñar y ejecutar pipelines de transformación de datos en Python utilizando funciones funcionales (`lambda`, `map`, `filter`, `reduce`) y construcciones idiomáticas (`list comprehensions`, `zip`, `any`, `all`).

El resultado será un script que:

* Normalice y transforme datos de entrada.
* Aplique filtros y combinaciones.
* Reduzca la información a indicadores útiles.

---

## 🔧 Requisitos previos

* Python 3.9+ instalado
* Editor recomendado: VS Code
* Módulo estándar `functools` (incluido en Python)
* Conocimientos básicos de colecciones en Python

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Normalización de datos con `lambda` y list comprehensions

* **Objetivo:** limpiar y transformar un dataset de strings (p. ej., lista de productos o usuarios).
* **Producto esperado:** script `pipeline.py` con funciones que quiten espacios, pasen a minúsculas y apliquen transformaciones básicas.

---

### 🔹 Fase 2: Filtros y combinaciones con `map`, `filter`, `zip`

* **Objetivo:** aplicar funciones de transformación y filtrado sobre el dataset, y combinar listas relacionadas (ej. nombres + precios).
* **Producto esperado:** versión extendida de `pipeline.py` que use `map`, `filter` y `zip`.

---

### 🔹 Fase 3: Agregación con `reduce`, any, all

* **Objetivo:** reducir el dataset a un indicador agregado (ej. suma de valores, conteo de registros válidos), y validar condiciones globales.
* **Producto esperado:** `pipeline.py` completo, con pipeline que devuelva resultados agregados e indicadores de calidad de datos.

---

## 🧠 Reflexión final

* ¿Qué aporta un pipeline funcional frente a un bucle tradicional?
* ¿Cuándo conviene usar comprehensions en lugar de `map`/`filter`?
* ¿Cómo se integra `reduce` con `any`/`all` para calcular métricas de calidad o validación global?

---

## 📁 Archivos utilizados

* `pipeline.py` → pipeline de transformación de datos paso a paso.

---

## ✅ Comprobación de conocimientos

1. ¿Cómo usarías `zip` para combinar usuarios y edades en un diccionario `{usuario: edad}`?
2. Escribe una `list comprehension` que filtre y eleve al cuadrado los números pares de `range(20)`.
3. Implementa con `reduce` la suma de los precios de un listado de productos.