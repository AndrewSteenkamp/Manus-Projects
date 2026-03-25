#!/usr/bin/env python3
"""
Advanced Machine Learning Prediction Models for Socrates AI
Implements sophisticated ML algorithms for market forecasting and analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression, RFE
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import joblib
import warnings
from dataclasses import dataclass
import json
import ta  # Technical Analysis library
from scipy import stats
from scipy.signal import find_peaks
import xgboost as xgb
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PredictionResult:
    """Structure for prediction results"""
    symbol: str
    prediction_type: str
    predictions: List[float]
    confidence_intervals: Dict[str, List[float]]
    feature_importance: Dict[str, float]
    model_performance: Dict[str, float]
    prediction_dates: List[str]
    metadata: Dict[str, Any]

class AdvancedFeatureEngineer:
    """Advanced feature engineering for market data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def create_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create comprehensive technical analysis features"""
        try:
            # Ensure required columns exist
            required_cols = ['open_price', 'high_price', 'low_price', 'close_price', 'volume']
            for col in required_cols:
                if col not in df.columns:
                    logger.warning(f"Missing column {col}, using close_price as fallback")
                    df[col] = df['close_price']
            
            # Price-based features
            df['returns'] = df['close_price'].pct_change()
            df['log_returns'] = np.log(df['close_price'] / df['close_price'].shift(1))
            df['price_range'] = df['high_price'] - df['low_price']
            df['price_gap'] = df['open_price'] - df['close_price'].shift(1)
            
            # Moving averages
            for window in [5, 10, 20, 50, 100, 200]:
                df[f'ma_{window}'] = df['close_price'].rolling(window=window).mean()
                df[f'ma_{window}_ratio'] = df['close_price'] / df[f'ma_{window}']
                df[f'ma_{window}_slope'] = df[f'ma_{window}'].diff()
            
            # Exponential moving averages
            for span in [12, 26, 50]:
                df[f'ema_{span}'] = df['close_price'].ewm(span=span).mean()
                df[f'ema_{span}_ratio'] = df['close_price'] / df[f'ema_{span}']
            
            # Bollinger Bands
            for window in [20, 50]:
                rolling_mean = df['close_price'].rolling(window=window).mean()
                rolling_std = df['close_price'].rolling(window=window).std()
                df[f'bb_upper_{window}'] = rolling_mean + (rolling_std * 2)
                df[f'bb_lower_{window}'] = rolling_mean - (rolling_std * 2)
                df[f'bb_width_{window}'] = df[f'bb_upper_{window}'] - df[f'bb_lower_{window}']
                df[f'bb_position_{window}'] = (df['close_price'] - df[f'bb_lower_{window}']) / df[f'bb_width_{window}']
            
            # RSI
            for window in [14, 21, 30]:
                df[f'rsi_{window}'] = ta.momentum.RSIIndicator(df['close_price'], window=window).rsi()
            
            # MACD
            df['macd'] = ta.trend.MACD(df['close_price']).macd()
            df['macd_signal'] = ta.trend.MACD(df['close_price']).macd_signal()
            df['macd_histogram'] = ta.trend.MACD(df['close_price']).macd_diff()
            
            # Stochastic Oscillator
            df['stoch_k'] = ta.momentum.StochasticOscillator(
                df['high_price'], df['low_price'], df['close_price']
            ).stoch()
            df['stoch_d'] = ta.momentum.StochasticOscillator(
                df['high_price'], df['low_price'], df['close_price']
            ).stoch_signal()
            
            # Williams %R
            df['williams_r'] = ta.momentum.WilliamsRIndicator(
                df['high_price'], df['low_price'], df['close_price']
            ).williams_r()
            
            # Commodity Channel Index
            df['cci'] = ta.trend.CCIIndicator(
                df['high_price'], df['low_price'], df['close_price']
            ).cci()
            
            # Average True Range
            df['atr'] = ta.volatility.AverageTrueRange(
                df['high_price'], df['low_price'], df['close_price']
            ).average_true_range()
            
            # Volume features
            if 'volume' in df.columns and df['volume'].notna().any():
                df['volume_ma'] = df['volume'].rolling(window=20).mean()
                df['volume_ratio'] = df['volume'] / df['volume_ma']
                df['price_volume'] = df['close_price'] * df['volume']
                
                # On-Balance Volume
                df['obv'] = ta.volume.OnBalanceVolumeIndicator(
                    df['close_price'], df['volume']
                ).on_balance_volume()
                
                # Volume Weighted Average Price
                df['vwap'] = ta.volume.VolumeSMAIndicator(
                    df['close_price'], df['volume']
                ).volume_sma()
            
            # Volatility features
            for window in [10, 20, 30]:
                df[f'volatility_{window}'] = df['returns'].rolling(window=window).std()
                df[f'volatility_{window}_ratio'] = df[f'volatility_{window}'] / df[f'volatility_{window}'].rolling(window=50).mean()
            
            # Support and resistance levels
            df['support'] = df['low_price'].rolling(window=20).min()
            df['resistance'] = df['high_price'].rolling(window=20).max()
            df['support_distance'] = (df['close_price'] - df['support']) / df['close_price']
            df['resistance_distance'] = (df['resistance'] - df['close_price']) / df['close_price']
            
            # Momentum features
            for window in [5, 10, 20]:
                df[f'momentum_{window}'] = df['close_price'] / df['close_price'].shift(window)
                df[f'roc_{window}'] = df['close_price'].pct_change(periods=window)
            
            # Trend features
            df['trend_5'] = np.where(df['close_price'] > df['ma_5'], 1, 0)
            df['trend_20'] = np.where(df['close_price'] > df['ma_20'], 1, 0)
            df['trend_50'] = np.where(df['close_price'] > df['ma_50'], 1, 0)
            
            # Seasonal features
            df['day_of_week'] = pd.to_datetime(df.index).dayofweek
            df['month'] = pd.to_datetime(df.index).month
            df['quarter'] = pd.to_datetime(df.index).quarter
            
            # Lag features
            for lag in [1, 2, 3, 5, 10]:
                df[f'close_lag_{lag}'] = df['close_price'].shift(lag)
                df[f'returns_lag_{lag}'] = df['returns'].shift(lag)
                df[f'volume_lag_{lag}'] = df['volume'].shift(lag) if 'volume' in df.columns else 0
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating technical features: {e}")
            return df
    
    def create_ecm_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create ECM-specific features"""
        try:
            # ECM cycle parameters
            base_cycle_days = 3141  # π × 1000
            reference_date = pd.Timestamp('2007-02-27')
            
            # Calculate days since reference
            df['days_since_ecm_ref'] = (pd.to_datetime(df.index) - reference_date).dt.days
            
            # ECM cycle position
            df['ecm_cycle_position'] = (df['days_since_ecm_ref'] % base_cycle_days) / base_cycle_days
            df['ecm_cycle_sin'] = np.sin(2 * np.pi * df['ecm_cycle_position'])
            df['ecm_cycle_cos'] = np.cos(2 * np.pi * df['ecm_cycle_position'])
            
            # ECM phase classification
            df['ecm_phase'] = pd.cut(
                df['ecm_cycle_position'], 
                bins=[0, 0.25, 0.5, 0.75, 1.0],
                labels=['Early_Expansion', 'Late_Expansion', 'Early_Contraction', 'Late_Contraction']
            )
            
            # ECM phase encoding
            phase_encoding = {'Early_Expansion': 1, 'Late_Expansion': 2, 'Early_Contraction': 3, 'Late_Contraction': 4}
            df['ecm_phase_encoded'] = df['ecm_phase'].map(phase_encoding).fillna(0)
            
            # Distance to turning points
            turning_points = [0, 0.25, 0.5, 0.75, 1.0]
            for i, tp in enumerate(turning_points):
                df[f'distance_to_tp_{i}'] = np.abs(df['ecm_cycle_position'] - tp)
            
            df['min_distance_to_tp'] = df[[f'distance_to_tp_{i}' for i in range(len(turning_points))]].min(axis=1)
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating ECM features: {e}")
            return df
    
    def create_market_regime_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create market regime classification features"""
        try:
            # Volatility regimes
            vol_20 = df['returns'].rolling(window=20).std()
            vol_quantiles = vol_20.quantile([0.33, 0.67])
            
            df['vol_regime'] = pd.cut(
                vol_20,
                bins=[-np.inf, vol_quantiles.iloc[0], vol_quantiles.iloc[1], np.inf],
                labels=['Low_Vol', 'Medium_Vol', 'High_Vol']
            )
            
            # Trend regimes
            ma_20 = df['close_price'].rolling(window=20).mean()
            ma_50 = df['close_price'].rolling(window=50).mean()
            
            df['trend_regime'] = np.where(
                ma_20 > ma_50, 'Uptrend',
                np.where(ma_20 < ma_50, 'Downtrend', 'Sideways')
            )
            
            # Market stress indicator
            df['market_stress'] = (
                (df['rsi_14'] < 30).astype(int) +
                (df['rsi_14'] > 70).astype(int) +
                (vol_20 > vol_20.quantile(0.9)).astype(int)
            )
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating market regime features: {e}")
            return df
    
    def select_features(self, X: pd.DataFrame, y: pd.Series, method: str = 'rf_importance') -> List[str]:
        """Select most important features"""
        try:
            if method == 'rf_importance':
                rf = RandomForestRegressor(n_estimators=100, random_state=42)
                rf.fit(X.fillna(0), y)
                
                feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': rf.feature_importances_
                }).sort_values('importance', ascending=False)
                
                # Select top 50 features
                selected_features = feature_importance.head(50)['feature'].tolist()
                
            elif method == 'correlation':
                correlations = X.corrwith(y).abs().sort_values(ascending=False)
                selected_features = correlations.head(50).index.tolist()
                
            elif method == 'mutual_info':
                from sklearn.feature_selection import mutual_info_regression
                mi_scores = mutual_info_regression(X.fillna(0), y)
                mi_df = pd.DataFrame({
                    'feature': X.columns,
                    'mi_score': mi_scores
                }).sort_values('mi_score', ascending=False)
                
                selected_features = mi_df.head(50)['feature'].tolist()
                
            else:
                selected_features = X.columns.tolist()
            
            logger.info(f"Selected {len(selected_features)} features using {method}")
            return selected_features
            
        except Exception as e:
            logger.error(f"Error selecting features: {e}")
            return X.columns.tolist()

class AdvancedMLPredictor:
    """Advanced machine learning predictor with ensemble methods"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.feature_engineer = AdvancedFeatureEngineer()
        self.models = {}
        self.scalers = {}
        self.feature_selectors = {}
        self.model_performance = {}
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize various ML models"""
        self.models = {
            'random_forest': RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'xgboost': xgb.XGBRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                min_child_weight=1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1
            ),
            'neural_network': MLPRegressor(
                hidden_layer_sizes=(100, 50, 25),
                activation='relu',
                solver='adam',
                alpha=0.001,
                learning_rate='adaptive',
                max_iter=1000,
                random_state=42
            ),
            'svr': SVR(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                epsilon=0.1
            ),
            'elastic_net': ElasticNet(
                alpha=0.1,
                l1_ratio=0.5,
                random_state=42
            )
        }
        
        # Create ensemble model
        self.models['ensemble'] = VotingRegressor([
            ('rf', self.models['random_forest']),
            ('gb', self.models['gradient_boosting']),
            ('xgb', self.models['xgboost'])
        ])
    
    def get_market_data(self, symbol: str, days: int = 500) -> pd.DataFrame:
        """Get market data for training"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT date, open_price, high_price, low_price, close_price, volume
                FROM market_data 
                WHERE symbol = ? 
                ORDER BY date ASC 
                LIMIT ?
            '''
            
            df = pd.read_sql_query(query, conn, params=(symbol, days))
            conn.close()
            
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                df = df.sort_index()
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return pd.DataFrame()
    
    def prepare_features_and_target(self, df: pd.DataFrame, target_days: int = 5) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target variable"""
        try:
            # Create comprehensive features
            df = self.feature_engineer.create_technical_features(df)
            df = self.feature_engineer.create_ecm_features(df)
            df = self.feature_engineer.create_market_regime_features(df)
            
            # Create target variable (future returns)
            df['target'] = df['close_price'].shift(-target_days) / df['close_price'] - 1
            
            # Remove rows with NaN target
            df = df.dropna(subset=['target'])
            
            # Separate features and target
            feature_cols = [col for col in df.columns if col not in ['target', 'close_price', 'open_price', 'high_price', 'low_price', 'volume']]
            
            # Handle categorical features
            categorical_cols = df[feature_cols].select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols:
                df[col] = pd.Categorical(df[col]).codes
            
            X = df[feature_cols].fillna(0)
            y = df['target']
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error preparing features and target: {e}")
            return pd.DataFrame(), pd.Series()
    
    def train_model(self, symbol: str, model_name: str = 'ensemble', target_days: int = 5) -> Dict[str, Any]:
        """Train a specific model"""
        try:
            logger.info(f"Training {model_name} model for {symbol}")
            
            # Get data
            df = self.get_market_data(symbol, days=1000)
            if df.empty:
                return {'error': f'No data available for {symbol}'}
            
            # Prepare features and target
            X, y = self.prepare_features_and_target(df, target_days)
            if X.empty:
                return {'error': 'Failed to prepare features'}
            
            # Feature selection
            selected_features = self.feature_engineer.select_features(X, y, method='rf_importance')
            X_selected = X[selected_features]
            
            # Split data (time series split)
            split_idx = int(len(X_selected) * 0.8)
            X_train, X_test = X_selected.iloc[:split_idx], X_selected.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = self.models[model_name]
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred_train = model.predict(X_train_scaled)
            y_pred_test = model.predict(X_test_scaled)
            
            # Calculate performance metrics
            train_mse = mean_squared_error(y_train, y_pred_train)
            test_mse = mean_squared_error(y_test, y_pred_test)
            train_mae = mean_absolute_error(y_train, y_pred_train)
            test_mae = mean_absolute_error(y_test, y_pred_test)
            train_r2 = r2_score(y_train, y_pred_train)
            test_r2 = r2_score(y_test, y_pred_test)
            
            # Feature importance (for tree-based models)
            feature_importance = {}
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(zip(selected_features, model.feature_importances_))
            elif hasattr(model, 'coef_'):
                feature_importance = dict(zip(selected_features, np.abs(model.coef_)))
            
            # Store model and scaler
            model_key = f"{symbol}_{model_name}_{target_days}d"
            self.models[model_key] = model
            self.scalers[model_key] = scaler
            self.feature_selectors[model_key] = selected_features
            
            # Store performance
            performance = {
                'train_mse': train_mse,
                'test_mse': test_mse,
                'train_mae': train_mae,
                'test_mae': test_mae,
                'train_r2': train_r2,
                'test_r2': test_r2,
                'feature_count': len(selected_features),
                'training_samples': len(X_train)
            }
            
            self.model_performance[model_key] = performance
            
            logger.info(f"Model {model_name} trained successfully for {symbol}")
            logger.info(f"Test R²: {test_r2:.4f}, Test MAE: {test_mae:.4f}")
            
            return {
                'success': True,
                'model_key': model_key,
                'performance': performance,
                'feature_importance': feature_importance,
                'selected_features': selected_features
            }
            
        except Exception as e:
            logger.error(f"Error training model {model_name} for {symbol}: {e}")
            return {'error': str(e)}
    
    def predict_future_prices(self, symbol: str, horizon_days: int = 30, model_name: str = 'ensemble') -> PredictionResult:
        """Predict future prices using trained model"""
        try:
            model_key = f"{symbol}_{model_name}_5d"
            
            # Check if model exists
            if model_key not in self.models:
                # Train model if it doesn't exist
                train_result = self.train_model(symbol, model_name)
                if 'error' in train_result:
                    raise Exception(f"Failed to train model: {train_result['error']}")
            
            # Get recent data
            df = self.get_market_data(symbol, days=200)
            if df.empty:
                raise Exception(f"No data available for {symbol}")
            
            # Prepare features
            df = self.feature_engineer.create_technical_features(df)
            df = self.feature_engineer.create_ecm_features(df)
            df = self.feature_engineer.create_market_regime_features(df)
            
            # Get selected features
            selected_features = self.feature_selectors[model_key]
            
            # Handle categorical features
            categorical_cols = df[selected_features].select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols:
                if col in df.columns:
                    df[col] = pd.Categorical(df[col]).codes
            
            X = df[selected_features].fillna(0)
            
            # Get model and scaler
            model = self.models[model_key]
            scaler = self.scalers[model_key]
            
            # Make predictions for multiple horizons
            predictions = []
            confidence_intervals = {'lower': [], 'upper': []}
            prediction_dates = []
            
            current_price = df['close_price'].iloc[-1]
            last_date = df.index[-1]
            
            for i in range(horizon_days):
                # Use the most recent features
                X_pred = X.iloc[-1:].values
                X_pred_scaled = scaler.transform(X_pred)
                
                # Make prediction (returns)
                pred_return = model.predict(X_pred_scaled)[0]
                
                # Convert to price
                pred_price = current_price * (1 + pred_return)
                predictions.append(pred_price)
                
                # Calculate confidence intervals (simplified)
                # In practice, you'd use prediction intervals from the model
                volatility = df['returns'].rolling(window=20).std().iloc[-1]
                confidence_factor = 1.96 * volatility * np.sqrt(i + 1)  # Assuming normal distribution
                
                lower_bound = pred_price * (1 - confidence_factor)
                upper_bound = pred_price * (1 + confidence_factor)
                
                confidence_intervals['lower'].append(lower_bound)
                confidence_intervals['upper'].append(upper_bound)
                
                # Update for next prediction
                current_price = pred_price
                prediction_dates.append((last_date + timedelta(days=i+1)).strftime('%Y-%m-%d'))
            
            # Get feature importance
            feature_importance = {}
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(zip(selected_features, model.feature_importances_))
            
            # Get model performance
            performance = self.model_performance.get(model_key, {})
            
            return PredictionResult(
                symbol=symbol,
                prediction_type=f"{horizon_days}d_price_forecast",
                predictions=predictions,
                confidence_intervals=confidence_intervals,
                feature_importance=feature_importance,
                model_performance=performance,
                prediction_dates=prediction_dates,
                metadata={
                    'model_name': model_name,
                    'horizon_days': horizon_days,
                    'base_price': df['close_price'].iloc[-1],
                    'prediction_timestamp': datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error predicting future prices for {symbol}: {e}")
            return PredictionResult(
                symbol=symbol,
                prediction_type="error",
                predictions=[],
                confidence_intervals={'lower': [], 'upper': []},
                feature_importance={},
                model_performance={},
                prediction_dates=[],
                metadata={'error': str(e)}
            )
    
    def predict_market_regime(self, symbol: str) -> Dict[str, Any]:
        """Predict market regime using clustering"""
        try:
            # Get data
            df = self.get_market_data(symbol, days=500)
            if df.empty:
                return {'error': f'No data available for {symbol}'}
            
            # Create features for regime classification
            df = self.feature_engineer.create_technical_features(df)
            
            # Select features for clustering
            regime_features = [
                'returns', 'volatility_20', 'rsi_14', 'macd', 'bb_position_20',
                'volume_ratio', 'momentum_10', 'atr'
            ]
            
            # Filter available features
            available_features = [f for f in regime_features if f in df.columns]
            X = df[available_features].dropna()
            
            if X.empty:
                return {'error': 'No valid features for regime classification'}
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Apply K-means clustering
            kmeans = KMeans(n_clusters=3, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Analyze clusters
            df_clustered = X.copy()
            df_clustered['cluster'] = clusters
            df_clustered['returns'] = df.loc[X.index, 'returns']
            
            cluster_analysis = {}
            for cluster in range(3):
                cluster_data = df_clustered[df_clustered['cluster'] == cluster]
                cluster_analysis[f'regime_{cluster}'] = {
                    'avg_return': cluster_data['returns'].mean(),
                    'volatility': cluster_data['returns'].std(),
                    'sample_count': len(cluster_data),
                    'characteristics': {
                        'rsi_avg': cluster_data['rsi_14'].mean() if 'rsi_14' in cluster_data.columns else None,
                        'volatility_avg': cluster_data['volatility_20'].mean() if 'volatility_20' in cluster_data.columns else None
                    }
                }
            
            # Predict current regime
            current_features = X.iloc[-1:].values
            current_features_scaled = scaler.transform(current_features)
            current_regime = kmeans.predict(current_features_scaled)[0]
            
            return {
                'success': True,
                'current_regime': f'regime_{current_regime}',
                'regime_analysis': cluster_analysis,
                'regime_probabilities': {
                    f'regime_{i}': float(np.exp(-np.linalg.norm(current_features_scaled - kmeans.cluster_centers_[i])))
                    for i in range(3)
                }
            }
            
        except Exception as e:
            logger.error(f"Error predicting market regime for {symbol}: {e}")
            return {'error': str(e)}
    
    def get_model_explanation(self, symbol: str, model_name: str = 'ensemble') -> Dict[str, Any]:
        """Get model explanation and interpretability"""
        try:
            model_key = f"{symbol}_{model_name}_5d"
            
            if model_key not in self.models:
                return {'error': 'Model not trained'}
            
            model = self.models[model_key]
            selected_features = self.feature_selectors[model_key]
            performance = self.model_performance[model_key]
            
            # Feature importance
            feature_importance = {}
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(zip(selected_features, model.feature_importances_))
            elif hasattr(model, 'coef_'):
                feature_importance = dict(zip(selected_features, np.abs(model.coef_)))
            
            # Sort by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'success': True,
                'model_type': type(model).__name__,
                'performance_metrics': performance,
                'top_features': sorted_features[:20],
                'feature_categories': self._categorize_features(selected_features),
                'model_complexity': {
                    'feature_count': len(selected_features),
                    'training_samples': performance.get('training_samples', 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting model explanation for {symbol}: {e}")
            return {'error': str(e)}
    
    def _categorize_features(self, features: List[str]) -> Dict[str, List[str]]:
        """Categorize features by type"""
        categories = {
            'price_features': [],
            'technical_indicators': [],
            'volume_features': [],
            'volatility_features': [],
            'momentum_features': [],
            'ecm_features': [],
            'seasonal_features': [],
            'lag_features': []
        }
        
        for feature in features:
            if any(x in feature for x in ['ma_', 'ema_', 'close', 'open', 'high', 'low']):
                categories['price_features'].append(feature)
            elif any(x in feature for x in ['rsi', 'macd', 'stoch', 'williams', 'cci', 'bb_']):
                categories['technical_indicators'].append(feature)
            elif 'volume' in feature or 'obv' in feature or 'vwap' in feature:
                categories['volume_features'].append(feature)
            elif 'volatility' in feature or 'atr' in feature:
                categories['volatility_features'].append(feature)
            elif any(x in feature for x in ['momentum', 'roc']):
                categories['momentum_features'].append(feature)
            elif 'ecm' in feature:
                categories['ecm_features'].append(feature)
            elif any(x in feature for x in ['day_of_week', 'month', 'quarter']):
                categories['seasonal_features'].append(feature)
            elif 'lag' in feature:
                categories['lag_features'].append(feature)
        
        return {k: v for k, v in categories.items() if v}
    
    def save_models(self, filepath: str):
        """Save trained models to disk"""
        try:
            model_data = {
                'models': self.models,
                'scalers': self.scalers,
                'feature_selectors': self.feature_selectors,
                'model_performance': self.model_performance
            }
            
            joblib.dump(model_data, filepath)
            logger.info(f"Models saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self, filepath: str):
        """Load trained models from disk"""
        try:
            model_data = joblib.load(filepath)
            
            self.models.update(model_data['models'])
            self.scalers = model_data['scalers']
            self.feature_selectors = model_data['feature_selectors']
            self.model_performance = model_data['model_performance']
            
            logger.info(f"Models loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")

def main():
    """Test the advanced ML prediction system"""
    print("Advanced ML Prediction Models for Socrates AI")
    print("=" * 50)
    
    # Initialize predictor
    predictor = AdvancedMLPredictor()
    
    # Test symbol
    symbol = 'AAPL'
    
    print(f"1. Training models for {symbol}...")
    
    # Train different models
    models_to_test = ['random_forest', 'gradient_boosting', 'xgboost', 'ensemble']
    
    for model_name in models_to_test:
        print(f"   Training {model_name}...")
        result = predictor.train_model(symbol, model_name)
        
        if 'error' not in result:
            performance = result['performance']
            print(f"   ✓ {model_name}: R² = {performance['test_r2']:.4f}, MAE = {performance['test_mae']:.4f}")
        else:
            print(f"   ✗ {model_name}: {result['error']}")
    
    print(f"\n2. Making predictions for {symbol}...")
    
    # Make price predictions
    prediction_result = predictor.predict_future_prices(symbol, horizon_days=30)
    
    if prediction_result.predictions:
        print(f"   ✓ Generated {len(prediction_result.predictions)} price predictions")
        print(f"   Current price: ${prediction_result.metadata['base_price']:.2f}")
        print(f"   30-day prediction: ${prediction_result.predictions[-1]:.2f}")
        print(f"   Model performance: R² = {prediction_result.model_performance.get('test_r2', 0):.4f}")
    else:
        print(f"   ✗ Prediction failed: {prediction_result.metadata.get('error', 'Unknown error')}")
    
    print(f"\n3. Analyzing market regime for {symbol}...")
    
    # Predict market regime
    regime_result = predictor.predict_market_regime(symbol)
    
    if 'error' not in regime_result:
        print(f"   ✓ Current regime: {regime_result['current_regime']}")
        print("   Regime characteristics:")
        for regime, analysis in regime_result['regime_analysis'].items():
            print(f"     {regime}: avg_return = {analysis['avg_return']:.4f}, volatility = {analysis['volatility']:.4f}")
    else:
        print(f"   ✗ Regime analysis failed: {regime_result['error']}")
    
    print(f"\n4. Getting model explanation for {symbol}...")
    
    # Get model explanation
    explanation = predictor.get_model_explanation(symbol)
    
    if 'error' not in explanation:
        print(f"   ✓ Model type: {explanation['model_type']}")
        print(f"   Features used: {explanation['model_complexity']['feature_count']}")
        print("   Top 5 features:")
        for feature, importance in explanation['top_features'][:5]:
            print(f"     {feature}: {importance:.4f}")
    else:
        print(f"   ✗ Explanation failed: {explanation['error']}")
    
    print("\nAdvanced ML prediction system test completed!")

if __name__ == "__main__":
    main()

