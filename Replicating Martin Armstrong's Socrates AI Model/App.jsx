import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, RadialBarChart, RadialBar
} from 'recharts';
import './App.css';

// Mobile-optimized Socrates AI Dashboard
const MobileSocratesAI = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isMobile, setIsMobile] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [validationData, setValidationData] = useState(null);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);

  // Detect mobile device
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = new WebSocket('ws://localhost:5000/ws');
        
        ws.onopen = () => {
          setConnectionStatus('connected');
          addNotification('Connected to Socrates AI', 'success');
        };
        
        ws.onmessage = (event) => {
          const message = JSON.parse(event.data);
          handleWebSocketMessage(message);
        };
        
        ws.onclose = () => {
          setConnectionStatus('disconnected');
          addNotification('Connection lost', 'warning');
          // Attempt to reconnect after 5 seconds
          setTimeout(connectWebSocket, 5000);
        };
        
        ws.onerror = () => {
          setConnectionStatus('error');
          addNotification('Connection error', 'error');
        };
        
        return ws;
      } catch (error) {
        console.error('WebSocket connection failed:', error);
        setConnectionStatus('error');
      }
    };

    const ws = connectWebSocket();
    return () => {
      if (ws) ws.close();
    };
  }, []);

  const handleWebSocketMessage = useCallback((message) => {
    switch (message.type) {
      case 'market_update':
        setData(prevData => ({
          ...prevData,
          marketData: message.data
        }));
        break;
      case 'analysis_update':
        setData(prevData => ({
          ...prevData,
          analysis: message.data
        }));
        break;
      case 'alert':
        addNotification(message.message, message.priority);
        break;
      case 'validation_update':
        setValidationData(message.data);
        break;
      case 'performance_update':
        setPerformanceMetrics(message.data);
        break;
      default:
        console.log('Unknown message type:', message.type);
    }
  }, []);

  const addNotification = useCallback((message, type = 'info') => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setNotifications(prev => [notification, ...prev.slice(0, 4)]);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  }, []);

  // Fetch data from API
  const fetchData = useCallback(async (endpoint, mobile = false) => {
    setLoading(true);
    setError(null);
    
    try {
      const mobileParam = mobile ? '?mobile=true' : '';
      const response = await fetch(`http://localhost:5000/api/socrates/${endpoint}${mobileParam}`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('API Error:', error);
      setError(error.message);
      addNotification(`Error: ${error.message}`, 'error');
      return null;
    } finally {
      setLoading(false);
    }
  }, [addNotification]);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      const analysisData = await fetchData(`analysis/${selectedSymbol}`, isMobile);
      if (analysisData) {
        setData(analysisData);
      }
      
      // Load validation data
      const validation = await fetchData(`validation/${selectedSymbol}`);
      if (validation) {
        setValidationData(validation);
      }
      
      // Load performance metrics
      const performance = await fetchData('performance');
      if (performance) {
        setPerformanceMetrics(performance);
      }
    };
    
    loadInitialData();
  }, [selectedSymbol, isMobile, fetchData]);

  // Memoized chart data processing
  const chartData = useMemo(() => {
    if (!data || !data.market_data) return [];
    
    return data.market_data.slice(0, isMobile ? 20 : 50).map(item => ({
      date: new Date(item.date).toLocaleDateString(),
      price: item.close,
      volume: item.volume,
      high: item.high,
      low: item.low,
      open: item.open
    }));
  }, [data, isMobile]);

  const validationChartData = useMemo(() => {
    if (!validationData || !validationData.summary) return [];
    
    return [
      { name: 'Passed', value: validationData.summary.passed_validations, color: '#10B981' },
      { name: 'Failed', value: validationData.summary.failed_validations, color: '#EF4444' }
    ];
  }, [validationData]);

  // Mobile-optimized components
  const MobileHeader = () => (
    <div className="mobile-header">
      <div className="header-top">
        <h1>Socrates AI</h1>
        <div className={`connection-status ${connectionStatus}`}>
          <span className="status-dot"></span>
          {connectionStatus}
        </div>
      </div>
      
      <div className="symbol-selector">
        <select 
          value={selectedSymbol} 
          onChange={(e) => setSelectedSymbol(e.target.value)}
          className="symbol-select"
        >
          <option value="AAPL">AAPL - Apple Inc.</option>
          <option value="GOOGL">GOOGL - Alphabet Inc.</option>
          <option value="MSFT">MSFT - Microsoft Corp.</option>
          <option value="TSLA">TSLA - Tesla Inc.</option>
          <option value="AMZN">AMZN - Amazon.com Inc.</option>
        </select>
      </div>
      
      {notifications.length > 0 && (
        <div className="notifications-mobile">
          {notifications.slice(0, 2).map(notification => (
            <div key={notification.id} className={`notification ${notification.type}`}>
              <span className="notification-message">{notification.message}</span>
              <span className="notification-time">{notification.timestamp}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const TabNavigation = () => (
    <div className="tab-navigation">
      {[
        { id: 'overview', label: '📊 Overview', icon: '📊' },
        { id: 'analysis', label: '📈 Analysis', icon: '📈' },
        { id: 'validation', label: '✅ Validation', icon: '✅' },
        { id: 'performance', label: '⚡ Performance', icon: '⚡' },
        { id: 'alerts', label: '🚨 Alerts', icon: '🚨' }
      ].map(tab => (
        <button
          key={tab.id}
          className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => setActiveTab(tab.id)}
        >
          {isMobile ? tab.icon : tab.label}
        </button>
      ))}
    </div>
  );

  const OverviewTab = () => (
    <div className="overview-tab">
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Current Price</h3>
          <div className="metric-value">
            ${data?.market_data?.[0]?.close?.toFixed(2) || 'N/A'}
          </div>
          <div className="metric-change positive">
            +2.45% Today
          </div>
        </div>
        
        <div className="metric-card">
          <h3>ECM Position</h3>
          <div className="metric-value">
            {data?.ecm_analysis?.cycle_position?.toFixed(1) || 'N/A'}°
          </div>
          <div className="metric-change neutral">
            8.6yr Cycle
          </div>
        </div>
        
        <div className="metric-card">
          <h3>Data Quality</h3>
          <div className="metric-value">
            {validationData?.summary?.accuracy_rate?.toFixed(1) || 'N/A'}%
          </div>
          <div className="metric-change positive">
            TradingView Validated
          </div>
        </div>
        
        <div className="metric-card">
          <h3>AI Confidence</h3>
          <div className="metric-value">
            {data?.ml_prediction?.confidence?.toFixed(0) || 'N/A'}%
          </div>
          <div className="metric-change positive">
            High Confidence
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>Price Chart (30 Days)</h3>
        <ResponsiveContainer width="100%" height={isMobile ? 200 : 300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: isMobile ? 10 : 12 }}
              interval={isMobile ? 4 : 2}
            />
            <YAxis tick={{ fontSize: isMobile ? 10 : 12 }} />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#3B82F6" 
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const AnalysisTab = () => (
    <div className="analysis-tab">
      <div className="analysis-section">
        <h3>Technical Analysis</h3>
        <div className="technical-indicators">
          <div className="indicator">
            <span>RSI (14):</span>
            <span className="indicator-value">65.2</span>
            <span className="indicator-signal neutral">Neutral</span>
          </div>
          <div className="indicator">
            <span>MACD:</span>
            <span className="indicator-value">1.23</span>
            <span className="indicator-signal positive">Bullish</span>
          </div>
          <div className="indicator">
            <span>SMA (20):</span>
            <span className="indicator-value">$210.45</span>
            <span className="indicator-signal positive">Above</span>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>Volume Analysis</h3>
        <ResponsiveContainer width="100%" height={isMobile ? 150 : 200}>
          <BarChart data={chartData.slice(0, isMobile ? 10 : 20)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: isMobile ? 8 : 10 }}
              interval={isMobile ? 2 : 1}
            />
            <YAxis tick={{ fontSize: isMobile ? 8 : 10 }} />
            <Tooltip />
            <Bar dataKey="volume" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="analysis-section">
        <h3>AI Prediction</h3>
        <div className="prediction-card">
          <div className="prediction-direction">
            <span className="direction-label">30-Day Forecast:</span>
            <span className="direction-value positive">↗ Bullish</span>
          </div>
          <div className="prediction-target">
            <span>Target Price: $225.00</span>
            <span className="confidence">Confidence: 78%</span>
          </div>
        </div>
      </div>
    </div>
  );

  const ValidationTab = () => (
    <div className="validation-tab">
      <div className="validation-summary">
        <h3>Data Quality Summary</h3>
        <div className="quality-metrics">
          <div className="quality-metric">
            <span>Accuracy Rate:</span>
            <span className="metric-value positive">
              {validationData?.summary?.accuracy_rate?.toFixed(1) || 'N/A'}%
            </span>
          </div>
          <div className="quality-metric">
            <span>Total Validations:</span>
            <span className="metric-value">
              {validationData?.summary?.total_validations || 'N/A'}
            </span>
          </div>
          <div className="quality-metric">
            <span>Avg Difference:</span>
            <span className="metric-value">
              {validationData?.summary?.avg_difference?.toFixed(2) || 'N/A'}%
            </span>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <h3>Validation Results</h3>
        <ResponsiveContainer width="100%" height={isMobile ? 150 : 200}>
          <PieChart>
            <Pie
              data={validationChartData}
              cx="50%"
              cy="50%"
              innerRadius={isMobile ? 30 : 40}
              outerRadius={isMobile ? 60 : 80}
              paddingAngle={5}
              dataKey="value"
            >
              {validationChartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      <div className="validation-details">
        <h4>Recent Validations</h4>
        <div className="validation-list">
          {validationData?.price_validation?.slice(0, isMobile ? 3 : 5).map((validation, index) => (
            <div key={index} className="validation-item">
              <span className="validation-type">{validation.data_type}</span>
              <span className="validation-difference">
                {validation.difference_pct?.toFixed(2)}% diff
              </span>
              <span className={`validation-status ${validation.is_valid ? 'valid' : 'invalid'}`}>
                {validation.is_valid ? '✅' : '❌'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const PerformanceTab = () => (
    <div className="performance-tab">
      <div className="performance-summary">
        <h3>System Performance</h3>
        <div className="performance-metrics">
          <div className="perf-metric">
            <span>Cache Hit Rate:</span>
            <span className="metric-value positive">
              {performanceMetrics?.cache_stats?.hit_rate?.toFixed(1) || 'N/A'}%
            </span>
          </div>
          <div className="perf-metric">
            <span>Avg Response:</span>
            <span className="metric-value">
              {performanceMetrics?.performance_summary?.operations?.get_optimized_analysis?.avg_duration?.toFixed(3) || 'N/A'}s
            </span>
          </div>
          <div className="perf-metric">
            <span>Memory Usage:</span>
            <span className="metric-value">
              {performanceMetrics?.system_info?.memory_percent?.toFixed(1) || 'N/A'}%
            </span>
          </div>
          <div className="perf-metric">
            <span>CPU Usage:</span>
            <span className="metric-value">
              {performanceMetrics?.system_info?.cpu_percent?.toFixed(1) || 'N/A'}%
            </span>
          </div>
        </div>
      </div>
      
      <div className="performance-chart">
        <h4>Operation Performance</h4>
        <div className="operation-list">
          {performanceMetrics?.performance_summary?.operations && 
           Object.entries(performanceMetrics.performance_summary.operations).map(([operation, stats]) => (
            <div key={operation} className="operation-item">
              <span className="operation-name">{operation}</span>
              <span className="operation-time">{stats.avg_duration?.toFixed(3)}s</span>
              <span className="operation-count">{stats.count} calls</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const AlertsTab = () => (
    <div className="alerts-tab">
      <div className="alerts-summary">
        <h3>Active Alerts</h3>
        <div className="alert-stats">
          <div className="alert-stat">
            <span>Active:</span>
            <span className="stat-value">3</span>
          </div>
          <div className="alert-stat">
            <span>Today:</span>
            <span className="stat-value">7</span>
          </div>
          <div className="alert-stat">
            <span>Critical:</span>
            <span className="stat-value critical">1</span>
          </div>
        </div>
      </div>
      
      <div className="alerts-list">
        <div className="alert-item critical">
          <div className="alert-icon">🚨</div>
          <div className="alert-content">
            <div className="alert-title">Price Alert: AAPL</div>
            <div className="alert-message">Price crossed $215 resistance</div>
            <div className="alert-time">2 minutes ago</div>
          </div>
        </div>
        
        <div className="alert-item warning">
          <div className="alert-icon">⚠️</div>
          <div className="alert-content">
            <div className="alert-title">Volume Spike: AAPL</div>
            <div className="alert-message">Volume 150% above average</div>
            <div className="alert-time">15 minutes ago</div>
          </div>
        </div>
        
        <div className="alert-item info">
          <div className="alert-icon">ℹ️</div>
          <div className="alert-content">
            <div className="alert-title">ECM Turning Point</div>
            <div className="alert-message">Approaching cycle inflection</div>
            <div className="alert-time">1 hour ago</div>
          </div>
        </div>
      </div>
    </div>
  );

  if (loading && !data) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading Socrates AI...</p>
      </div>
    );
  }

  return (
    <div className={`socrates-ai-app ${isMobile ? 'mobile' : 'desktop'}`}>
      {isMobile && <MobileHeader />}
      
      {!isMobile && (
        <header className="desktop-header">
          <div className="header-content">
            <h1>Socrates AI - Advanced Market Analysis</h1>
            <div className="header-controls">
              <select 
                value={selectedSymbol} 
                onChange={(e) => setSelectedSymbol(e.target.value)}
                className="symbol-select"
              >
                <option value="AAPL">AAPL - Apple Inc.</option>
                <option value="GOOGL">GOOGL - Alphabet Inc.</option>
                <option value="MSFT">MSFT - Microsoft Corp.</option>
                <option value="TSLA">TSLA - Tesla Inc.</option>
                <option value="AMZN">AMZN - Amazon.com Inc.</option>
              </select>
              <div className={`connection-status ${connectionStatus}`}>
                <span className="status-dot"></span>
                {connectionStatus}
              </div>
            </div>
          </div>
          
          {notifications.length > 0 && (
            <div className="notifications-desktop">
              {notifications.map(notification => (
                <div key={notification.id} className={`notification ${notification.type}`}>
                  <span className="notification-message">{notification.message}</span>
                  <span className="notification-time">{notification.timestamp}</span>
                </div>
              ))}
            </div>
          )}
        </header>
      )}
      
      <TabNavigation />
      
      <main className="main-content">
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}
        
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'analysis' && <AnalysisTab />}
        {activeTab === 'validation' && <ValidationTab />}
        {activeTab === 'performance' && <PerformanceTab />}
        {activeTab === 'alerts' && <AlertsTab />}
      </main>
      
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner small"></div>
        </div>
      )}
    </div>
  );
};

export default MobileSocratesAI;

