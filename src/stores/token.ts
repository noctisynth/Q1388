import { ref } from "vue";
import { defineStore } from "pinia";

export const useTokenStore = defineStore(
  "token",
  () => {
    const token = ref("");
    const setToken = (newToken: string) => {
      token.value = newToken;
    };
    const removeToken = () => {
      token.value = "";
    };

    return { token, setToken, removeToken };
  },
  {
    persist: true,
  }
);
