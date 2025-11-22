import { useMemo, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Bar, Line, Doughnut, Scatter } from "react-chartjs-2";
import { Card } from "@/components/ui/card";
import { EquipmentData, EquipmentStats } from "@/types/equipment";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface ChartsProps {
  data: EquipmentData[];
  stats: EquipmentStats;
}

type MetricType = "Flowrate" | "Pressure" | "Temperature";

// Helper to create histogram data
const createHistogramData = (values: number[], bins = 10) => {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const binWidth = (max - min) / bins;
  const histogram = new Array(bins).fill(0);
  const labels: string[] = [];

  for (let i = 0; i < bins; i++) {
    const start = min + i * binWidth;
    const end = start + binWidth;
    labels.push(`${start.toFixed(0)}-${end.toFixed(0)}`);
  }

  values.forEach((v) => {
    const idx = Math.min(Math.floor((v - min) / binWidth), bins - 1);
    if (idx >= 0) histogram[idx]++;
  });

  return { histogram, labels };
};

// Helper to calculate box plot stats
const calcBoxPlotStats = (values: number[]) => {
  const sorted = [...values].sort((a, b) => a - b);
  const n = sorted.length;
  const q1 = sorted[Math.floor(n * 0.25)];
  const median = sorted[Math.floor(n * 0.5)];
  const q3 = sorted[Math.floor(n * 0.75)];
  const iqr = q3 - q1;
  const min = Math.max(sorted[0], q1 - 1.5 * iqr);
  const max = Math.min(sorted[n - 1], q3 + 1.5 * iqr);
  return { min, q1, median, q3, max, mean: values.reduce((a, b) => a + b, 0) / n };
};

export const Charts = ({ data, stats }: ChartsProps) => {
  const [selectedMetric, setSelectedMetric] = useState<MetricType>("Flowrate");

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" as const },
    },
  };

  const metricColors: Record<MetricType, string> = {
    Flowrate: "rgba(59, 130, 246, 0.8)",
    Pressure: "rgba(16, 185, 129, 0.8)",
    Temperature: "rgba(249, 115, 22, 0.8)",
  };

  const typeColors = [
    "rgba(59, 130, 246, 0.8)",
    "rgba(16, 185, 129, 0.8)",
    "rgba(249, 115, 22, 0.8)",
    "rgba(239, 68, 68, 0.8)",
    "rgba(139, 92, 246, 0.8)",
    "rgba(236, 72, 153, 0.8)",
  ];

  // Equipment Distribution (existing)
  const doughnutChartData = useMemo(() => {
    const types = Object.keys(stats.typeDistribution);
    const counts = Object.values(stats.typeDistribution);
    return {
      labels: types,
      datasets: [{
        data: counts,
        backgroundColor: typeColors.slice(0, types.length),
        borderColor: typeColors.slice(0, types.length).map(c => c.replace("0.8", "1")),
        borderWidth: 2,
      }],
    };
  }, [stats.typeDistribution]);

  // Histogram data for selected metric
  const histogramData = useMemo(() => {
    const values = data.map((d) => d[selectedMetric]).filter((v) => !isNaN(v));
    const { histogram, labels } = createHistogramData(values, 12);
    return {
      labels,
      datasets: [{
        label: `${selectedMetric} Distribution`,
        data: histogram,
        backgroundColor: metricColors[selectedMetric],
        borderColor: metricColors[selectedMetric].replace("0.8", "1"),
        borderWidth: 1,
      }],
    };
  }, [data, selectedMetric]);

  // Box plot simulation using bar chart with error bars concept
  const boxPlotData = useMemo(() => {
    const values = data.map((d) => d[selectedMetric]).filter((v) => !isNaN(v));
    const stats = calcBoxPlotStats(values);
    return {
      labels: ["All Data"],
      datasets: [
        {
          label: "Min",
          data: [stats.min],
          backgroundColor: "rgba(100, 116, 139, 0.6)",
          borderColor: "rgba(100, 116, 139, 1)",
          borderWidth: 1,
        },
        {
          label: "Q1",
          data: [stats.q1],
          backgroundColor: metricColors[selectedMetric].replace("0.8", "0.4"),
          borderColor: metricColors[selectedMetric].replace("0.8", "1"),
          borderWidth: 1,
        },
        {
          label: "Median",
          data: [stats.median],
          backgroundColor: metricColors[selectedMetric],
          borderColor: metricColors[selectedMetric].replace("0.8", "1"),
          borderWidth: 2,
        },
        {
          label: "Q3",
          data: [stats.q3],
          backgroundColor: metricColors[selectedMetric].replace("0.8", "0.4"),
          borderColor: metricColors[selectedMetric].replace("0.8", "1"),
          borderWidth: 1,
        },
        {
          label: "Max",
          data: [stats.max],
          backgroundColor: "rgba(100, 116, 139, 0.6)",
          borderColor: "rgba(100, 116, 139, 1)",
          borderWidth: 1,
        },
      ],
    };
  }, [data, selectedMetric]);

  // By equipment type - grouped bar chart
  const byTypeData = useMemo(() => {
    const types = Object.keys(stats.typeDistribution);
    const typeStats = types.map((type) => {
      const typeData = data.filter((d) => d.Type === type);
      const values = typeData.map((d) => d[selectedMetric]).filter((v) => !isNaN(v));
      if (values.length === 0) return { mean: 0, min: 0, max: 0 };
      return {
        mean: values.reduce((a, b) => a + b, 0) / values.length,
        min: Math.min(...values),
        max: Math.max(...values),
      };
    });

    return {
      labels: types,
      datasets: [
        {
          label: "Min",
          data: typeStats.map((s) => s.min),
          backgroundColor: "rgba(100, 116, 139, 0.6)",
          borderColor: "rgba(100, 116, 139, 1)",
          borderWidth: 1,
        },
        {
          label: "Mean",
          data: typeStats.map((s) => s.mean),
          backgroundColor: metricColors[selectedMetric],
          borderColor: metricColors[selectedMetric].replace("0.8", "1"),
          borderWidth: 1,
        },
        {
          label: "Max",
          data: typeStats.map((s) => s.max),
          backgroundColor: metricColors[selectedMetric].replace("0.8", "0.5"),
          borderColor: metricColors[selectedMetric].replace("0.8", "1"),
          borderWidth: 1,
        },
      ],
    };
  }, [data, stats.typeDistribution, selectedMetric]);

  // Correlation scatter plot
  const correlationData = useMemo(() => {
    return {
      datasets: [
        {
          label: "Flowrate vs Pressure",
          data: data.slice(0, 50).map((d) => ({ x: d.Flowrate, y: d.Pressure })),
          backgroundColor: "rgba(59, 130, 246, 0.6)",
          borderColor: "rgba(59, 130, 246, 1)",
          pointRadius: 6,
        },
        {
          label: "Flowrate vs Temperature",
          data: data.slice(0, 50).map((d) => ({ x: d.Flowrate, y: d.Temperature })),
          backgroundColor: "rgba(249, 115, 22, 0.6)",
          borderColor: "rgba(249, 115, 22, 1)",
          pointRadius: 6,
        },
      ],
    };
  }, [data]);

  // Flowrate vs Pressure bar (existing style)
  const barChartData = useMemo(() => ({
    labels: data.slice(0, 10).map((item) => item["Equipment Name"]),
    datasets: [
      {
        label: "Flowrate",
        data: data.slice(0, 10).map((item) => item.Flowrate),
        backgroundColor: "rgba(59, 130, 246, 0.9)",
        borderColor: "rgba(59, 130, 246, 1)",
        borderWidth: 1,
      },
      {
        label: "Pressure",
        data: data.slice(0, 10).map((item) => item.Pressure),
        backgroundColor: "rgba(20, 184, 166, 0.7)",
        borderColor: "rgba(20, 184, 166, 1)",
        borderWidth: 1,
      },
    ],
  }), [data]);

  // Temperature trend (existing)
  const lineChartData = useMemo(() => ({
    labels: data.slice(0, 15).map((item) => item["Equipment Name"]),
    datasets: [{
      label: "Temperature",
      data: data.slice(0, 15).map((item) => item.Temperature),
      borderColor: "rgba(249, 115, 22, 1)",
      backgroundColor: "rgba(249, 115, 22, 0.1)",
      tension: 0.4,
      fill: true,
    }],
  }), [data]);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Metric Selector */}
      <Card className="p-4 shadow-medium opacity-75">
        <div className="flex items-center gap-4 flex-wrap">
          <span className="font-semibold text-foreground">Analyze Metric:</span>
          {(["Flowrate", "Pressure", "Temperature"] as MetricType[]).map((metric) => (
            <button
              key={metric}
              onClick={() => setSelectedMetric(metric)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                selectedMetric === metric
                  ? "bg-primary text-primary-foreground shadow-md"
                  : "bg-muted hover:bg-muted/80 text-foreground"
              }`}
            >
              {metric}
            </button>
          ))}
        </div>
      </Card>

      {/* Row 1: Histogram and Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 shadow-medium opacity-75">
          <h3 className="text-lg font-semibold mb-4 text-foreground">
            {selectedMetric} Distribution (Histogram)
          </h3>
          <div className="h-72">
            <Bar options={{
              ...chartOptions,
              plugins: { ...chartOptions.plugins, legend: { display: false } },
              scales: {
                y: { beginAtZero: true, title: { display: true, text: "Frequency" } },
                x: { title: { display: true, text: selectedMetric } },
              },
            }} data={histogramData} />
          </div>
        </Card>

        <Card className="p-6 shadow-medium opacity-75">
          <h3 className="text-lg font-semibold mb-4 text-foreground">
            {selectedMetric} Statistics
          </h3>
          <div className="h-72">
            <Bar options={{
              ...chartOptions,
              indexAxis: "y" as const,
              scales: { x: { beginAtZero: true } },
            }} data={boxPlotData} />
          </div>
        </Card>
      </div>

      {/* Row 2: By Type Analysis */}
      <Card className="p-6 shadow-medium opacity-75">
        <h3 className="text-lg font-semibold mb-4 text-foreground">
          {selectedMetric} by Equipment Type
        </h3>
        <div className="h-80">
          <Bar options={{
            ...chartOptions,
            scales: {
              y: { beginAtZero: true, title: { display: true, text: selectedMetric } },
              x: { title: { display: true, text: "Equipment Type" } },
            },
          }} data={byTypeData} />
        </div>
      </Card>

      {/* Row 3: Original Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 shadow-medium opacity-75">
          <h3 className="text-lg font-semibold mb-4 text-foreground">
            Flowrate vs Pressure (Top 10)
          </h3>
          <div className="h-80">
            <Bar options={chartOptions} data={barChartData} />
          </div>
        </Card>

        <Card className="p-6 shadow-medium opacity-75">
          <h3 className="text-lg font-semibold mb-4 text-foreground">
            Temperature Trend
          </h3>
          <div className="h-80">
            <Line options={chartOptions} data={lineChartData} />
          </div>
        </Card>
      </div>

      {/* Row 4: Correlation and Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 shadow-medium opacity-75">
          <h3 className="text-lg font-semibold mb-4 text-foreground">
            Correlation Analysis
          </h3>
          <div className="h-80">
            <Scatter options={{
              ...chartOptions,
              scales: {
                x: { title: { display: true, text: "Flowrate" } },
                y: { title: { display: true, text: "Value" } },
              },
            }} data={correlationData} />
          </div>
        </Card>

        <Card className="p-6 shadow-medium opacity-75">
          <h3 className="text-lg font-semibold mb-4 text-foreground">
            Equipment Type Distribution
          </h3>
          <div className="h-80 flex items-center justify-center">
            <div className="w-full max-w-sm">
              <Doughnut data={doughnutChartData} options={chartOptions} />
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};