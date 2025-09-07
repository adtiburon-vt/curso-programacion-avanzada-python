# 🧭 Laboratorio 1 — Validación de formularios + funciones reutilizables

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 1 (Expresiones regulares, `*args`/`**kwargs`, decoradores y funciones anidadas)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Construir un pequeño sistema de validación de formularios en Python, aplicando expresiones regulares para validar campos, creando funciones reutilizables con `*args` y `**kwargs`, y añadiendo decoradores para extender el comportamiento de validación (logging, control, etc.).

---

## 🔧 Requisitos previos

* Python 3.9+ instalado
* Editor recomendado: VS Code
* Acceso a línea de comandos
* Ficheros de prueba con entradas de formulario (pueden ser creados como listas o diccionarios en el propio script)

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Validación con expresiones regulares

* **Objetivo:** implementar validadores para email, teléfono y contraseña.
* **Producto esperado:** módulo `validaciones.py` con funciones `validar_email`, `validar_telefono`, `validar_password`.

---

### 🔹 Fase 2: Funciones reutilizables con `*args` y `**kwargs`

* **Objetivo:** crear funciones que procesen formularios dinámicamente, aceptando distintos campos sin necesidad de definirlos de antemano.
* **Producto esperado:** módulo `funciones.py` con funciones como `procesar_formulario(**kwargs)` que impriman/valide varios campos en un mismo paso.

---

### 🔹 Fase 3: Decoradores y funciones anidadas

* **Objetivo:** implementar un decorador que añada comportamiento extra a las validaciones (ej. logging de cada validación, cronómetro, contador de errores).
* **Producto esperado:** módulo `decoradores.py` con ejemplos de decoradores aplicados a las funciones de validación creadas en fases previas.

---

## 🧠 Reflexión final

* ¿Qué ventaja tiene centralizar las validaciones en un módulo reutilizable?
* ¿Cómo simplifican `*args` y `**kwargs` la construcción de funciones flexibles?
* ¿En qué situaciones reales sería útil un decorador de validación (ej. auditoría, seguridad)?

---

## 📁 Archivos utilizados

* `validaciones.py` → funciones con regex para validación.
* `funciones.py` → funciones genéricas con `*args` y `**kwargs`.
* `decoradores.py` → decoradores aplicados a validaciones.

---

## ✅ Comprobación de conocimientos

1. Implementa una regex que valide códigos postales de 5 dígitos.
2. Crea una función `guardar_datos(**campos)` que acepte cualquier número de claves/valores y los imprima formateados.
3. Aplica un decorador `@log` a la función `validar_email` que muestre en consola cada intento de validación.

