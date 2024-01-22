import { createRouter, createWebHashHistory } from "vue-router";


const routes = [
    {
        path: "/",
        name: "loginView",
        component: () => import("./views/assembly/LoginView.vue"),
    },

    {
        path: "/errshare",
        name: "layout",
        component: () => import("./views/layout/LayoutView.vue"),
        // 重定向
        redirect: '/home',
        children: [
            {path: "/home", component: () => import("./views/assembly/HomeView.vue"), name: "HomeView"}, 
            {path: "/user/create", component: () => import("./views/assembly/UserCreateView.vue"), name: "UserCreateView"},
            {path: "/wz/pic", component: () => import("./views/assembly/ArticlePicView.vue"), name: "ArticlePicView"},
            {path: "/wz/category", component: () => import("./views/assembly/CategoryView.vue"), name: "CategoryView"},
            {path: "/wz/write", component: () => import("./views/assembly/ArticleWritingView.vue"), name: "ArticleWritingView"},
            {path: "/wz/label", component: () => import("./views/assembly/ArticleLabelView.vue"), name: "ArticleLabelView"},
            {path: "/data", component: () => import("./views/assembly/DataView.vue"), name: "DataView"},
            {path: "/recovery", component: () => import("./views/assembly/RecoveryView.vue"), name: "RecoveryView"},
            {path: "/user/center", component: () => import("./views/assembly/UserCenterView.vue"), name: "UserCenterView"},
        ]
    },
    
];


const route = createRouter({
    // 内部提供了 history 模式的实现。这里使用 hash 模式。
    history: createWebHashHistory(),
    routes,
});


export default route;
