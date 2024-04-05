export const getStatusColor = (
  status: "Saudável" | "Alerta" | "Crítico" | "Offline"
) => {
  switch (status) {
    case "Saudável":
      return "#35F33D";
    case "Alerta":
      return "#E8FF5D";
    case "Crítico":
      return "#FF0000";
    case "Offline":
      return "#9AA0A6";
    default:
      return "#9AA0A6";
  }
};
