<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item>数据表盘</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
  <div id="d01" style="width: auto; height: 500px; margin-top: 15px;"></div>
</template>

<script>
import {getDataGet} from "@/utils/apis"
import {useRouter} from "vue-router";
import { ArrowRight } from '@element-plus/icons-vue';

export default {

  mounted() {
    const router = useRouter();
    let d01 = this.$echarts.init(document.getElementById("d01"));

    function showDataD01() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      getDataGet().then(res => {
        let xaxisData = res.class_list;
        let seriesData = res.num_list;

        d01.setOption({
          title: {text: "文章类分布图"},
          tooltip: {},
          xAxis: {
            data: xaxisData,
          },
          yAxis: {},
          series: [
            {
              name: "文章量",
              type: "line",
              data: seriesData,
              areaStyle: {
                color: '#f3c717',
                opacity: 1,
              },
            },
          ],
        });
      });
    }

    showDataD01();

    return {
      ArrowRight,
    };
  },

};
</script>

<style scoped>
#d01 {
  background-color: #fff;
}
</style>
