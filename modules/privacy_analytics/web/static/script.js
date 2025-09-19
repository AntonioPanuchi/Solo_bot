// JavaScript для Privacy-Compliant Analytics Dashboard

class PrivacyAnalytics {
    constructor() {
        this.refreshInterval = 30000; // 30 секунд
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeCharts();
        this.startAutoRefresh();
        this.setupNotifications();
    }

    setupEventListeners() {
        // Обработчики для кнопок обновления
        document.querySelectorAll('.refresh-btn').forEach(btn => {
            btn.addEventListener('click', () => this.refreshData());
        });

        // Обработчики для алертов
        document.querySelectorAll('.alert-acknowledge').forEach(btn => {
            btn.addEventListener('click', (e) => this.acknowledgeAlert(e.target.dataset.alertId));
        });

        document.querySelectorAll('.alert-resolve').forEach(btn => {
            btn.addEventListener('click', (e) => this.resolveAlert(e.target.dataset.alertId));
        });
    }

    initializeCharts() {
        // Инициализация всех графиков
        this.initBandwidthChart();
        this.initConnectionsChart();
        this.initRevenueChart();
        this.initGeoChart();
    }

    initBandwidthChart() {
        const ctx = document.getElementById('bandwidthChart');
        if (!ctx) return;

        this.charts.bandwidth = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Пропускная способность (Mbps)',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Mbps'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Время'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }

    initConnectionsChart() {
        const ctx = document.getElementById('connectionsChart');
        if (!ctx) return;

        this.charts.connections = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Активные', 'Новые', 'Отключенные'],
                datasets: [{
                    label: 'Подключения',
                    data: [150, 25, 10],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(255, 99, 132, 0.8)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    initRevenueChart() {
        const ctx = document.getElementById('revenueChart');
        if (!ctx) return;

        this.charts.revenue = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['1 месяц', '3 месяца', '6 месяцев', '12 месяцев'],
                datasets: [{
                    data: [30, 40, 20, 10],
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    initGeoChart() {
        const ctx = document.getElementById('geoChart');
        if (!ctx) return;

        this.charts.geo = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['US', 'DE', 'RU', 'FR', 'UK'],
                datasets: [{
                    label: 'Пользователи',
                    data: [45, 35, 25, 15, 10],
                    backgroundColor: 'rgba(153, 102, 255, 0.8)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    async refreshData() {
        try {
            this.showLoading();
            
            // Обновляем данные в реальном времени
            const realtimeData = await this.fetchData('/api/data/realtime');
            this.updateRealtimeData(realtimeData);
            
            // Обновляем бизнес-данные
            const businessData = await this.fetchData('/api/data/business');
            this.updateBusinessData(businessData);
            
            // Обновляем административные данные
            const adminData = await this.fetchData('/api/data/admin');
            this.updateAdminData(adminData);
            
            this.hideLoading();
            this.showNotification('Данные обновлены', 'success');
            
        } catch (error) {
            console.error('Ошибка обновления данных:', error);
            this.hideLoading();
            this.showNotification('Ошибка обновления данных', 'error');
        }
    }

    async fetchData(url) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    updateRealtimeData(data) {
        // Обновляем метрики
        if (data.current_metrics) {
            this.updateMetric('.metric-value', data.current_metrics.active_connections);
        }
        
        // Обновляем статус серверов
        if (data.server_status) {
            this.updateServerStatus(data.server_status);
        }
        
        // Обновляем алерты
        if (data.alerts) {
            this.updateAlerts(data.alerts);
        }
        
        // Обновляем графики
        if (data.performance_graphs) {
            this.updatePerformanceGraphs(data.performance_graphs);
        }
    }

    updateBusinessData(data) {
        // Обновляем бизнес-метрики
        if (data.user_metrics) {
            this.updateMetric('.user-metric', data.user_metrics.total_users);
        }
        
        if (data.revenue_metrics) {
            this.updateMetric('.revenue-metric', data.revenue_metrics.daily_revenue);
        }
    }

    updateAdminData(data) {
        // Обновляем административные данные
        if (data.system_overview) {
            this.updateSystemOverview(data.system_overview);
        }
    }

    updateMetric(selector, value) {
        const element = document.querySelector(selector);
        if (element) {
            element.textContent = value;
        }
    }

    updateServerStatus(serverStatus) {
        // Обновляем таблицу серверов
        const tbody = document.querySelector('.server-table tbody');
        if (tbody && serverStatus.servers) {
            tbody.innerHTML = serverStatus.servers.map(server => `
                <tr>
                    <td>${server.name}</td>
                    <td>
                        <span class="status-indicator status-${server.status}"></span>
                        ${server.status.charAt(0).toUpperCase() + server.status.slice(1)}
                    </td>
                    <td>${server.cpu_usage.toFixed(1)}%</td>
                    <td>${server.memory_usage.toFixed(1)}%</td>
                    <td>${server.connections}</td>
                </tr>
            `).join('');
        }
    }

    updateAlerts(alerts) {
        // Обновляем список алертов
        const alertsContainer = document.querySelector('.alerts-container');
        if (alertsContainer && alerts.alerts) {
            if (alerts.alerts.length === 0) {
                alertsContainer.innerHTML = `
                    <div class="text-center text-muted">
                        <i class="fas fa-check-circle fa-2x mb-2"></i>
                        <p>Нет активных алертов</p>
                    </div>
                `;
            } else {
                alertsContainer.innerHTML = alerts.alerts.slice(0, 5).map(alert => `
                    <div class="alert alert-${alert.severity === 'critical' ? 'danger' : alert.severity === 'warning' ? 'warning' : 'info'} alert-sm">
                        <small>
                            <strong>${alert.severity.charAt(0).toUpperCase() + alert.severity.slice(1)}:</strong> 
                            ${alert.message}
                        </small>
                    </div>
                `).join('');
            }
        }
    }

    updatePerformanceGraphs(graphs) {
        // Обновляем график пропускной способности
        if (this.charts.bandwidth && graphs.bandwidth_trend) {
            const labels = graphs.bandwidth_trend.map(point => 
                new Date(point.timestamp).toLocaleTimeString()
            );
            const data = graphs.bandwidth_trend.map(point => point.bandwidth_mbps);
            
            this.charts.bandwidth.data.labels = labels;
            this.charts.bandwidth.data.datasets[0].data = data;
            this.charts.bandwidth.update();
        }
        
        // Обновляем график подключений
        if (this.charts.connections && graphs.connections_trend) {
            const data = graphs.connections_trend.map(point => point.total_connections);
            this.charts.connections.data.datasets[0].data = data;
            this.charts.connections.update();
        }
    }

    async acknowledgeAlert(alertId) {
        try {
            const response = await fetch(`/api/alerts/${alertId}/acknowledge`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    acknowledged_by: 'user'
                })
            });
            
            if (response.ok) {
                this.showNotification('Алерт подтвержден', 'success');
                this.refreshData();
            } else {
                throw new Error('Ошибка подтверждения алерта');
            }
        } catch (error) {
            console.error('Ошибка подтверждения алерта:', error);
            this.showNotification('Ошибка подтверждения алерта', 'error');
        }
    }

    async resolveAlert(alertId) {
        try {
            const response = await fetch(`/api/alerts/${alertId}/resolve`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resolved_by: 'user'
                })
            });
            
            if (response.ok) {
                this.showNotification('Алерт разрешен', 'success');
                this.refreshData();
            } else {
                throw new Error('Ошибка разрешения алерта');
            }
        } catch (error) {
            console.error('Ошибка разрешения алерта:', error);
            this.showNotification('Ошибка разрешения алерта', 'error');
        }
    }

    startAutoRefresh() {
        setInterval(() => {
            this.refreshData();
        }, this.refreshInterval);
    }

    showLoading() {
        const loadingElements = document.querySelectorAll('.loading-indicator');
        loadingElements.forEach(el => el.style.display = 'inline-block');
    }

    hideLoading() {
        const loadingElements = document.querySelectorAll('.loading-indicator');
        loadingElements.forEach(el => el.style.display = 'none');
    }

    setupNotifications() {
        // Создаем контейнер для уведомлений
        if (!document.querySelector('.notifications-container')) {
            const container = document.createElement('div');
            container.className = 'notifications-container';
            container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1050;';
            document.body.appendChild(container);
        }
    }

    showNotification(message, type = 'info') {
        const container = document.querySelector('.notifications-container');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;

        container.appendChild(notification);

        // Автоматически удаляем уведомление через 5 секунд
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Утилиты для работы с данными
    formatNumber(num) {
        return new Intl.NumberFormat('ru-RU').format(num);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: 'RUB'
        }).format(amount);
    }

    formatBytes(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (bytes === 0) return '0 Bytes';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }

    formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
    window.privacyAnalytics = new PrivacyAnalytics();
});

// Обработка ошибок
window.addEventListener('error', (event) => {
    console.error('Глобальная ошибка:', event.error);
    if (window.privacyAnalytics) {
        window.privacyAnalytics.showNotification('Произошла ошибка в приложении', 'error');
    }
});

// Обработка необработанных промисов
window.addEventListener('unhandledrejection', (event) => {
    console.error('Необработанное отклонение промиса:', event.reason);
    if (window.privacyAnalytics) {
        window.privacyAnalytics.showNotification('Ошибка загрузки данных', 'error');
    }
});
