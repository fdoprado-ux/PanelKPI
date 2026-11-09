require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const FudoService = require('./services/fudoService');
const MockService = require('./services/mockService');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const fudo = new FudoService({
  apiUrl: process.env.FUDO_API_URL,
  authUrl: process.env.FUDO_AUTH_URL,
  apiKey: process.env.FUDO_API_KEY,
  apiSecret: process.env.FUDO_API_SECRET
});

// Cache variables for optimal performance
let cachedMetrics = null;
let lastMetricsFetchTime = 0;
const METRICS_TTL_MS = 30 * 1000; // 30s cache

const apiRouter = express.Router();

/**
 * Diagnostic & Permission Status
 */
apiRouter.get('/status', async (req, res) => {
  try {
    const diagnostic = await fudo.checkPermissions();
    res.json({
      success: true,
      diagnostic,
      instructions: {
        message: diagnostic.hasSalesPermission && diagnostic.hasDiscountsPermission
          ? 'Conexión completa con Fudo. Permisos de ventas y descuentos activos.'
          : 'La API Key está autenticada con éxito, pero el usuario asignado no tiene permisos para ver Ventas y Descuentos.',
        steps: [
          'Inicia sesión en Fudo con una cuenta Administrador (https://app.fu.do)',
          'Ve a "Administración" > "Usuarios"',
          'Edita el usuario "usuario api" (ito_api@beakers2)',
          'En el campo "Rol", selecciona un rol con permisos de ventas (como "Admin" o "Gerencia"), o en "Administración > Roles" añade "list_sales" y "list_discounts" al rol "Integraciones"',
          'Haz clic en Guardar y luego presiona "Re-verificar Fudo" en este dashboard'
        ]
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * Re-check permissions and invalidate token
 */
apiRouter.post('/check-permissions', async (req, res) => {
  try {
    await fudo.getToken(true);
    const diagnostic = await fudo.checkPermissions();
    cachedMetrics = null; // bust metrics cache
    res.json({ success: true, diagnostic });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * Main Metrics Endpoint
 */
apiRouter.get('/metrics', async (req, res) => {
  // Prevent browser/proxy intermediate caching for real-time freshness
  res.set({
    'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  });

  const force = req.query.force === 'true';
  const now = Date.now();

  if (!force && cachedMetrics && (now - lastMetricsFetchTime < METRICS_TTL_MS)) {
    return res.json(cachedMetrics);
  }

  try {
    const diagnostic = await fudo.checkPermissions();

    if (diagnostic.hasSalesPermission && diagnostic.hasDiscountsPermission) {
      console.log('[Server] Fetching live metrics from Fudo POS API...');
      const liveData = await fudo.getLiveMetrics();
      cachedMetrics = liveData;
      lastMetricsFetchTime = now;
      return res.json(liveData);
    } else {
      console.log('[Server] Missing sales/discount permissions in Fudo. Serving calibrated Steakout simulation...');
      const mockData = MockService.getMetrics();
      mockData.diagnostic = diagnostic;
      mockData.source = 'simulated_permission_required';
      cachedMetrics = mockData;
      lastMetricsFetchTime = now;
      return res.json(mockData);
    }
  } catch (err) {
    console.error('[Server] Critical error in /api/metrics:', err.message);
    const mockData = MockService.getMetrics();
    mockData.error = err.message;
    res.json(mockData);
  }
});

/**
 * Live Products from Fudo
 */
apiRouter.get('/products', async (req, res) => {
  try {
    const products = await fudo.fetchProducts();
    res.json({ success: true, count: products.length, data: products });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Register routes for both standalone Express and Netlify Function routing
app.use('/api', apiRouter);
app.use('/.netlify/functions/api', apiRouter);
app.use('/', apiRouter);

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`=================================================`);
    console.log(` Steakout KPI Dashboard Server running!`);
    console.log(` Local URL: http://localhost:${PORT}`);
    console.log(` Fudo Account: 45523 (beakers2) | User: 123 (ito_api)`);
    console.log(`=================================================`);
  });
}

module.exports = app;
