export interface DeviceProps {
  device_code: string;
  id: number;
  timestamp: string;
  status: "HEALTHY" | "WARNING" | "CRITICAL" | "OFFLINE";
}
