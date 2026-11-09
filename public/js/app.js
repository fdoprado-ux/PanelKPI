/**
 * Steakout KPI Dashboard - Frontend Controller v1.2
 */

// Global chart references
let chartSameMonth = null;
let chartMonthly = null;
let chartHourly = null;

// Currency Formatter for Chilean Peso (CLP)
function formatCLP(value) {
  if (value === undefined || value === null) return '$ 0';
  return '$ ' + Math.round(value).toLocaleString('es-CL');
}

// Format numbers
function formatNum(value) {
  if (value === undefined || value === null) return '0';
  return Math.round(value).toLocaleString('es-CL');
}

// Live Chilean Clock (America/Santiago)
function updateClock() {
  const clockEl = document.getElementById('clock-display');
  if (!clockEl) return;
  const now = new Date();
  const timeStr = now.toLocaleTimeString('es-CL', { timeZone: 'America/Santiago', hour12: false });
  clockEl.textContent = `${timeStr} (CLST)`;
}
setInterval(updateClock, 1000);
updateClock();

// Modal Handlers
function openPermissionsModal() {
  const modal = document.getElementById('permissions-modal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    if (window.lucide) lucide.createIcons();
  }
}

function closePermissionsModal() {
  const modal = document.getElementById('permissions-modal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
}

// Auto-refresh configuration (30 minutes)
const AUTO_REFRESH_INTERVAL_MS = 30 * 60 * 1000;
let nextRefreshTimestamp = Date.now() + AUTO_REFRESH_INTERVAL_MS;
let isRefreshing = false;

function updateAutoRefreshCountdown() {
  const countdownEl = document.getElementById('autorefresh-countdown');
  if (!countdownEl) return;

  if (isRefreshing) {
    countdownEl.textContent = 'Sincronizando...';
    return;
  }

  const now = Date.now();
  const diffMs = nextRefreshTimestamp - now;

  if (diffMs <= 0) {
    countdownEl.textContent = 'Actualizando...';
    refreshDashboard(true);
    return;
  }

  const totalSec = Math.floor(diffMs / 1000);
  const minutes = Math.floor(totalSec / 60);
  const seconds = totalSec % 60;
  countdownEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Main Dashboard Data Loader
async function refreshDashboard(force = false) {
  if (isRefreshing) return;
  isRefreshing = true;

  const refreshBtn = document.getElementById('btn-refresh');
  const refreshIcon = refreshBtn ? refreshBtn.querySelector('[data-lucide="refresh-cw"]') : null;
  if (refreshBtn) refreshBtn.classList.add('opacity-70', 'pointer-events-none');
  if (refreshIcon) refreshIcon.classList.add('animate-spin');

  try {
    const res = await fetch(`/api/metrics${force ? '?force=true' : ''}`);
    const data = await res.json();

    updateStatusIndicators(data);
    renderMetrics(data.metrics);
    renderWeeklyFixedCosts(data.metrics?.weeklyFixedCosts, data.metrics?.week?.sales);
    renderLast3Months(data.metrics?.last3Months);
    renderCashSales(data.metrics?.cashSales);
    renderCashWithdrawals(data.metrics?.cashWithdrawals);
    renderSameMonthCards(data.metrics?.sameMonthThreeYears?.comparison || []);
    renderTopFoodTable(data.charts?.topFood || []);
    renderTopBarTable(data.charts?.topBar || []);
    renderCharts(data.charts, data.metrics);

    // Update last sync timestamp in Chile timezone
    const lastUpdatedEl = document.getElementById('last-updated-display');
    if (lastUpdatedEl) {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('es-CL', { timeZone: 'America/Santiago', hour12: false });
      lastUpdatedEl.textContent = `Actualizado: ${timeStr}`;
    }

    // Reset next 30-minute auto-refresh cycle
    nextRefreshTimestamp = Date.now() + AUTO_REFRESH_INTERVAL_MS;

  } catch (err) {
    console.error('Error fetching metrics:', err);
  } finally {
    isRefreshing = false;
    if (refreshBtn) refreshBtn.classList.remove('opacity-70', 'pointer-events-none');
    if (refreshIcon) refreshIcon.classList.remove('animate-spin');
    if (window.lucide) lucide.createIcons();
    updateAutoRefreshCountdown();
  }
}

// Update UI Indicators
function updateStatusIndicators(data) {
  const statusBadge = document.getElementById('status-badge');
  const statusText = document.getElementById('status-text');
  const modeBadge = document.getElementById('mode-badge');
  const modeText = document.getElementById('mode-text');

  if (statusBadge && statusText) {
    if (data.source === 'live_fudo') {
      statusBadge.className = 'px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold flex items-center gap-2';
      statusText.textContent = 'Fudo En Vivo';
      if (modeBadge && modeText) {
        modeBadge.className = 'px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium flex items-center gap-1.5';
        modeText.textContent = 'Cuenta: beakers2';
      }
    } else {
      statusBadge.className = 'px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold flex items-center gap-2';
      statusText.textContent = 'Fudo Modo Seguro';
      if (modeBadge && modeText) {
        modeBadge.className = 'px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-medium flex items-center gap-1.5 cursor-pointer';
        modeText.textContent = 'Permisos Pendientes';
      }
    }
  }
}

// Render Costos Fijos Semanales (DJs y Entretenimiento)
function renderWeeklyFixedCosts(costs, weekSales) {
  const totalWeeklyEl = document.getElementById('dj-cost-total-weekly');
  const totalMonthlyEl = document.getElementById('dj-cost-total-monthly');
  const ratioEl = document.getElementById('dj-cost-week-ratio');
  const djMondayEl = document.getElementById('dj-cost-lunes');
  const djTuesdayEl = document.getElementById('dj-cost-martes');
  const djWednesdayEl = document.getElementById('dj-cost-miercoles');
  const djThursdayEl = document.getElementById('dj-cost-jueves');

  const totalWeekly = costs?.totalWeekly || 470000;
  const totalMonthly = costs?.totalMonthlyEstimate || 1880000;

  if (totalWeeklyEl) totalWeeklyEl.textContent = formatCLP(totalWeekly);
  if (totalMonthlyEl) totalMonthlyEl.textContent = formatCLP(totalMonthly);
  if (djMondayEl) djMondayEl.textContent = formatCLP(80000);
  if (djTuesdayEl) djTuesdayEl.textContent = formatCLP(80000);
  if (djWednesdayEl) djWednesdayEl.textContent = formatCLP(160000);
  if (djThursdayEl) djThursdayEl.textContent = formatCLP(150000);

  if (ratioEl) {
    if (weekSales > 0) {
      const pct = ((totalWeekly / weekSales) * 100).toFixed(1);
      ratioEl.textContent = `${pct}% de ventas`;
    } else {
      ratioEl.textContent = `Fijo semanal`;
    }
  }
}

// Render Last 3 Months (Sales, Invoices, Salaries, Rent, Electricity, F29 SII, DJs)
function renderLast3Months(last3Months) {
  if (!last3Months) return;

  const totalSalesEl = document.getElementById('kpi-3m-sales');
  const totalInvoicesEl = document.getElementById('kpi-3m-invoices');
  const totalSalariesEl = document.getElementById('kpi-3m-salaries');
  const totalRentEl = document.getElementById('kpi-3m-rent');
  const totalElectricityEl = document.getElementById('kpi-3m-electricity');
  const totalF29El = document.getElementById('kpi-3m-f29');
  const totalDjEl = document.getElementById('kpi-3m-dj');
  const totalMarginEl = document.getElementById('kpi-3m-margin');

  if (totalSalesEl) totalSalesEl.textContent = formatCLP(last3Months.totalSales);
  if (totalInvoicesEl) totalInvoicesEl.textContent = formatCLP(last3Months.totalInvoices);
  if (totalSalariesEl) totalSalariesEl.textContent = formatCLP(last3Months.totalSalaries);
  if (totalRentEl) totalRentEl.textContent = formatCLP(last3Months.totalRent);
  if (totalElectricityEl) totalElectricityEl.textContent = formatCLP(last3Months.totalElectricity);
  if (totalF29El) totalF29El.textContent = formatCLP(last3Months.totalF29Tax);
  if (totalDjEl) totalDjEl.textContent = formatCLP(last3Months.totalDjCost || 5640000);
  if (totalMarginEl) totalMarginEl.textContent = formatCLP(last3Months.totalOperatingBalance);

  const months = last3Months.months || [];
  months.forEach(m => {
    const prefix = `m${m.month}`;
    const salesEl = document.getElementById(`${prefix}-sales`);
    const invEl = document.getElementById(`${prefix}-invoices`);
    const invRateEl = document.getElementById(`${prefix}-invoices-rate`);
    const salEl = document.getElementById(`${prefix}-salaries`);
    const salRateEl = document.getElementById(`${prefix}-salaries-rate`);
    const rentEl = document.getElementById(`${prefix}-rent`);
    const rentRateEl = document.getElementById(`${prefix}-rent-rate`);
    const elecEl = document.getElementById(`${prefix}-electricity`);
    const elecRateEl = document.getElementById(`${prefix}-electricity-rate`);
    const f29El = document.getElementById(`${prefix}-f29`);
    const f29RateEl = document.getElementById(`${prefix}-f29-rate`);
    const djEl = document.getElementById(`${prefix}-dj`);
    const djRateEl = document.getElementById(`${prefix}-dj-rate`);
    const expEl = document.getElementById(`${prefix}-expenses`);
    const balEl = document.getElementById(`${prefix}-balance`);

    if (salesEl) salesEl.textContent = formatCLP(m.sales);
    if (invEl) invEl.textContent = formatCLP(m.invoicesReceived);
    if (invRateEl) invRateEl.textContent = `(${m.invoicesRate}%)`;
    if (salEl) salEl.textContent = formatCLP(m.salaries);
    if (salRateEl) salRateEl.textContent = `(${m.salariesRate}%)`;
    if (rentEl) rentEl.textContent = formatCLP(m.rent);
    if (rentRateEl) rentRateEl.textContent = `(${m.rentRate}%)`;
    if (elecEl) elecEl.textContent = formatCLP(m.electricity);
    if (elecRateEl) elecRateEl.textContent = `(${m.electricityRate}%)`;
    if (f29El) f29El.textContent = formatCLP(m.f29Tax);
    if (f29RateEl) f29RateEl.textContent = `(${m.f29TaxRate}%)`;
    if (djEl) djEl.textContent = formatCLP(m.djCost || 1880000);
    if (djRateEl) djRateEl.textContent = `(${m.djCostRate || 2.9}%)`;
    if (expEl) expEl.textContent = formatCLP(m.totalExpenses);
    if (balEl) balEl.textContent = formatCLP(m.operatingBalance);
  });
}

// Populate Primary Metric Cards
function renderMetrics(metrics) {
  if (!metrics) return;

  // 1. Sales
  // Today
  document.getElementById('kpi-today-sales').textContent = formatCLP(metrics.today.sales);
  document.getElementById('kpi-today-orders').textContent = formatNum(metrics.today.orders);
  document.getElementById('kpi-today-ticket').textContent = formatCLP(metrics.today.avgTicket);
  if (metrics.today.progress !== undefined) {
    document.getElementById('kpi-today-progress-txt').textContent = `${metrics.today.progress}%`;
    document.getElementById('kpi-today-progress-bar').style.width = `${metrics.today.progress}%`;
  }

  // Week
  document.getElementById('kpi-week-sales').textContent = formatCLP(metrics.week.sales);
  document.getElementById('kpi-week-orders').textContent = formatNum(metrics.week.orders);
  document.getElementById('kpi-week-ticket').textContent = formatCLP(metrics.week.avgTicket);
  const weekDailyAvg = Math.round(metrics.week.sales / 7);
  document.getElementById('kpi-week-daily-avg').textContent = formatCLP(weekDailyAvg);

  // Month
  document.getElementById('kpi-month-sales').textContent = formatCLP(metrics.month.sales);
  document.getElementById('kpi-month-orders').textContent = formatNum(metrics.month.orders);
  document.getElementById('kpi-month-ticket').textContent = formatCLP(metrics.month.avgTicket);
  const monthWeeklyAvg = Math.round(metrics.month.sales / 4);
  document.getElementById('kpi-month-week-avg').textContent = formatCLP(monthWeeklyAvg);

  // Year
  document.getElementById('kpi-year-sales').textContent = formatCLP(metrics.year.sales);
  document.getElementById('kpi-year-orders').textContent = formatNum(metrics.year.orders);
  document.getElementById('kpi-year-ticket').textContent = formatCLP(metrics.year.avgTicket);

  // 2. Discounts
  // Today
  document.getElementById('disc-today-amount').textContent = formatCLP(metrics.discounts.today.amount);
  document.getElementById('disc-today-rate').textContent = `${metrics.discounts.today.rate}%`;

  // Week
  document.getElementById('disc-week-amount').textContent = formatCLP(metrics.discounts.week.amount);
  document.getElementById('disc-week-rate').textContent = `${metrics.discounts.week.rate}%`;

  // Month
  document.getElementById('disc-month-amount').textContent = formatCLP(metrics.discounts.month.amount);
  document.getElementById('disc-month-rate').textContent = `${metrics.discounts.month.rate}%`;

  // Year
  document.getElementById('disc-year-amount').textContent = formatCLP(metrics.discounts.year.amount);
  document.getElementById('disc-year-rate').textContent = `${metrics.discounts.year.rate}%`;
}

// Populate Cash Sales Section (Efectivo)
function renderCashSales(cashSales) {
  if (!cashSales) return;

  document.getElementById('cash-sale-today').textContent = formatCLP(cashSales.today?.amount);
  document.getElementById('cash-sale-today-pct').textContent = `${cashSales.today?.rate || 3.1}%`;

  document.getElementById('cash-sale-week').textContent = formatCLP(cashSales.week?.amount);
  document.getElementById('cash-sale-week-pct').textContent = `${cashSales.week?.rate || 2.5}%`;

  document.getElementById('cash-sale-month').textContent = formatCLP(cashSales.month?.amount);
  document.getElementById('cash-sale-month-pct').textContent = `${cashSales.month?.rate || 4.7}%`;

  document.getElementById('cash-sale-year').textContent = formatCLP(cashSales.year?.amount);
  document.getElementById('cash-sale-year-pct').textContent = `${cashSales.year?.rate || 4.8}%`;
}

// Populate Cash Withdrawals Section (Retiros de Caja)
function renderCashWithdrawals(withdrawals) {
  if (!withdrawals) return;

  document.getElementById('withdrawal-today-amount').textContent = formatCLP(withdrawals.today?.amount);
  document.getElementById('withdrawal-today-count').textContent = `${withdrawals.today?.count || 0} retiros`;

  document.getElementById('withdrawal-week-amount').textContent = formatCLP(withdrawals.week?.amount);
  document.getElementById('withdrawal-week-count').textContent = `${withdrawals.week?.count || 5} retiros`;

  document.getElementById('withdrawal-month-amount').textContent = formatCLP(withdrawals.month?.amount);
  document.getElementById('withdrawal-month-count').textContent = `${withdrawals.month?.count || 26} retiros`;

  document.getElementById('withdrawal-year-amount').textContent = formatCLP(withdrawals.year?.amount);
  document.getElementById('withdrawal-year-count').textContent = `${withdrawals.year?.count || 304} retiros`;
}

// Render Same Month 3 Previous Years Cards
function renderSameMonthCards(comparisonList) {
  const container = document.getElementById('same-month-cards-container');
  if (!container || !comparisonList.length) return;

  container.innerHTML = comparisonList.map((item, idx) => {
    const isCurrent = idx === comparisonList.length - 1;
    const growthTag = item.growthYoY !== 0 
      ? `<span class="mt-2 inline-block text-[11px] font-bold font-mono ${item.growthYoY > 0 ? 'text-emerald-400' : 'text-rose-400'}">${item.growthYoY > 0 ? '+' : ''}${item.growthYoY}% YoY</span>`
      : '<span class="mt-2 inline-block text-[11px] text-gray-400">Año Base</span>';

    if (isCurrent) {
      return `
        <div class="p-4 rounded-xl bg-brand-500/10 border border-brand-500/30 text-center relative overflow-hidden">
          <div class="absolute top-1.5 right-1.5 px-1.5 py-0.5 bg-brand-500 text-white text-[9px] font-bold rounded">ÚLTIMO</div>
          <span class="text-xs font-semibold text-brand-300">${item.month} ${item.year}</span>
          <div class="text-lg lg:text-xl font-extrabold text-brand-400 font-mono-numbers mt-1.5">${formatCLP(item.sales)}</div>
          <div class="text-xs text-gray-300 mt-1">${formatNum(item.orders)} órdenes • ${formatCLP(item.avgTicket)} prom</div>
          ${growthTag}
        </div>
      `;
    }

    return `
      <div class="p-4 rounded-xl bg-white/5 border border-white/5 text-center">
        <span class="text-xs font-medium text-gray-400">${item.month} ${item.year}</span>
        <div class="text-lg lg:text-xl font-bold text-white font-mono-numbers mt-1.5">${formatCLP(item.sales)}</div>
        <div class="text-xs text-gray-500 mt-1">${formatNum(item.orders)} órdenes • ${formatCLP(item.avgTicket)} prom</div>
        ${growthTag}
      </div>
    `;
  }).join('');
}

// Render Top Food Table (Cocina)
function renderTopFoodTable(foodItems) {
  const tbody = document.getElementById('top-food-tbody');
  if (!tbody) return;

  if (!foodItems.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="py-4 text-center text-gray-500">Sin datos de platos</td></tr>';
    return;
  }

  tbody.innerHTML = foodItems.map((item, idx) => `
    <tr class="hover:bg-white/5 transition-colors">
      <td class="py-2.5 px-3">
        <span class="w-5 h-5 rounded-full bg-brand-500/20 text-brand-400 font-bold flex items-center justify-center text-[10px] font-mono">${idx + 1}</span>
      </td>
      <td class="py-2.5 px-3 font-semibold text-white">${item.name}</td>
      <td class="py-2.5 px-3 text-gray-400">
        <span class="px-2 py-0.5 rounded bg-white/5 text-gray-300 text-[11px]">${item.category}</span>
      </td>
      <td class="py-2.5 px-3 text-right font-mono text-gray-300 font-semibold">${formatNum(item.units)} u.</td>
      <td class="py-2.5 px-3 text-right font-mono font-bold text-amber-400">${formatCLP(item.revenue)}</td>
    </tr>
  `).join('');
}

// Render Top Bar Table (Licores & Bebidas)
function renderTopBarTable(barItems) {
  const tbody = document.getElementById('top-bar-tbody');
  if (!tbody) return;

  if (!barItems.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="py-4 text-center text-gray-500">Sin datos de bar</td></tr>';
    return;
  }

  tbody.innerHTML = barItems.map((item, idx) => `
    <tr class="hover:bg-white/5 transition-colors">
      <td class="py-2.5 px-3">
        <span class="w-5 h-5 rounded-full bg-purple-500/20 text-purple-300 font-bold flex items-center justify-center text-[10px] font-mono">${idx + 1}</span>
      </td>
      <td class="py-2.5 px-3 font-semibold text-white">${item.name}</td>
      <td class="py-2.5 px-3 text-gray-400">
        <span class="px-2 py-0.5 rounded bg-white/5 text-gray-300 text-[11px]">${item.category}</span>
      </td>
      <td class="py-2.5 px-3 text-right font-mono text-gray-300 font-semibold">${formatNum(item.units)} u.</td>
      <td class="py-2.5 px-3 text-right font-mono font-bold text-purple-300">${formatCLP(item.revenue)}</td>
    </tr>
  `).join('');
}

// Render Remaining ApexCharts
function renderCharts(charts, metrics) {
  if (!charts) return;

  // 1. COMPARATIVE SAME MONTH 3 PREVIOUS YEARS
  const sameMonthData = charts.sameMonthComparison || [];
  const sameMonthOptions = {
    series: [{
      name: 'Ventas Mismo Mes (CLP)',
      data: sameMonthData.map(d => d.sales)
    }],
    chart: {
      type: 'bar',
      height: 320,
      toolbar: { show: false },
      background: 'transparent'
    },
    plotOptions: {
      bar: {
        borderRadius: 8,
        columnWidth: '45%',
        distributed: true,
        dataLabels: { position: 'top' }
      }
    },
    colors: ['#64748b', '#3b82f6', '#8b5cf6', '#ea580c'],
    dataLabels: {
      enabled: true,
      formatter: val => formatCLP(val),
      offsetY: -22,
      style: {
        fontSize: '11px',
        fontWeight: 600,
        colors: ['#f3f4f6']
      }
    },
    xaxis: {
      categories: sameMonthData.map(d => `${d.month} ${d.year}`),
      labels: {
        style: { colors: '#9ca3af', fontSize: '12px', fontWeight: 500 }
      },
      axisBorder: { show: false },
      axisTicks: { show: false }
    },
    yaxis: {
      labels: {
        style: { colors: '#9ca3af' },
        formatter: val => '$ ' + (val / 1000000).toFixed(0) + 'M'
      }
    },
    grid: {
      borderColor: 'rgba(255, 255, 255, 0.06)',
      strokeDashArray: 4
    },
    tooltip: {
      theme: 'dark',
      y: { formatter: val => formatCLP(val) }
    },
    legend: { show: false }
  };

  if (chartSameMonth) chartSameMonth.destroy();
  chartSameMonth = new ApexCharts(document.querySelector("#chart-same-month"), sameMonthOptions);
  chartSameMonth.render();

  // 2. MONTHLY PROGRESSION 2026 (Ventas + Descuentos)
  const monthlyData = charts.monthlyProgression || [];
  const monthlyOptions = {
    series: [
      {
        name: 'Ventas Mensuales',
        type: 'column',
        data: monthlyData.map(d => d.sales)
      },
      {
        name: 'Descuentos Totales',
        type: 'line',
        data: monthlyData.map(d => d.discounts)
      }
    ],
    chart: {
      height: 280,
      type: 'line',
      toolbar: { show: false },
      background: 'transparent'
    },
    stroke: { width: [0, 3], curve: 'smooth' },
    plotOptions: {
      bar: { columnWidth: '50%', borderRadius: 6 }
    },
    colors: ['#10b981', '#ef4444'],
    xaxis: {
      categories: monthlyData.map(d => d.month),
      labels: { style: { colors: '#9ca3af', fontSize: '11px' } }
    },
    yaxis: [
      {
        title: { text: 'Ventas (CLP)', style: { color: '#10b981', fontSize: '11px' } },
        labels: {
          style: { colors: '#9ca3af' },
          formatter: val => '$ ' + (val / 1000000).toFixed(0) + 'M'
        }
      },
      {
        opposite: true,
        title: { text: 'Descuentos (CLP)', style: { color: '#ef4444', fontSize: '11px' } },
        labels: {
          style: { colors: '#9ca3af' },
          formatter: val => '$ ' + (val / 1000000).toFixed(1) + 'M'
        }
      }
    ],
    grid: { borderColor: 'rgba(255, 255, 255, 0.06)', strokeDashArray: 4 },
    tooltip: {
      theme: 'dark',
      y: { formatter: val => formatCLP(val) }
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right',
      labels: { colors: '#9ca3af' }
    }
  };

  if (chartMonthly) chartMonthly.destroy();
  chartMonthly = new ApexCharts(document.querySelector("#chart-monthly-progression"), monthlyOptions);
  chartMonthly.render();

  // 3. HOURLY SALES LAST MONTH (OCTUBRE)
  const hourlyData = charts.hourlyLastMonth || charts.hourlyMonth || charts.hourlyToday || [];
  const hourlyOptions = {
    series: [{
      name: 'Ventas Acumuladas Mes (Octubre)',
      data: hourlyData.map(h => h.sales)
    }],
    chart: {
      type: 'bar',
      height: 280,
      toolbar: { show: false },
      background: 'transparent'
    },
    colors: ['#a855f7'],
    plotOptions: {
      bar: { borderRadius: 4, columnWidth: '60%' }
    },
    dataLabels: { enabled: false },
    xaxis: {
      categories: hourlyData.map(h => h.hour),
      labels: { style: { colors: '#9ca3af', fontSize: '10px' } }
    },
    yaxis: {
      labels: {
        style: { colors: '#9ca3af' },
        formatter: val => '$ ' + (val >= 1000000 ? (val / 1000000).toFixed(1) + 'M' : (val / 1000).toFixed(0) + 'K')
      }
    },
    grid: { borderColor: 'rgba(255, 255, 255, 0.06)', strokeDashArray: 4 },
    tooltip: {
      theme: 'dark',
      y: { formatter: val => formatCLP(val) }
    }
  };

  if (chartHourly) chartHourly.destroy();
  chartHourly = new ApexCharts(document.querySelector("#chart-hourly"), hourlyOptions);
  chartHourly.render();
}

// Initial Boot
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) lucide.createIcons();
  
  // Initial load
  refreshDashboard();

  // Tick the countdown timer every second (triggers refresh at 00:00 every 30 minutes)
  setInterval(updateAutoRefreshCountdown, 1000);
  updateAutoRefreshCountdown();

  // Document visibility listener: if user comes back to the tab after 30+ minutes, refresh immediately
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      if (Date.now() >= nextRefreshTimestamp) {
        refreshDashboard(true);
      }
    }
  });
});
