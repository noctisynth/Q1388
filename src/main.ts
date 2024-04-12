import "virtual:uno.css";
import "primeicons/primeicons.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";
// @ts-ignore
import PrimeOne from "primevue/themes/primeone";
// @ts-ignore
import Aura from "primevue/themes/primeone/aura";
import Ripple from "primevue/ripple";

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

app.use(createPinia());
app.use(router);

app.mount("#app");
