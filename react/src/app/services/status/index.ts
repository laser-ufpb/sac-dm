import { api } from "..";

class StatusService {
  async getStatus() {
    try {
      const response = await api.get("/status");
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async postStatus(description: string) {
    try {
      const response = await api.post("/status", { description });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }
}

const statusService = new StatusService();
export default statusService;
