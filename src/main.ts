import "virtual:uno.css";
import "primeicons/primeicons.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import PrimeVue from "primevue/config";
// @ts-ignore
import PrimeOne from "primevue/themes/primeone";
// @ts-ignore
import Aura from "primevue/themes/primeone/aura";
import Ripple from "primevue/ripple";
import ToastService from 'primevue/toastservice';

import App from "./App.vue";
import router from "./router";

const app = createApp(App);
app.use(PrimeVue, {
  ripple: true,
  theme: {
    base: PrimeOne,
    preset: Aura,
    options: {
      prefix: "p",
      darkModeSelector: "system",
      cssLayer: false,
    },
  },
});

app.directive("ripple", Ripple);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(ToastService)
app.use(pinia);
app.use(router);
app.use(ToastService);
app.mount("#app");
