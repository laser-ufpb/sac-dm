import { api } from "..";

interface SacDmFilterOptions {
  vehicleId?: number;
  datetimeInitial?: string;
  datetimeFinal?: string;
  limit?: number;
}

class SacDmService {
  async getSacDm(limit?: number) {
    try {
      const response = await api.get("/sac_dm", {
        params: {
          limit: limit || 1000,
        },
      });
      return response.data.reverse();
    } catch (error) {
      console.error(error);
    }
  }

  async getSacDmByFilter(options: SacDmFilterOptions = {}) {
    const { vehicleId, datetimeInitial, datetimeFinal, limit } = options;

    try {
      const response = await api.get(`/sac_dm_by_filter`, {
        params: {
          limit: limit,
          vehicle_id: vehicleId,
          datetime_initial: datetimeInitial,
          datetime_final: datetimeFinal,
        },
      });

      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async postSacDm() {
    try {
      const value = Math.floor(Math.random() * 11);
      const timestamp = new Date().toISOString();

      const response = await api.post("/sac_dm", [
        {
          device_id: 1,
          value: value,
          timestamp: timestamp,
        },
      ]);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }
}

const sacDmService = new SacDmService();
export default sacDmService;
