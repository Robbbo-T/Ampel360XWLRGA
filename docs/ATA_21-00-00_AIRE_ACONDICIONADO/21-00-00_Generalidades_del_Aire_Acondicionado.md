# 21-00-00 Generalidades del Aire Acondicionado

---
dmc: [COMPLETAR: DMC-GAIAPULSE-AMPEL-0201-21-000-A-001-00_EN-US]
ident:
  dmCode: GPAM-AMPEL-0201-21-00-000-A-001-00  #Example
  modelIdentCode: AMPEL360
  systemDiffCode: A
  systemCode: 0201 # Airframe (adjust as needed)
  subSystemCode: 21 # Air Conditioning
  subSubSystemCode: 00 # General
  assyCode: 000
  disassyCode: 00
  disassyCodeVariant: A
  infoCode: 001  # Overview
  infoCodeVariant: A
  itemLocationCode: 00
  language: ES-ES #Spanish
applicability: AMPEL360XWLRGA
status: draft
security: [COMPLETAR: Clasificación de seguridad, si aplica]
responsiblePartnerCompany: GAIAPULSE
originator: [COMPLETAR: Autor/Equipo]
date: 2025-03-09
---

## 1. Introducción

Este documento proporciona una descripción general del **Sistema de Aire Acondicionado** de la aeronave **AMPEL360XWLRGA**. El sistema de aire acondicionado es crucial para mantener un ambiente cómodo y seguro para los pasajeros y la tripulación, regulando la temperatura, la humedad y la calidad del aire en la cabina durante todas las fases del vuelo.

## 2. Componentes Clave y Sus Funciones

El sistema de aire acondicionado se compone de los siguientes componentes principales:

* **Compresores y Turbinas:** Estos componentes impulsan el ciclo de aire acondicionado al comprimir y expandir el aire para regular la temperatura.
* **Intercambiadores de Calor:** Transfieren calor del aire comprimido al aire ambiente, enfriando el aire antes de su distribución en la cabina.
* **Reguladores de Presión:** Controlan los niveles de presurización de la cabina ajustando el flujo de aire.
* **Sensores de Temperatura y Presión:** Monitorean el rendimiento del sistema de aire acondicionado, proporcionando datos en tiempo real a los controladores.
* **Controles Electrónicos y Paneles de Usuario:** Interfaz para la operación y monitoreo del sistema, permitiendo a la tripulación ajustar y supervisar las condiciones de la cabina.

## 3. Principios de Operación

El sistema de aire acondicionado opera mediante la integración de varios subsistemas que trabajan juntos para lograr condiciones ambientales óptimas en la cabina:

### Regulación de la Temperatura

* **Control Automático de Temperatura:** Los sensores monitorean continuamente la temperatura de la cabina y ajustan la configuración de la máquina de ciclo de aire para mantener una precisión de ±1°C.
* **Intercambiadores de Calor y Evaporadores:** Enfrían o calientan el aire antes de su distribución en la cabina.

### Presurización de la Cabina

* **Válvulas de Salida y Sensores de Presión:** Regulan con precisión la presión de la cabina para simular un ambiente a nivel del mar, minimizando el estrés fisiológico para los pasajeros.
* **Unidad de Control de Presurización (PS):** Ajusta dinámicamente el flujo de aire basado en los cambios de altitud y las fases del vuelo.

### Distribución y Calidad del Aire

* **Sistemas de Filtración Avanzada:** Eliminan partículas y contaminantes del aire, asegurando una alta calidad del aire.
* **Conductos y Ventilaciones:** Distribuyen uniformemente el aire acondicionado en las zonas de la cabina.

### Recuperación de Energía

* **Sistemas de Recuperación de Calor:** Capturan el calor residual de los procesos del sistema de aire acondicionado para su reutilización, mejorando la eficiencia energética general.

### Seguridad y Monitoreo

* **Sistemas de Control Redundantes:** Sensores y actuadores de respaldo aseguran una operación ininterrumpida durante fallos de componentes.
* **Monitoreo en Tiempo Real:** La Unidad de Control Ambiental (ECU) proporciona actualizaciones continuas del estado al panel de control de vuelo.

## 4. Referencias

* **[FAA FAR Part 25](https://www.faa.gov/regulations_policies/faa_regulations/)**: Normativas de la FAA para la certificación de aeronaves.
* **[EASA CS-25](https://www.easa.europa.eu/document-library/certification-specifications/cs-25-aircraft)**: Normativas de la EASA para la certificación de aeronaves.
* **[COAFI Part XI](docs/COAFI/PartXI/DocumentationManagement/CodingSystem/)**: Sistema de codificación de documentos COAFI.
* **[GPPM-QPROP-0401-01-002-A: Q-01 Principles of Operation and Theoretical Basis](docs/GPPM/QPROP/GPPM-QPROP-0401-01-002-A.md)**: Documento detallado sobre la teoría detrás del Q-01.
* **[GPPM-QPROP-0401-01-003-A: Q-01 System Architecture and Schematics](docs/GPPM/QPROP/GPPM-QPROP-0401-01-003-A.md)**: Documento con diagramas y esquemas detallados del Q-01.
