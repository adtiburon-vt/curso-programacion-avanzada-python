# 🔹 Fase 3: Simulación de deadlock y prevención

### 🎯 Objetivo

Provocar un **deadlock** entre hilos usando dos `Lock` adquiridos en distinto orden, y luego **prevenirlo** aplicando:
para la preparación de cursos técnicos personalizados
📘 Briefing para la preparación de cursos técnicos personalizados
🧠 Nota para el asistente y el usuario: Este documento es un briefing general, reutilizable y auto-gestionado. No representa un curso específico.

Cuando lo pegues en un nuevo chat, simplemente continúa con:

“Deseo preparar un nuevo curso, aquí tienes el documento base”, o
“Vamos a trabajar sobre un curso que ya tengo”.
📌 El asistente no debe generar contenido a partir de este documento. Su única respuesta inicial debe ser:

"Perfecto, ya tengo las reglas para preparar cursos personalizados. ¿Puedes pasarme ahora el documento base o los datos del curso que deseas crear?"

🌟 Objetivo
Establecer una metodología clara para que se puedan generar cursos técnicos personalizados a partir de un documento base. El asistente analizará dicho documento y entregará un plan detallado y profesional listo para usar.

📥 Qué debe proporcionar el usuario
Un documento base que contenga información como:

Título del curso
Duración total
Objetivos generales
Perfil del alumnado
Contenidos o temario deseado
Modalidad y calendario (si aplica)
🚧 Todo lo que no esté especificado o sea ambiguo será consultado antes de continuar.

📦 Entregables del asistente
Tras analizar el documento base, se entregará un plan completo del curso que incluirá:

Temario estructurado por sesiones
Duración total y distribución horaria por sesión
Distribución de tiempo: 70% laboratorios / 30% teoría y demostraciones
Propuesta de laboratorios faseados
Herramientas o archivos requeridos (si aplica)
Preguntas de validación o reflexión final (si aplica)
El contenido se entrega en formato listo para copiar y guardar fuera, para luego retomarlo en cualquier momento desde un nuevo chat.

⚙️ Estructura estándar del curso
Duración por defecto: 25 horas (modificable si se indica otra cosa)

Número de sesiones: 5 sesiones de 5 horas

Modalidad: presencial, remoto o mixto

Distribución del tiempo por sesión:

70% Laboratorio auto-guiado y práctico
30% Exposición teórica y demostraciones por parte del formador
🧪 Laboratorios: metodología
Los laboratorios se estructuran en fases. Cada fase sigue esta plantilla:

🔹 Plantilla de fase de laboratorio
🔹 Fase X: Título
🎯 Objetivo: qué se busca lograr
🧱 Scaffold (opcional): archivos de partida o entorno inicial
🧭 Pasos: instrucciones detalladas paso a paso
🔥 Reto: ejercicio adicional con tip opcional
✅ Validación: comprobación de que la fase se ha completado correctamente
📄 Plantilla resumen de sesión/laboratorio (README)
Se puede generar un resumen estilo README con la siguiente estructura:

🧭 Sesión X: Título
Duración: X horas
Modalidad: presencial / remota
Objetivo general: propósito de la sesión

🔧 Requisitos previos: herramientas o conocimientos necesarios

🔬 Fases del laboratorio:
- Fase 1: ...
- Fase 2: ...
...

🧠 Reflexión final: preguntas de debate o análisis

📁 Archivos utilizados: scripts, manifiestos, etc.

✅ Comprobación de conocimientos: preguntas clave para repaso final
🧵 Flujo de trabajo
El usuario proporciona el documento base.

El asistente entrega un plan completo para guardar y reutilizar.

A partir de ahí, el usuario puede iniciar un nuevo chat y pedir:

"Genera el contenido del tema 2"
"Dame la fase 1 del laboratorio 3"
"Prepara el resumen del laboratorio 1"
"Haz el README de la sesión 4"
Cada petición generará contenido detallado según la estructura descrita.
1. **Orden global de adquisición**, o
2. **`acquire(timeout=…)`** con manejo de fallo.

---

## 🧱 Qué vas a añadir

* Nuevas funciones en `app/procesador.py` para:

  * simular el deadlock
  * resolverlo con **orden global**
  * resolverlo con **timeout**
* Un script de entrada para ver cada caso.

---

## 🧭 Código

### 1) `app/procesador.py` — utilidades de deadlock

Añade al final del archivo:

```python
# app/procesador.py (añadir al final)
from time import sleep
import threading

def _trabajo_breve():
    # simula trabajo crítico
    sleep(0.1)

def simular_deadlock(lock1: threading.Lock, lock2: threading.Lock):
    """
    Lanza dos hilos que adquieren lock1->lock2 y lock2->lock1.
    Riesgo: deadlock (interbloqueo) si el timing coincide.
    """
    def t1():
        with lock1:
            print("[t1] tomó lock1, esperando lock2…")
            sleep(0.2)
            with lock2:
                print("[t1] tomó lock2")
                _trabajo_breve()

    def t2():
        with lock2:
            print("[t2] tomó lock2, esperando lock1…")
            sleep(0.2)
            with lock1:
                print("[t2] tomó lock1")
                _trabajo_breve()

    h1 = threading.Thread(target=t1, name="t1")
    h2 = threading.Thread(target=t2, name="t2")
    h1.start(); h2.start()
    # Atención: join podría bloquearse si entran en deadlock.
    h1.join(timeout=2.0)
    h2.join(timeout=2.0)

    stuck = h1.is_alive() or h2.is_alive()
    if stuck:
        print("⚠️  Deadlock detectado: hilos no finalizaron a tiempo")
    else:
        print("✔ Sin deadlock (esta vez)")

def trabajo_ordenado(lock_a: threading.Lock, lock_b: threading.Lock):
    """
    Adquiere SIEMPRE en el mismo orden: A -> B.
    """
    with lock_a:
        print(f"[{threading.current_thread().name}] tomó A")
        sleep(0.1)
        with lock_b:
            print(f"[{threading.current_thread().name}] tomó B")
            _trabajo_breve()

def resolver_con_orden_global():
    """
    Dos hilos que respetan el orden A->B (evita deadlock).
    """
    A = threading.Lock()
    B = threading.Lock()
    h1 = threading.Thread(target=trabajo_ordenado, args=(A, B), name="r1")
    h2 = threading.Thread(target=trabajo_ordenado, args=(A, B), name="r2")
    h1.start(); h2.start()
    h1.join(); h2.join()
    print("✔ Finalizado sin deadlock (orden global)")

def resolver_con_timeout(lock1: threading.Lock, lock2: threading.Lock, who: str):
    """
    Intenta lock1->lock2 con timeout; si falla, libera y reintenta.
    """
    # Primer lock (bloqueante)
    acquired1 = lock1.acquire(timeout=1.0)
    if not acquired1:
        print(f"[{who}] no pudo tomar lock1, reintentará…")
        return

    print(f"[{who}] tomó lock1, intentando lock2 con timeout…")
    try:
        acquired2 = lock2.acquire(timeout=0.5)
        if not acquired2:
            print(f"[{who}] no pudo tomar lock2, desistiendo para evitar deadlock")
            return
        try:
            print(f"[{who}] tomó lock2, trabajando…")
            _trabajo_breve()
        finally:
            lock2.release()
    finally:
        lock1.release()
```

### 2) `main.py` — demo de deadlock y soluciones

Puedes crear un archivo separado para las demos, por ejemplo `deadlock_demo.py`:

```python
# deadlock_demo.py
import threading
from app.procesador import (
    simular_deadlock,
    resolver_con_orden_global,
    resolver_con_timeout,
)

def demo_deadlock():
    print("\n=== DEMO: Posible deadlock ===")
    L1 = threading.Lock()
    L2 = threading.Lock()
    simular_deadlock(L1, L2)  # puede quedarse atascado; usamos join con timeout

def demo_orden_global():
    print("\n=== DEMO: Prevención por orden global A->B ===")
    resolver_con_orden_global()

def demo_timeout():
    print("\n=== DEMO: Prevención con timeouts ===")
    L1 = threading.Lock()
    L2 = threading.Lock()
    t1 = threading.Thread(target=resolver_con_timeout, args=(L1, L2, "X"))
    t2 = threading.Thread(target=resolver_con_timeout, args=(L2, L1, "Y"))  # orden inverso, pero con timeout
    t1.start(); t2.start()
    t1.join(); t2.join()
    print("✔ Finalizado sin deadlock (timeouts)")

if __name__ == "__main__":
    demo_deadlock()
    demo_orden_global()
    demo_timeout()
```

---

## ▶️ Ejecución

```bash
python deadlock_demo.py
```

**Salida típica (puede variar):**

```
=== DEMO: Posible deadlock ===
[t1] tomó lock1, esperando lock2…
[t2] tomó lock2, esperando lock1…
⚠️  Deadlock detectado: hilos no finalizaron a tiempo

=== DEMO: Prevención por orden global A->B ===
[r1] tomó A
[r1] tomó B
[r2] tomó A
[r2] tomó B
✔ Finalizado sin deadlock (orden global)

=== DEMO: Prevención con timeouts ===
[X] tomó lock1, intentando lock2 con timeout…
[Y] tomó lock1, intentando lock2 con timeout…
[Y] no pudo tomar lock2, desistiendo para evitar deadlock
[X] tomó lock2, trabajando…
✔ Finalizado sin deadlock (timeouts)
```

---

## ✅ Criterios de aceptación

* **Deadlock reproducible** (al menos de forma intermitente): dos hilos quedan esperando mutuamente → detectado por `join(timeout)` y mensaje de alerta.
* **Prevención por orden global**: ambos hilos completan con el patrón **A→B** sin bloqueo.
* **Prevención por timeout**: al menos uno de los hilos aborta la adquisición del segundo lock, liberando el primero y evitando el deadlock.

---

## 🔥 Retos (opcionales)

1. **Backoff exponencial**: si falla el segundo lock, espera un tiempo creciente antes de reintentar.
2. **RLock cooperativo**: reescribe los ejemplos usando `threading.RLock` cuando un mismo hilo necesite reentrar en la región crítica.
3. **Métricas**: registra cuántos reintentos fueron necesarios antes de completar sin deadlock.

---

# ✅ Conclusión del Laboratorio 7

**Qué has conseguido:**

* Procesar archivos en **paralelo** con hilos y consolidar resultados con **`Lock`**.
* Entender y **reproducir un deadlock** controlado entre dos locks.
* Aplicar **dos estrategias de prevención**:

  * **Orden global de adquisición** (determinista y simple).
  * **`acquire(timeout=…)` + desistir/reintentar** (robusto ante contención).

**Aprendizajes clave:**

* Los **locks** evitan **condiciones de carrera**, pero un mal orden de adquisición puede bloquear el sistema.
* El **diseño** (orden global, regiones críticas pequeñas) es tan importante como la API (`Lock`, `RLock`, timeouts).
* `join(timeout)` te ayuda a **detectar síntomas** de deadlock en demos/tests.

**Listo para continuar:**

* Migrar este patrón a **ThreadPoolExecutor** y a operaciones de I/O reales (descargas, lectura de logs).
* Instrumentar con **logging** y **tests** que verifiquen ausencia de deadlocks (p. ej., ejecuciones repetidas con timeouts).
* Prepararte para la **Sesión 8** (Multiprocesamiento: `Process`, `Queue`, `Pool`) para tareas **CPU intensivo**.
