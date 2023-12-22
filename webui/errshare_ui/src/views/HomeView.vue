<template>
  <el-row :gutter="50">

    <el-col :span="10"><div class="grid-content ep-bg-purple" />
      <div style="background: #fff; border: 1px solid rgb(232, 224, 224);">
        <h4 style="padding: 5px;">服务检测</h4>
        <el-divider border-style="dashed" />
        <div style="padding: 10px;">
          <el-button type="success">mangodb检测</el-button>
          <el-button type="success">站点检测</el-button>
          <el-button type="success">服务器检测</el-button>
        </div>
        <div id="check-text" style="padding: 5px;">
          我是检测回调数据展示区
        </div>
      </div>
    </el-col>

    <el-col :span="12"><div class="grid-content ep-bg-purple" />
      <div style="background: #fff; border: 1px solid rgb(232, 224, 224);">
        <h4 style="text-align: center; margin-top: 10px;">欢迎使用ErrShare共享平台</h4>
        <p style="padding: 15px;">errShare是一款为公司内部故障共享系统，就是日常工作中遇到的所有技术难题及解决方案和思路的共享平台。</p>
      </div>
    </el-col>

  </el-row>
</template>
  
<script>
  export default {
    name: "homeView"
  }
</script>

<style scoped>

</style>