import { StatusProps } from "../types";

export const getStatusColor = (
  statusId: number,
  statusOptions: StatusProps[]
) => {
  const status = statusOptions.find((s) => s.id === statusId)?.description;

  switch (status) {
    case "Saudável":
      return "#35F33D";
    case "ONLINE":
      return "#35F33D";
    case "Alerta":
      return "#FFA500";
    case "Crítico":
      return "#FF0000";
    case "Offline":
      return "#9AA0A6";
    default:
      return "#9AA0A6";
  }
};
