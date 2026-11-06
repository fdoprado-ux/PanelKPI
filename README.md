# Steakout Executive KPI Dashboard (Fudo POS Integration)

Dashboard ejecutivo de métricas operativas y financieras para el restaurante **Steakout Chophouse**, conectado en tiempo real a la API pública de **Fudo POS** (`https://api.fu.do/v1alpha1`).

---

## 🚀 Inicio Rápido

El servidor ya se encuentra corriendo localmente en:
👉 **[http://localhost:3000](http://localhost:3000)**

Para reiniciar o ejecutar manualmente:
```bash
npm install
npm start
```

---

## 📊 Métricas Claves Desplegadas

### 1. Ventas Claves (Expresadas en Pesos Chilenos - CLP)
- **Ventas Actuales del Día**: Total acumulado hoy, cantidad de órdenes, ticket promedio y barra de progreso hacia la meta diaria ($3.0M).
- **Ventas Última Semana**: Total de los últimos 7 días móviles, órdenes, promedio diario y ticket promedio.
- **Ventas Último Mes**: Total del último mes cerrado (Octubre), órdenes totales, promedio semanal y ticket promedio.
- **Venta Año en Curso (2026)**: Total acumulado anual (Enero a Noviembre 2026), volumen de órdenes y ticket promedio anual.

### 2. Comparativa Histórica: Mismo Mes 3 Años Anteriores
Comparativa del mismo mes calendario durante los últimos 4 años con tarjetas KPI interactivas y gráfico de barras comparativo:
- **Octubre 2023**: $ 89.788.480 CLP (2.580 órdenes • $ 34.802 prom)
- **Octubre 2024**: $ 91.463.778 CLP (2.399 órdenes • $ 38.126 prom)
- **Octubre 2025**: $ 67.778.320 CLP (1.832 órdenes • $ 36.997 prom)
- **Octubre 2026**: $ 63.961.266 CLP (2.182 órdenes • $ 29.313 prom)

*(También incluye el comparativo Noviembre mes en curso a la fecha: Noviembre 2026 $ 9.661.655 vs Noviembre 2025 $ 8.637.867).*

### 3. Descuentos Totales
- **Descuentos de Hoy**: Monto deducido y porcentaje sobre venta bruta.
- **Descuentos Semana Pasada**: Total 7 días móviles.
- **Descuentos Mes Pasado**: Total mes cerrado (Octubre).
- **Descuentos Año en Curso**: Total acumulado 2026.
- **Desglose de Descuentos**: Distribución gráfica por tipo (Promociones Menú / Happy Hour, Convenios Apps Delivery, Cortesías de Fidelización, Descuento Personal).

### 4. Gráficos Interactivos (ApexCharts)
1. **Evolución Diaria de Ventas**: Curva de ventas día por día (Lunes a Domingo).
2. **Progresión Mensual 2026**: Gráfico combinado de barras (ventas) y línea roja (descuentos) de Enero a Noviembre 2026.
3. **Distribución por Canales de Venta**: Donut chart con distribución Salón (Eat-in), Delivery (Apps) y Para Llevar (Takeaway).
4. **Curva de Distribución Horaria de Hoy**: Análisis de horas pico (almuerzo 13:00 - 15:00 y cena 20:00 - 22:00).
5. **Top Platillos Vendidos**: Extraído del catálogo real de Fudo (Smoked Sampler, BBQ CW, etc.) con precios en carta.

---

## 🔐 Integración con la API de Fudo

- **Endpoint de Autenticación**: `POST https://auth.fu.do/api`
- **Generación de Token**: Se intercambian `apiKey` y `apiSecret` por un Bearer JWT token con expiración de 24 horas y renovación automática.
- **Endpoints Utilizados**:
  - `GET /sales`: Ventas, canales, estados (`CLOSED`, `IN-COURSE`), totales y fechas.
  - `GET /discounts`: Rebajas comerciales, porcentajes y mermas.
  - `GET /products`: Catálogo de platos y bebidas con precios reales.
  - `GET /users` y `GET /roles`: Diagnóstico de salud y permisos.
- **Cuenta**: `beakers2` (ID 45523)
- **Usuario**: `ito_api` (ID 123)
- **Zona Horaria**: `America/Santiago`
