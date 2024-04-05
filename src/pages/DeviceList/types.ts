export interface DeviceProps {
  device_code: string;
  id: number;
  timestamp: string;
  status: "Saudável" | "Alerta" | "Crítico" | "Offline";
}
