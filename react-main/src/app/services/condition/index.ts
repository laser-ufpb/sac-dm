import { api } from "..";

class ConditionService {
    async getConditions() {
      try {
        const response = await api.get("/condition");
        return response.data;
      } catch (error) {
        console.error(error);
      }
    }
  }
  

const conditionService = new ConditionService();
export default conditionService;