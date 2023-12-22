<template>
    <div class="frame">
      <el-container class="frame-container">
          <!-- 数据绑定和逻辑判断 -->
          <el-aside :width="iszt ? '64px' : '200px'" class="aside">
            <el-row class="menu-row">
              <el-col :span="24">
  
                <el-menu
                  active-text-color="#ffd04b"
                  background-color="#545c64"
                  text-color="#fff"
                  default-active="1"
                  :collapse=iszt
                  :collapse-transition="false"
                  :router="true"
                >
                <div style="padding: 15px;">
                  <h2><a href="/">errShare</a></h2>
                </div>

                <el-menu-item index="1" :route="{name: 'HomeView'}">
                  <el-icon><House /></el-icon>
                  <span>首页</span>
                </el-menu-item>

                <el-menu-item v-if="showUserManagement" index="2" :route="{name: 'UserCreateView'}">
                  <el-icon><User /></el-icon>
                  <span>用户管理</span>
                </el-menu-item>
  
                  <el-sub-menu v-if="showArticleManagement" index="3">
                    <template #title>
                      <el-icon><Document /></el-icon>
                      <span>文章管理</span>
                    </template>
                    <el-menu-item-group>
                      <el-menu-item index="3-1" :route="{name: 'ArticlePicView'}">文章版图</el-menu-item>
                      <el-menu-item index="3-2" :route="{name: 'ArticleWritingView'}">文章编写</el-menu-item>
                      <el-menu-item index="3-3" :route="{name: 'CategoryView'}">文章分类</el-menu-item>
                      <el-menu-item index="3-4" :route="{name: 'ArticleLabelView'}">文章标签</el-menu-item>
                    </el-menu-item-group>
                  </el-sub-menu>
  
                  <el-menu-item index="4" :route="{name: 'DataView'}">
                    <el-icon><Monitor /></el-icon>
                    <span>数据表盘</span>
                  </el-menu-item>
  
                </el-menu>
              </el-col>
            </el-row>
          </el-aside>

          <el-container>
          <el-header class="header">
          <div class="header-content">
            <div class="sj-button">
              <span @click="sj"><b>窗口伸缩</b></span>
              <span style="margin-left: 20px;"><a :href="serverIndexUrl" target=_blank><b>站点</b></a></span>
              <span style="margin-left: 20px;"><a href="https://github.com/Yepeng-hup/errShare.git"><b>github</b></a></span>
            </div>
          <div>

            <el-dropdown>
              <el-button type="success" style="color: #ffffff; background: #5cb85c;">你好 {{ title }}</el-button>
              <template #dropdown>
                <el-dropdown-menu>  
                  <el-dropdown-item> 
                    <!-- <a href="/user/create"><span class="hover-text">设置</span></a>   -->
                    <el-menu 
                      default-active="1"
                      :router="true"
                    >
                    <el-menu-item style="padding: 0px; height: 25px;;" index="1" :route="{name: 'HomeView'}">
                      <span class="hover-text">设置</span>
                    </el-menu-item>
                    </el-menu>
                  </el-dropdown-item>  
                  <el-dropdown-item>  
                    <a href="/"><span class="hover-text">退出</span></a>  
                  </el-dropdown-item>  
                </el-dropdown-menu>  
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

          <el-main>
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>
    </div>
  
  </template>
  
<script>
  import { ref, onMounted } from 'vue'

  import {userLoginPost} from '@/utils/apis'

  
  export default {

    setup(){

      const iszt = ref(false);
      const showUserManagement = ref(false);
      const showArticleManagement = ref(true);
      const title = ref("")
  
    // 定义侧边栏伸缩函数
      const sj=()=>{
        iszt.value = !iszt.value
      }

      const fetchUserData = async () => {
        userLoginPost().then(
          res => {
                    let roleName=res.role;
                    let userName=res.username;
                    title.value = userName;
                    
                    if (roleName == "admin"){
                        const userData = { isAdmin: true };
                        showUserManagement.value = userData.isAdmin;
                        showArticleManagement.value = userData.isAdmin;
                  

                    } else if (roleName == "ordinary"){
                        const userData = { isAdmin: false };
                        const articleData = { isAdmin: true };
                        showUserManagement.value = userData.isAdmin;
                        showArticleManagement.value = articleData.isAdmin;

                    }else {
                      const xx = "xx"
                      console.log(xx)
                    }             
            }
        )
    };

    onMounted(() => {
      // Fetch user data when the component is mounted
      fetchUserData();
    });

      return {
        iszt: iszt,
        sj,
        title,
        serverIndexUrl: "http://192.168.1.119:8088/test",
        showUserManagement,
        showArticleManagement,
      }
    }
  
  };
</script>
  
  
<style scoped>
  .frame-container {
    height: 100vh;
  }
  .header {
    height: 60px;
    background: #5cb85c;
    display: flex;
  }
  
  .header .brand {
    width: 200px;
    margin-left: -20px;
    background-color: #545c64;
    font-size: 20px;
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .header .header-content {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-left: 20px;
    color: #fff;
  }
  
  .header-content .signout {
      cursor: pointer;
    }
  
  .aside {
    background-color: #545c64;
  }
  
  .aside .el-menu .is-active {
    background-color: #434a50 !important;
  }
  
  .footer {
    background: gray;
  }
  </style>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
  
  <style scoped>
  .el-menu{
    border-right: none;
  }
  .el-main{
    background: #efefef;
  }
  </style>
  
  
  <style scoped>
  .sj-button {
    color: #fff;
    cursor: pointer;
  }
  a {
      text-decoration: none;
      color: #fff;
    }
  
  </style>
  
  <style>
  * {
    margin: 0;
    padding: 0;
    border: 0;
    text-decoration: none;
    vertical-align: baseline;
  }

  .home-centext{
    box-sizing: border-box;
    display: block;
    width: 100%;
    padding: 10px;
    background: #fff;
    margin-top: 15px;
  }

  .flex{
    display: flex;
    align-items: center;
  }

  .hover-text {
  color: black;
}
 
.hover-text:hover {
  color: rgb(0, 115, 255); /* 鼠标放上去时的文字颜色 */
}

</style>

<style>
.infinite-list {
  height: 300px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.infinite-list .infinite-list-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  background: var(--el-color-primary-light-9);
  margin: 5px;
  color: var(--el-color-primary);
}
.infinite-list .infinite-list-item + .list-item {
  margin-top: 5px;
}
.tests{
  background: #12cc4400;
}
</style>