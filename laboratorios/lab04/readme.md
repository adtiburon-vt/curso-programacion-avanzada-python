# 🧭 Laboratorio 4 — Extensión y especialización de clases

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 4 (Herencia simple y múltiple; uso de `super()`)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Extender y especializar el sistema de usuarios creado en el Lab 3 mediante:

* Subclases con **atributos y métodos adicionales**.
* Uso correcto de **`super()`** en constructores y métodos sobreescritos.
* Ejercicios con **herencia múltiple** y orden de resolución de métodos (MRO).

---

## 🔧 Requisitos previos

* Proyecto de **Lab 3** disponible (`Usuario`, `Admin`, `Invitado`, `BaseUsuario`).
* Python 3.9+ instalado.
* Editor recomendado: VS Code.

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Subclase `Moderador` (herencia simple)

* Crear clase `Moderador` que herede de `Usuario`.
* Añadir un atributo adicional: `nivel` (int, por defecto `1`).
* Sobrescribir `permisos()` para incluir `{"ver", "editar"}` dependiendo del `nivel`.
* Usar `super().__init__` para inicializar la parte común (`nombre`, `email`, `rol`).

---

### 🔹 Fase 2: Métodos sobreescritos con `super()`

* Sobrescribir `presentarse()` en `Admin` para añadir el prefijo `[ADMIN]`.
* Sobrescribir `__str__` en `Moderador` para mostrar también el nivel.
* Asegurarse de reutilizar parte de la lógica de la clase padre con `super()`.

---

### 🔹 Fase 3: Herencia múltiple (mixins)

* Crear un **mixin `LoggerMixin`** con un método `log_evento(self, msg)`.

  * Ejemplo: imprime `[LOG usuario@email] Mensaje`.
* Crear una clase `AdminConLogger` que herede de `Admin` y `LoggerMixin`.
* Probar el orden de resolución de métodos (`.mro()`) y validar que se puede usar `super()` en el mixin.

---

## 🧠 Reflexión final

* ¿Qué aporta heredar de `Usuario` en lugar de copiar código?
* ¿Cuándo conviene usar herencia múltiple (mixins) y cuándo es mejor composición?
* ¿Qué problemas podrían aparecer si abusamos de la herencia múltiple?

---

## 📁 Archivos utilizados

* `app/modelos.py` → nuevas subclases (`Moderador`, `AdminConLogger`, `LoggerMixin`).
* `main.py` → script de pruebas con instancias de las nuevas clases.

---

## ✅ Comprobación de conocimientos

1. ¿Qué diferencia hay entre sobreescribir un método y ampliarlo con `super()`?
2. ¿Qué devuelve `AdminConLogger.mro()` y por qué ese orden?
3. ¿Cómo harías para que `Moderador` pudiera tener distintos permisos según el nivel (básico = editar, avanzado = editar+borrar)?

