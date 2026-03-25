import React, { useState, useEffect, useRef, useCallback } from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, Scatter, ScatterChart, Heatmap } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  BarChart3, 
  PieChart as PieChartIcon, 
  Globe, 
  Zap, 
  Settings,
  Play,
  Pause,
  RefreshCw,
  Download,
  Maximize2,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Percent
} from 'lucide-react';
import io from 'socket.io-client';

// Enhanced Socrates AI Dashboard with Advanced Visualizations
const EnhancedSocratesAIDashboard = () => {
  // State management
  const [marketData, setMarketData] = useState({});
  const [analysisResults, setAnalysisResults] = useState({});
  const [globalAnalysis, setGlobalAnalysis] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [selectedTimeframe, setSelectedTimeframe] = useState('1D');
  const [isRealTimeEnabled, setIsRealTimeEnabled] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [notifications, setNotifications] = useState([]);
  const [chartType, setChartType] = useState('candlestick');
  const [showTechnicalIndicators, setShowTechnicalIndicators] = useState(true);
  const [ecmData, setEcmData] = useState(null);
  const [correlationData, setCorrelationData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // WebSocket connection
  const socketRef = useRef(null);
  const [subscriptions, setSubscriptions] = useState(new Set());
  
  // Available symbols and timeframes
  const symbols = ['AAPL', 'GOOGL', 'MSFT', 'SPY', 'GLD', 'EURUSD=X', 'GC=F', 'CL=F'];
  const timeframes = ['1D', '5D', '1M', '3M', '6M', '1Y', '2Y'];
  
  // Color schemes for different chart types
  const colors = {
    primary: '#3b82f6',
    secondary: '#ef4444',
    success: '#10b981',
    warning: '#f59e0b',
    info: '#06b6d4',
    purple: '#8b5cf6'
  };
  
  // Initialize WebSocket connection
  useEffect(() => {
    if (isRealTimeEnabled) {
      initializeWebSocket();
    } else {
      disconnectWebSocket();
    }
    
    return () => {
      disconnectWebSocket();
    };
  }, [isRealTimeEnabled]);
  
  const initializeWebSocket = useCallback(() => {
    try {
      socketRef.current = io('http://localhost:5000', {
        transports: ['websocket', 'polling']
      });
      
      socketRef.current.on('connect', () => {
        setConnectionStatus('connected');
        addNotification('Connected to Socrates AI streaming service', 'success');
        
        // Subscribe to default streams
        subscribeToStream('system_status');
        subscribeToStream('global_analysis');
        if (selectedSymbol) {
          subscribeToStream('market_data', selectedSymbol);
          subscribeToStream('analysis_results', selectedSymbol);
        }
      });
      
      socketRef.current.on('disconnect', () => {
        setConnectionStatus('disconnected');
        addNotification('Disconnected from streaming service', 'warning');
      });
      
      socketRef.current.on('stream_data', (data) => {
        handleStreamData(data);
      });
      
      socketRef.current.on('error', (error) => {
        console.error('WebSocket error:', error);
        addNotification('WebSocket connection error', 'error');
      });
      
    } catch (error) {
      console.error('Failed to initialize WebSocket:', error);
      addNotification('Failed to connect to streaming service', 'error');
    }
  }, [selectedSymbol]);
  
  const disconnectWebSocket = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
      setConnectionStatus('disconnected');
    }
  }, []);
  
  const subscribeToStream = useCallback((streamType, symbol = null) => {
    if (socketRef.current && socketRef.current.connected) {
      const subscriptionKey = symbol ? `${streamType}_${symbol}` : streamType;
      
      if (!subscriptions.has(subscriptionKey)) {
        socketRef.current.emit('subscribe', {
          stream_type: streamType,
          symbol: symbol
        });
        
        setSubscriptions(prev => new Set([...prev, subscriptionKey]));
      }
    }
  }, [subscriptions]);
  
  const handleStreamData = useCallback((data) => {
    const { stream_type, symbol, data: streamData } = data;
    
    switch (stream_type) {
      case 'market_data':
        setMarketData(prev => ({
          ...prev,
          [symbol]: streamData
        }));
        break;
        
      case 'analysis_results':
        setAnalysisResults(prev => ({
          ...prev,
          [symbol]: streamData
        }));
        break;
        
      case 'global_analysis':
        setGlobalAnalysis(streamData);
        break;
        
      case 'system_status':
        setSystemStatus(streamData);
        break;
        
      case 'ecm_updates':
        setEcmData(streamData);
        break;
        
      case 'alerts':
        addNotification(streamData.message, streamData.severity);
        break;
        
      default:
        console.log('Unknown stream type:', stream_type);
    }
  }, []);
  
  const addNotification = useCallback((message, type = 'info') => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date().toISOString()
    };
    
    setNotifications(prev => [notification, ...prev.slice(0, 9)]); // Keep last 10
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  }, []);
  
  // API calls for non-real-time data
  const fetchMarketAnalysis = useCallback(async (symbol) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/socrates/analyze/market/${symbol}`);
      const result = await response.json();
      
      if (result.success) {
        setAnalysisResults(prev => ({
          ...prev,
          [symbol]: result.data
        }));
      } else {
        addNotification(`Failed to fetch analysis for ${symbol}`, 'error');
      }
    } catch (error) {
      console.error('Error fetching market analysis:', error);
      addNotification('Error fetching market analysis', 'error');
    } finally {
      setLoading(false);
    }
  }, []);
  
  const fetchGlobalAnalysis = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5000/api/socrates/analyze/global');
      const result = await response.json();
      
      if (result.success) {
        setGlobalAnalysis(result.data);
      }
    } catch (error) {
      console.error('Error fetching global analysis:', error);
    }
  }, []);
  
  const fetchECMData = useCallback(async () => {
    try {
      // This would call a specific ECM endpoint
      const mockECMData = {
        cycle_position: 0.73,
        phase: 'Late Expansion',
        confidence: 0.85,
        days_into_cycle: 2287,
        next_turning_point: '2024-12-15'
      };
      setEcmData(mockECMData);
    } catch (error) {
      console.error('Error fetching ECM data:', error);
    }
  }, []);
  
  const fetchCorrelationData = useCallback(async () => {
    try {
      // Mock correlation data
      const mockCorrelationData = [
        { symbol1: 'AAPL', symbol2: 'GOOGL', correlation: 0.72 },
        { symbol1: 'AAPL', symbol2: 'SPY', correlation: 0.85 },
        { symbol1: 'GOOGL', symbol2: 'SPY', correlation: 0.78 },
        { symbol1: 'SPY', symbol2: 'GLD', correlation: -0.23 },
        { symbol1: 'GLD', symbol2: 'EURUSD=X', correlation: 0.45 }
      ];
      setCorrelationData(mockCorrelationData);
    } catch (error) {
      console.error('Error fetching correlation data:', error);
    }
  }, []);
  
  const fetchForecastData = useCallback(async (symbol) => {
    try {
      const response = await fetch(`http://localhost:5000/api/socrates/forecast/${symbol}?horizon=30`);
      const result = await response.json();
      
      if (result.success) {
        setForecastData(prev => ({
          ...prev,
          [symbol]: result.data
        }));
      }
    } catch (error) {
      console.error('Error fetching forecast data:', error);
    }
  }, []);
  
  // Effect for symbol changes
  useEffect(() => {
    if (selectedSymbol) {
      fetchMarketAnalysis(selectedSymbol);
      fetchForecastData(selectedSymbol);
      
      if (isRealTimeEnabled && socketRef.current) {
        subscribeToStream('market_data', selectedSymbol);
        subscribeToStream('analysis_results', selectedSymbol);
      }
    }
  }, [selectedSymbol, fetchMarketAnalysis, fetchForecastData, isRealTimeEnabled, subscribeToStream]);
  
  // Initial data fetch
  useEffect(() => {
    fetchGlobalAnalysis();
    fetchECMData();
    fetchCorrelationData();
  }, [fetchGlobalAnalysis, fetchECMData, fetchCorrelationData]);
  
  // Generate mock chart data for demonstration
  const generateMockPriceData = (symbol) => {
    const data = [];
    const basePrice = 150;
    let currentPrice = basePrice;
    
    for (let i = 0; i < 30; i++) {
      const change = (Math.random() - 0.5) * 10;
      currentPrice += change;
      
      data.push({
        date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        price: Math.max(currentPrice, 50),
        volume: Math.floor(Math.random() * 1000000) + 500000,
        rsi: Math.random() * 100,
        ma20: currentPrice * (0.98 + Math.random() * 0.04),
        ma50: currentPrice * (0.95 + Math.random() * 0.1)
      });
    }
    
    return data;
  };
  
  const priceData = generateMockPriceData(selectedSymbol);
  
  // Component for connection status
  const ConnectionStatus = () => (
    <div className="flex items-center space-x-2">
      <div className={`w-3 h-3 rounded-full ${
        connectionStatus === 'connected' ? 'bg-green-500' : 
        connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'
      }`} />
      <span className="text-sm font-medium">
        {connectionStatus === 'connected' ? 'Live' : 
         connectionStatus === 'connecting' ? 'Connecting' : 'Offline'}
      </span>
    </div>
  );
  
  // Component for notifications
  const NotificationPanel = () => (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {notifications.map((notification) => (
        <Alert key={notification.id} className={`
          ${notification.type === 'success' ? 'border-green-500 bg-green-50' : ''}
          ${notification.type === 'warning' ? 'border-yellow-500 bg-yellow-50' : ''}
          ${notification.type === 'error' ? 'border-red-500 bg-red-50' : ''}
          ${notification.type === 'info' ? 'border-blue-500 bg-blue-50' : ''}
        `}>
          <AlertDescription className="text-sm">
            {notification.message}
          </AlertDescription>
        </Alert>
      ))}
    </div>
  );
  
  // Advanced Price Chart Component
  const AdvancedPriceChart = () => (
    <Card className="col-span-2">
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5" />
              <span>{selectedSymbol} Price Analysis</span>
            </CardTitle>
            <CardDescription>
              Advanced price chart with technical indicators
            </CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Select value={chartType} onValueChange={setChartType}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="line">Line</SelectItem>
                <SelectItem value="candlestick">Candlestick</SelectItem>
                <SelectItem value="area">Area</SelectItem>
              </SelectContent>
            </Select>
            <Switch
              checked={showTechnicalIndicators}
              onCheckedChange={setShowTechnicalIndicators}
            />
            <span className="text-sm">Indicators</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            {chartType === 'area' ? (
              <AreaChart data={priceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="price" 
                  stroke={colors.primary} 
                  fill={colors.primary}
                  fillOpacity={0.3}
                />
                {showTechnicalIndicators && (
                  <>
                    <Line type="monotone" dataKey="ma20" stroke={colors.warning} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="ma50" stroke={colors.secondary} strokeWidth={2} dot={false} />
                  </>
                )}
              </AreaChart>
            ) : (
              <LineChart data={priceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke={colors.primary} 
                  strokeWidth={3}
                  dot={{ fill: colors.primary, strokeWidth: 2, r: 4 }}
                />
                {showTechnicalIndicators && (
                  <>
                    <Line type="monotone" dataKey="ma20" stroke={colors.warning} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="ma50" stroke={colors.secondary} strokeWidth={2} dot={false} />
                  </>
                )}
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
  
  // ECM Cycle Visualization
  const ECMCycleChart = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Activity className="w-5 h-5" />
          <span>ECM Cycle Analysis</span>
        </CardTitle>
        <CardDescription>
          Economic Confidence Model cycle position
        </CardDescription>
      </CardHeader>
      <CardContent>
        {ecmData && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Cycle Position</span>
              <Badge variant="outline">{(ecmData.cycle_position * 100).toFixed(1)}%</Badge>
            </div>
            <Progress value={ecmData.cycle_position * 100} className="w-full" />
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Phase:</span>
                <div className="font-medium">{ecmData.phase}</div>
              </div>
              <div>
                <span className="text-gray-600">Confidence:</span>
                <div className="font-medium">{(ecmData.confidence * 100).toFixed(1)}%</div>
              </div>
              <div>
                <span className="text-gray-600">Days into Cycle:</span>
                <div className="font-medium">{ecmData.days_into_cycle}</div>
              </div>
              <div>
                <span className="text-gray-600">Next Turn:</span>
                <div className="font-medium">{ecmData.next_turning_point}</div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
  
  // Market Correlation Heatmap
  const CorrelationHeatmap = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Globe className="w-5 h-5" />
          <span>Market Correlations</span>
        </CardTitle>
        <CardDescription>
          Cross-market correlation analysis
        </CardDescription>
      </CardHeader>
      <CardContent>
        {correlationData && (
          <div className="space-y-2">
            {correlationData.map((item, index) => (
              <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                <span className="text-sm font-medium">
                  {item.symbol1} × {item.symbol2}
                </span>
                <div className="flex items-center space-x-2">
                  <div className={`w-4 h-4 rounded ${
                    item.correlation > 0.5 ? 'bg-green-500' :
                    item.correlation < -0.5 ? 'bg-red-500' : 'bg-yellow-500'
                  }`} />
                  <span className="text-sm">{item.correlation.toFixed(2)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
  
  // Volume Analysis Chart
  const VolumeChart = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <BarChart3 className="w-5 h-5" />
          <span>Volume Analysis</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={priceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="volume" fill={colors.info} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
  
  // RSI Indicator Chart
  const RSIChart = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <TrendingUp className="w-5 h-5" />
          <span>RSI Indicator</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={priceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="rsi" 
                stroke={colors.purple} 
                strokeWidth={2}
              />
              {/* Overbought/Oversold lines */}
              <Line 
                type="monotone" 
                dataKey={() => 70} 
                stroke={colors.secondary} 
                strokeDasharray="5 5"
                dot={false}
              />
              <Line 
                type="monotone" 
                dataKey={() => 30} 
                stroke={colors.success} 
                strokeDasharray="5 5"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
  
  // Global Market Overview
  const GlobalMarketOverview = () => (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Globe className="w-5 h-5" />
          <span>Global Market Overview</span>
        </CardTitle>
        <CardDescription>
          Cross-market analysis and capital flows
        </CardDescription>
      </CardHeader>
      <CardContent>
        {globalAnalysis && (
          <div className="grid grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {(globalAnalysis.global_confidence * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600">Global Confidence</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {globalAnalysis.markets_analyzed || 0}
              </div>
              <div className="text-sm text-gray-600">Markets Analyzed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {globalAnalysis.capital_flow_analysis?.flow_strength || 'N/A'}
              </div>
              <div className="text-sm text-gray-600">Flow Strength</div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
  
  // System Status Panel
  const SystemStatusPanel = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Activity className="w-5 h-5" />
          <span>System Status</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm">Connection</span>
            <ConnectionStatus />
          </div>
          
          {systemStatus && (
            <>
              <div className="flex justify-between items-center">
                <span className="text-sm">Active Connections</span>
                <Badge variant="outline">{systemStatus.active_connections}</Badge>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm">Data Status</span>
                <Badge variant={systemStatus.status === 'operational' ? 'default' : 'destructive'}>
                  {systemStatus.status}
                </Badge>
              </div>
              
              {systemStatus.data_stats && (
                <div className="text-xs text-gray-600 space-y-1">
                  <div>Market Data: {systemStatus.data_stats.market_data_count}</div>
                  <div>Forex Data: {systemStatus.data_stats.forex_data_count}</div>
                  <div>Commodities: {systemStatus.data_stats.commodities_data_count}</div>
                </div>
              )}
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
  
  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <NotificationPanel />
      
      {/* Header */}
      <div className="mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Enhanced Socrates AI Dashboard
            </h1>
            <p className="text-gray-600 mt-1">
              Advanced market analysis with real-time visualizations
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <Select value={selectedSymbol} onValueChange={setSelectedSymbol}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {symbols.map(symbol => (
                  <SelectItem key={symbol} value={symbol}>{symbol}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Select value={selectedTimeframe} onValueChange={setSelectedTimeframe}>
              <SelectTrigger className="w-20">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {timeframes.map(tf => (
                  <SelectItem key={tf} value={tf}>{tf}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <div className="flex items-center space-x-2">
              <Switch
                checked={isRealTimeEnabled}
                onCheckedChange={setIsRealTimeEnabled}
              />
              <span className="text-sm">Real-time</span>
            </div>
            
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => {
                fetchMarketAnalysis(selectedSymbol);
                fetchGlobalAnalysis();
              }}
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </Button>
          </div>
        </div>
      </div>
      
      {/* Main Dashboard */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
          <TabsTrigger value="cycles">ECM Cycles</TabsTrigger>
          <TabsTrigger value="correlations">Correlations</TabsTrigger>
          <TabsTrigger value="forecasts">Forecasts</TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <GlobalMarketOverview />
            <SystemStatusPanel />
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <AdvancedPriceChart />
            <ECMCycleChart />
          </div>
        </TabsContent>
        
        <TabsContent value="analysis" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AdvancedPriceChart />
            <div className="space-y-6">
              <VolumeChart />
              <RSIChart />
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="cycles" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ECMCycleChart />
            <Card>
              <CardHeader>
                <CardTitle>Cycle Analysis Details</CardTitle>
              </CardHeader>
              <CardContent>
                {ecmData && (
                  <div className="space-y-4">
                    <div className="text-sm">
                      <strong>Current Phase:</strong> {ecmData.phase}
                    </div>
                    <div className="text-sm">
                      <strong>Cycle Progress:</strong> {(ecmData.cycle_position * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm">
                      <strong>Confidence Level:</strong> {(ecmData.confidence * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm">
                      <strong>Next Turning Point:</strong> {ecmData.next_turning_point}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        
        <TabsContent value="correlations" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CorrelationHeatmap />
            <Card>
              <CardHeader>
                <CardTitle>Correlation Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-sm">
                  <div className="p-3 bg-green-50 rounded-lg">
                    <strong>Strong Positive:</strong> High correlation indicates assets move together
                  </div>
                  <div className="p-3 bg-red-50 rounded-lg">
                    <strong>Strong Negative:</strong> Assets move in opposite directions
                  </div>
                  <div className="p-3 bg-yellow-50 rounded-lg">
                    <strong>Weak Correlation:</strong> Assets move independently
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        
        <TabsContent value="forecasts" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5" />
                <span>{selectedSymbol} Price Forecast</span>
              </CardTitle>
              <CardDescription>
                30-day price prediction with confidence intervals
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={priceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="price" 
                      stroke={colors.primary} 
                      strokeWidth={3}
                      name="Historical Price"
                    />
                    {/* Forecast would be added here with actual forecast data */}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default EnhancedSocratesAIDashboard;

