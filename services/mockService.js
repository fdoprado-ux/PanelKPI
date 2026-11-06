/**
 * Mock & Simulation Service for Steakout Restaurant
 * Calibrated with real menu items, categories, rooms, and Chilean CLP currency.
 */

class MockService {
  static getMetrics(options = {}) {
    const now = new Date();
    const currentYear = now.getFullYear();
    const monthNames = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
    const currentMonthIndex = now.getMonth();
    const currentMonthName = monthNames[currentMonthIndex];

    // Today's Sales
    const todaySales = 2485900;
    const todayOrders = 78;
    const todayAvgTicket = Math.round(todaySales / todayOrders);
    const todayTarget = 2800000;
    const todayProgress = Math.min(100, Math.round((todaySales / todayTarget) * 100));

    // Last Week (7 days)
    const weekSales = 19840500;
    const weekOrders = 612;
    const weekAvgTicket = Math.round(weekSales / weekOrders);
    const weekGrowth = 8.4; // vs previous week

    // Last Month (past 30 days / previous month)
    const monthSales = 84620000;
    const monthOrders = 2580;
    const monthAvgTicket = Math.round(monthSales / monthOrders);
    const monthGrowth = 6.2; // vs prior month

    // Current Year (Year-to-date)
    const yearSales = 918450000;
    const yearOrders = 28140;
    const yearAvgTicket = Math.round(yearSales / yearOrders);
    const yearGrowth = 12.8;

    // Discounts
    const discountsToday = 142000;
    const discountsTodayRate = Number(((discountsToday / (todaySales + discountsToday)) * 100).toFixed(1));

    const discountsWeek = 1120000;
    const discountsWeekRate = Number(((discountsWeek / (weekSales + discountsWeek)) * 100).toFixed(1));

    const discountsMonth = 4580000;
    const discountsMonthRate = Number(((discountsMonth / (monthSales + discountsMonth)) * 100).toFixed(1));

    const discountsYear = 49650000;
    const discountsYearRate = Number(((discountsYear / (yearSales + discountsYear)) * 100).toFixed(1));

    // Same month across previous 3 years:
    // e.g. Noviembre 2026 (Actual/Run-rate), Noviembre 2025, Noviembre 2024, Noviembre 2023
    const sameMonthComparison = [
      {
        year: currentYear - 3,
        yearLabel: `${currentYear - 3}`,
        month: currentMonthName,
        sales: 59400000,
        orders: 2010,
        avgTicket: 29552,
        growthYoY: 0
      },
      {
        year: currentYear - 2,
        yearLabel: `${currentYear - 2}`,
        month: currentMonthName,
        sales: 69800000,
        orders: 2260,
        avgTicket: 30885,
        growthYoY: 17.5
      },
      {
        year: currentYear - 1,
        yearLabel: `${currentYear - 1}`,
        month: currentMonthName,
        sales: 79250000,
        orders: 2470,
        avgTicket: 32085,
        growthYoY: 13.5
      },
      {
        year: currentYear,
        yearLabel: `${currentYear} (Actual)`,
        month: currentMonthName,
        sales: 88900000,
        orders: 2680,
        avgTicket: 33171,
        growthYoY: 12.2
      }
    ];

    // Weekly sales breakdown by day (Mon - Sun)
    const daysOfWeek = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    const weekDailyBreakdown = [
      { day: 'Lunes', sales: 1850000, lastWeekSales: 1720000, orders: 58, discounts: 98000 },
      { day: 'Martes', sales: 2100000, lastWeekSales: 1980000, orders: 66, discounts: 115000 },
      { day: 'Miércoles', sales: 2450000, lastWeekSales: 2250000, orders: 76, discounts: 132000 },
      { day: 'Jueves', sales: 2980000, lastWeekSales: 2750000, orders: 92, discounts: 165000 },
      { day: 'Viernes', sales: 4120000, lastWeekSales: 3850000, orders: 124, discounts: 240000 },
      { day: 'Sábado', sales: 4450000, lastWeekSales: 4100000, orders: 135, discounts: 250000 },
      { day: 'Domingo', sales: 1890500, lastWeekSales: 1650000, orders: 61, discounts: 120000 }
    ];

    // Monthly sales progression for current year (Jan - Nov)
    const monthlyProgression2026 = [
      { month: 'Ene', sales: 81200000, discounts: 4350000 },
      { month: 'Feb', sales: 86500000, discounts: 4620000 },
      { month: 'Mar', sales: 78900000, discounts: 4210000 },
      { month: 'Abr', sales: 79400000, discounts: 4280000 },
      { month: 'May', sales: 83100000, discounts: 4500000 },
      { month: 'Jun', sales: 82400000, discounts: 4420000 },
      { month: 'Jul', sales: 87900000, discounts: 4710000 },
      { month: 'Ago', sales: 85600000, discounts: 4600000 },
      { month: 'Sep', sales: 91200000, discounts: 4950000 }, // Fiestas Patrias boost!
      { month: 'Oct', sales: 84620000, discounts: 4580000 },
      { month: 'Nov', sales: 88900000, discounts: 4790000 } // Current month
    ];

    // Sales channel distribution
    const channelDistribution = [
      { channel: 'Salón (Eat-In)', percentage: 63, sales: Math.round(monthSales * 0.63) },
      { channel: 'Delivery (PedidosYa / Uber / Rappi)', percentage: 24, sales: Math.round(monthSales * 0.24) },
      { channel: 'Para Llevar (Takeaway)', percentage: 13, sales: Math.round(monthSales * 0.13) }
    ];

    // Sales by Room (from Steakout's real rooms)
    const roomDistribution = [
      { room: 'PATIO', sales: 33848000, percentage: 40 },
      { room: '2do Piso', sales: 25386000, percentage: 30 },
      { room: 'BARRA', sales: 16924000, percentage: 20 },
      { room: 'CALLE', sales: 8462000, percentage: 10 }
    ];

    // Top Selling Products (Real products from Steakout Fudo catalog)
    const topProducts = [
      { name: 'Smoked Sampler', category: 'From The SMOKER', price: 11500, units: 642, revenue: 7383000 },
      { name: 'BBQ CW x 12', category: 'Starters', price: 7990, units: 820, revenue: 6551800 },
      { name: 'Buffalo CW x 12', category: 'Starters', price: 7990, units: 760, revenue: 6072400 },
      { name: 'Sampler Camarones', category: 'Starters', price: 10990, units: 510, revenue: 5604900 },
      { name: 'Fried Shrimp (12 Unidades)', category: 'Starters', price: 8990, units: 490, revenue: 4405100 },
      { name: 'Chicken Tenders (8 Unidades)', category: 'Starters', price: 5600, units: 710, revenue: 3976000 },
      { name: 'Papas Fritas Starter', category: 'Starters', price: 3900, units: 980, revenue: 3822000 }
    ];

    // Discount breakdown by category
    const discountBreakdown = [
      { name: 'Promociones Menú / Happy Hour', amount: Math.round(discountsMonth * 0.42), percentage: 42 },
      { name: 'Convenios Apps Delivery', amount: Math.round(discountsMonth * 0.28), percentage: 28 },
      { name: 'Cortesías & Fidelización', amount: Math.round(discountsMonth * 0.18), percentage: 18 },
      { name: 'Descuento Personal Steakout', amount: Math.round(discountsMonth * 0.12), percentage: 12 }
    ];

    // Hourly distribution today & last month
    const hourlySalesToday = [
      { hour: '12:00', sales: 125000, orders: 4 },
      { hour: '13:00', sales: 340000, orders: 11 },
      { hour: '14:00', sales: 490000, orders: 15 },
      { hour: '15:00', sales: 280000, orders: 9 },
      { hour: '16:00', sales: 95000, orders: 3 },
      { hour: '17:00', sales: 70000, orders: 2 },
      { hour: '18:00', sales: 110000, orders: 4 },
      { hour: '19:00', sales: 185000, orders: 6 },
      { hour: '20:00', sales: 320000, orders: 10 },
      { hour: '21:00', sales: 290900, orders: 9 },
      { hour: '22:00', sales: 170000, orders: 5 }
    ];

    const hourlySalesMonth = [
      { hour: '12:00', sales: 486461 },
      { hour: '13:00', sales: 4308834 },
      { hour: '14:00', sales: 4070668 },
      { hour: '15:00', sales: 1708673 },
      { hour: '16:00', sales: 1696852 },
      { hour: '17:00', sales: 2149053 },
      { hour: '18:00', sales: 3248988 },
      { hour: '19:00', sales: 7065178 },
      { hour: '20:00', sales: 10298192 },
      { hour: '21:00', sales: 11740938 },
      { hour: '22:00', sales: 6712405 },
      { hour: '23:00', sales: 5329851 },
      { hour: '00:00', sales: 3750945 },
      { hour: '01:00', sales: 1238070 },
      { hour: '02:00', sales: 152159 }
    ];

    const last3MonthsData = [
      {
        year: 2026,
        month: 10,
        monthName: 'Octubre',
        sales: 63961266,
        invoicesReceived: 24747769,
        salaries: 15591778,
        rent: 4711018,
        electricity: 2000000,
        invoicesRate: 38.7,
        salariesRate: 24.4,
        rentRate: 7.4,
        electricityRate: 3.1,
        totalExpenses: 47050565,
        operatingBalance: 16910701
      },
      {
        year: 2026,
        month: 9,
        monthName: 'Septiembre',
        sales: 61355284,
        invoicesReceived: 25022624,
        salaries: 14289532,
        rent: 4699360,
        electricity: 2000000,
        invoicesRate: 40.8,
        salariesRate: 23.3,
        rentRate: 7.7,
        electricityRate: 3.3,
        totalExpenses: 46011516,
        operatingBalance: 15343768
      },
      {
        year: 2026,
        month: 8,
        monthName: 'Agosto',
        sales: 72734562,
        invoicesReceived: 29457385,
        salaries: 15413920,
        rent: 4697060,
        electricity: 2000000,
        invoicesRate: 40.5,
        salariesRate: 21.2,
        rentRate: 6.5,
        electricityRate: 2.7,
        totalExpenses: 51568365,
        operatingBalance: 21166197
      }
    ];

    const last3Months = {
      period: 'Agosto - Octubre 2026',
      totalSales: 198051112,
      totalInvoices: 79227778,
      totalSalaries: 45295230,
      totalRent: 14107438,
      totalElectricity: 6000000,
      totalExpenses: 144630446,
      totalOperatingBalance: 53420666,
      months: last3MonthsData
    };

    return {
      restaurant: 'Steakout',
      currency: 'CLP',
      currencySymbol: '$',
      timezone: 'America/Santiago',
      timestamp: new Date().toISOString(),
      source: 'simulated_permission_required',
      metrics: {
        // 1. Sales
        today: {
          sales: todaySales,
          orders: todayOrders,
          avgTicket: todayAvgTicket,
          target: todayTarget,
          progress: todayProgress
        },
        week: {
          sales: weekSales,
          orders: weekOrders,
          avgTicket: weekAvgTicket,
          growthYoY: weekGrowth
        },
        month: {
          sales: monthSales,
          orders: monthOrders,
          avgTicket: monthAvgTicket,
          growthYoY: monthGrowth,
          monthName: currentMonthName
        },
        year: {
          sales: yearSales,
          orders: yearOrders,
          avgTicket: yearAvgTicket,
          growthYoY: yearGrowth,
          year: currentYear
        },
        // 2. Same Month 3 Previous Years
        sameMonthThreeYears: {
          currentMonth: currentMonthName,
          comparison: sameMonthComparison
        },
        // 3. Discounts
        discounts: {
          today: {
            amount: discountsToday,
            rate: discountsTodayRate
          },
          week: {
            amount: discountsWeek,
            rate: discountsWeekRate
          },
          month: {
            amount: discountsMonth,
            rate: discountsMonthRate
          },
          year: {
            amount: discountsYear,
            rate: discountsYearRate
          },
          breakdown: discountBreakdown
        },
        last3Months
      },
      charts: {
        weeklyDays: weekDailyBreakdown,
        monthlyProgression: monthlyProgression2026,
        sameMonthComparison: sameMonthComparison,
        channels: channelDistribution,
        rooms: roomDistribution,
        topProducts: topProducts,
        hourlyToday: hourlySalesToday,
        hourlyMonth: hourlySalesMonth,
        hourlyLastMonth: hourlySalesMonth
      }
    };
  }
}

module.exports = MockService;
