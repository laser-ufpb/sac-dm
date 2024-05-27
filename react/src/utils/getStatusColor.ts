export const getStatusColor = (status: string) => {
  switch (status) {
    case "Saudável":
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
