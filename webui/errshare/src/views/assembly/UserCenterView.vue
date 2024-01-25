<template>
  <el-alert title="当做样式。如需要，自行二次开发。" type="info" effect="dark"/>
  <el-row :gutter="20">
    <el-col :span="8">
      <div class="grid-content ep-bg-purple"/>
      <div class="bj">
        <h3 style="text-align: center;color: #606266;margin-top: 10px">个人信息</h3>
        <div style="margin-top: 20px; margin-left: 10px; color: #606266;">
          <div style="margin-top: 10px">
            <el-icon>
              <User/>
            </el-icon>
            {{ userName }}
          </div>
          <el-divider border-style="dashed"/>
          <div style="margin-top: 10px">
            <el-icon>
              <School/>
            </el-icon>
            贝尔实验室
          </div>
          <el-divider border-style="dashed"/>
          <div style="margin-top: 10px">
            <el-icon>
              <OfficeBuilding/>
            </el-icon>
            美国洛杉矶
          </div>
          <el-divider border-style="dashed"/>
          <div style="margin-top: 10px">
            <el-icon>
              <Star/>
            </el-icon>
            篮球，羽毛球，乒乓球，网球
          </div>
        </div>
      </div>
    </el-col>

    <el-col :span="16">
      <div class="grid-content ep-bg-purple"/>
      <div class="bj">
        <div style="margin-top: 20px; margin-left: 10px; color: #606266;">
          <div>
            <el-calendar v-model="value"/>
          </div>

        </div>
      </div>
    </el-col>

  </el-row>

</template>

<script>
import {reactive, toRefs, ref} from "vue";

export default {
  name: "UserCenterView",
  setup() {
    const data = reactive({
      testList: [],

    })
    const value = ref(new Date())
    const userName = localStorage.getItem('user')


    return {
      ...toRefs(data),
      value,
      userName,
    }

  }
}
</script>


<style scoped>
.bj {
  box-sizing: border-box;
  display: block;
  width: 100%;
  padding: 10px;
  background: #fff;
}

.el-alert {
  margin: 20px 0 0;
}

.el-alert:first-child {
  margin: 0;
}
</style>