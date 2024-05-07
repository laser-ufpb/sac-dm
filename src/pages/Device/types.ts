import { ChartData } from "chart.js";

export interface DeviceData {
  device_id: number;
  value: number;
  timestamp: string;
}

export interface MyChartData extends ChartData<"line", number[], string> {}
