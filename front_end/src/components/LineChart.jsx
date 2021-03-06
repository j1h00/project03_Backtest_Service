import { createChart } from "lightweight-charts";
import React, { useEffect, useRef } from "react";

/**
 * prop.data 로
 *
 * [{ time: "2006-01-02", value: 24.89 }
 * , { time: "2006-01-02", value: 24.89 }]
 *
 * 위 형식의 데이터를 받는다.
 *
 *  */
export default function Chart({ data }) {
  const chartContainerRef = useRef();

  // 데이터가 변경될 때 그래프를 그린다.
  useEffect(() => {
    var chart = createChart(chartContainerRef.current, {
      layout: {
        backgroundColor: "#ffffff",
        textColor: "#d1d4dc",
      },
      grid: {
        vertLines: {
          visible: false,
        },
        horzLines: {},
      },
      rightPriceScale: {
        borderVisible: false,
      },
      timeScale: {
        borderVisible: false,
      },
      crosshair: {
        horzLine: {
          visible: false,
        },
      },
    });

    var areaSeries = null;

    // 데이터 셋팅 함수
    function syncToInterval(data) {
      if (areaSeries) {
        chart.removeSeries(areaSeries);
        areaSeries = null;
      }
      areaSeries = chart.addAreaSeries({
        topColor: "rgba(24, 33, 109, 0.56)",
        bottomColor: "rgba(24, 33, 109, 0.04)",
        lineColor: "rgba(24, 33, 109, 1)",
        lineWidth: 2,
      });
      areaSeries.setData(data);
    }

    syncToInterval(data);

    const handleResize = () => {
      console.log("@ resized here");
      chart.applyOptions({ width: chartContainerRef.current.clientWidth });
    };

    window.addEventListener("resize", handleResize);
    // 종료시 차트 제거
    return () => {
      window.removeEventListener("resize", handleResize);

      chart.remove();
    };
  }, [data]);

  // 컴포넌트 반환
  return <div className="w-full" ref={chartContainerRef} />;
}
