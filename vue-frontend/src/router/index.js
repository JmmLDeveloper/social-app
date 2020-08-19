/* eslint-disable */

import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Registration from "../views/Registration.vue";
import store from "../store/index";
import PostForm from '../views/PostForm.vue'
import Feed from '../views/Feed.vue'
import PostDetail from '../views/PostDetail.vue'
import CommentForm from '../views/CommentForm.vue'
import Filters from '../views/Filters.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: "/filters",
    name: "Filters",
    component: Filters
  },
  {
    path: "/posts/:id",
    name: "Post",
    component: PostDetail,
  },
  {
    path: "/posts/:postId/comments/:commentId/edit",
    name: "EditForm",
    component: CommentForm,
  },
  {
    path: "/posts/:postId/comments/create",
    name: "CreateForm",
    component: CommentForm,
  },
  {
    path: "/posts",
    name: "Feed",
    component: Feed,
  },
  {
    path: "/posts/:id/edit",
    name: "EditPost",
    component: PostForm,
  },
  {
    path: "/create-post",
    name: "CreateForm",
    component: PostForm,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/registration",
    name: "Registration",
    component: Registration,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (
    to.fullPath != "/login" &&
    to.fullPath != "/registration" &&
    store.getters.getToken === null
  ) {
    next("/login");
  } else next();
  
});
export default router;
