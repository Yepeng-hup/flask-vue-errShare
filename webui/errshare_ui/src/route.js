import { createRouter, createWebHashHistory } from "vue-router";



const routes = [
    {path: "/", component: () => import("./views/HomeView.vue"), name: "HomeView"}, 
    {path: "/user/create", component: () => import("./views/UserCreateView.vue"), name: "UserCreateView"},
    {path: "/wz/pic", component: () => import("./views/ArticlePicView.vue"), name: "ArticlePicView"},
    {path: "/wz/category", component: () => import("./views/CategoryView.vue"), name: "CategoryView"},
    {path: "/wz/write", component: () => import("./views/ArticleWritingView.vue"), name: "ArticleWritingView"},
    {path: "/wz/label", component: () => import("./views/ArticleLabelView.vue"), name: "ArticleLabelView"},
    {path: "/data", component: () => import("./views/DataView.vue"), name: "DataView"},
    
];


const route = createRouter({
    // 4. 内部提供了 history 模式的实现。这里使用 hash 模式。
    history: createWebHashHistory(),
    routes, // `routes: routes` 的缩写
});


export default route;
