import axios from "axios";

export const api = axios.create({
  baseURL: "http://150.165.167.12:8100/",
});
