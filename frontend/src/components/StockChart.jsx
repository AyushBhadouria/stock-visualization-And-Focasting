import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

const StockChart = ({ data, indicators = {}, height = 400 }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();

  useEffect(() => {
    if (!chartContainerRef.current || !data || data.length === 0) return;

    // Create chart
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: height,
      layout: {
        backgroundColor: '#ffffff',
        textColor: '#333',
      },
      grid: {
        vertLines: {
          color: '#f0f0f0',
        },
        horzLines: {
          color: '#f0f0f0',
        },
      },
      crosshair: {
        mode: 1,
      },
      rightPriceScale: {
        borderColor: '#cccccc',
      },
      timeScale: {
        borderColor: '#cccccc',
        timeVisible: true,
        secondsVisible: false,
      },
    });

    chartRef.current = chart;

    // Add candlestick series
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#10b981',
      downColor: '#ef4444',
      borderDownColor: '#ef4444',
      borderUpColor: '#10b981',
      wickDownColor: '#ef4444',
      wickUpColor: '#10b981',
    });

    // Prepare data - convert date strings to timestamps
    const chartData = data.map(item => {
      const date = new Date(item.Date);
      return {
        time: Math.floor(date.getTime() / 1000), // Convert to seconds
        open: parseFloat(item.Open),
        high: parseFloat(item.High),
        low: parseFloat(item.Low),
        close: parseFloat(item.Close),
      };
    }).filter(item => !isNaN(item.time) && !isNaN(item.open)); // Filter out invalid data

    console.log('Chart data:', chartData.slice(0, 5)); // Debug log

    if (chartData.length > 0) {
      candlestickSeries.setData(chartData);

      // Add volume series
      const volumeSeries = chart.addHistogramSeries({
        color: '#26a69a',
        priceFormat: {
          type: 'volume',
        },
        priceScaleId: '',
        scaleMargins: {
          top: 0.8,
          bottom: 0,
        },
      });

      const volumeData = data.map((item, index) => {
        const date = new Date(item.Date);
        const timestamp = Math.floor(date.getTime() / 1000);
        return {
          time: timestamp,
          value: parseInt(item.Volume) || 0,
          color: parseFloat(item.Close) >= parseFloat(item.Open) ? '#10b98180' : '#ef444480',
        };
      }).filter(item => !isNaN(item.time));

      if (volumeData.length > 0) {
        volumeSeries.setData(volumeData);
      }

      // Add indicators
      if (indicators.sma_20 && indicators.sma_20.length > 0) {
        const sma20Series = chart.addLineSeries({
          color: '#2196F3',
          lineWidth: 2,
          title: 'SMA 20',
        });
        
        const sma20Data = indicators.sma_20.map((value, index) => {
          if (index >= data.length || !data[index]) return null;
          const date = new Date(data[index].Date);
          return {
            time: Math.floor(date.getTime() / 1000),
            value: parseFloat(value),
          };
        }).filter(item => item && !isNaN(item.value) && item.value > 0);
        
        if (sma20Data.length > 0) {
          sma20Series.setData(sma20Data);
        }
      }

      if (indicators.sma_50 && indicators.sma_50.length > 0) {
        const sma50Series = chart.addLineSeries({
          color: '#FF9800',
          lineWidth: 2,
          title: 'SMA 50',
        });
        
        const sma50Data = indicators.sma_50.map((value, index) => {
          if (index >= data.length || !data[index]) return null;
          const date = new Date(data[index].Date);
          return {
            time: Math.floor(date.getTime() / 1000),
            value: parseFloat(value),
          };
        }).filter(item => item && !isNaN(item.value) && item.value > 0);
        
        if (sma50Data.length > 0) {
          sma50Series.setData(sma50Data);
        }
      }
    }

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current && chart) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chart) {
        chart.remove();
      }
    };
  }, [data, indicators, height]);

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-gray-100 rounded-lg">
        <p className="text-gray-500">No chart data available</p>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div ref={chartContainerRef} className="w-full" />
    </div>
  );
};

export default StockChart;