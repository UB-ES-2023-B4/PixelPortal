import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

//Development backend path
//app.config.globalProperties.backendPath = "http://localhost:8000";

//Production backend path
app.config.globalProperties.backendPath =
  "https://pixelportal-backend-api.onrender.com";

app.use(router).mount("#app");
