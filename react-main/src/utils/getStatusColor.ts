import { StatusProps } from "../types";

export const getStatusColor = (
  statusId: number,
  statusOptions: StatusProps[]
) => {

  switch (statusId) {
    case 1:
      return "#9AA0A6";
    case 3:
      return "#35F33D";
    default:
      return "#9AA0A6";
    // case "ONLINE":
    //   return "#35F33D";
  }
};
