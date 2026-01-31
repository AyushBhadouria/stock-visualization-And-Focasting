import React, { useMemo } from 'react';

const Sparkline = ({ data = [1, 2, 3, 2, 4, 3, 5, 4, 6, 5], sentiment = 'up', size = 'sm' }) => {
  const { viewBox, path, color } = useMemo(() => {
    const points = data.length;
    const width = 100;
    const height = 30;
    
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    
    // Create SVG path
    let pathData = `M 0 ${height - ((data[0] - min) / range) * height}`;
    for (let i = 1; i < points; i++) {
      const x = (i / (points - 1)) * width;
      const y = height - ((data[i] - min) / range) * height;
      pathData += ` L ${x} ${y}`;
    }
    
    const isUp = data[data.length - 1] >= data[0];
    const col = isUp ? '#10B981' : '#EF4444';
    
    return {
      viewBox: `0 0 ${width} ${height}`,
      path: pathData,
      color: col,
    };
  }, [data]);

  const sizeClasses = {
    sm: 'w-12 h-6',
    md: 'w-16 h-8',
    lg: 'w-24 h-10',
  };

  return (
    <svg
      viewBox={viewBox}
      className={`${sizeClasses[size]} opacity-80`}
      preserveAspectRatio="none"
    >
      <polyline
        points={path}
        fill="none"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <polyline
        points={path}
        fill={color}
        fillOpacity="0.1"
        stroke="none"
      />
    </svg>
  );
};

export default Sparkline;
