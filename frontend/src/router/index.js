import { createRouter, createWebHistory } from "vue-router";
import AboutView from "../views/AboutView.vue";
import HomeView from "../views/HomeView.vue";
import LoginregisterView from "../views/LoginregisterView.vue";
import PostZoom from "../components/PostZoom.vue";
import UserProfile from "../components/UserProfile.vue";
import EditProfile from "../components/EditProfile.vue";

const routes = [
  {
    path: "/",
    name: "loginregister",
    component: LoginregisterView,
  },
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: AboutView,
  },
  {
    path: '/postZoom/:id',
    name:"postZoom",
    component: PostZoom,
    props: true,
  },
  {
    path: '/user/:id',
    name:"userProfile",
    component: UserProfile,
    props: true,
  },
  {
    path: '/editProfile/:id',
    name:"editProfile",
    component: EditProfile,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
