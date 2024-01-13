<template>
  <div id="d01" style="width: auto; height: 500px;"></div>
</template>

<script>
import {getDataGet} from "@/utils/apis"

export default {

  mounted() {
    let d01 = this.$echarts.init(document.getElementById("d01"));

    function showDataD01(){
      getDataGet().then(res => {
        let xaxisData = res.class_list;
        let seriesData = res.num_list;

        d01.setOption({
          title: { text: "文章类分布图" },
          tooltip: {},
          xAxis: {
            data: xaxisData,
          },
          yAxis: {},
          series: [
            {
              name: "文章量",
              type: "bar",
              data: seriesData,
            },
          ],
        });
      });
    }

    showDataD01();

    return {};
  },

};
</script>

<style scoped>
#d01 {
  background-color: #fff;
}
</style>
