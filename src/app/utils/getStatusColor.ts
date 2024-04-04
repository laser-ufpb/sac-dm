export const getStatusColor = (
  status: "HEALTHY" | "WARNING" | "CRITICAL" | "OFFLINE"
) => {
  switch (status) {
    case "HEALTHY":
      return "#35F33D";
    case "WARNING":
      return "#E8FF5D";
    case "CRITICAL":
      return "#FF0000";
    case "OFFLINE":
      return "#9AA0A6";
    default:
      return "#9AA0A6";
  }
};
