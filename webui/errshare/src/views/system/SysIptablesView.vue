<template>
  <div>
    <el-alert title="个人私服使用，并不完善。如需要，自己二次开发。" type="warning" effect="dark"/>
  </div>

  <div class="bj" style="margin-top: 15px">
    <div>
      <el-button type="primary" @click="addRule">添加规则</el-button>
      <!-- 添加规则弹窗对话框 -->
      <el-dialog v-model="dialogFormVisible" title="添加规则">
        <el-form
            :model="fromRule"
            :rules="rules"
            ref="ruleFrom"
            label-width="120px"
            class="demo-ruleForm"
        >
          <el-form-item label="规则" prop="rule">
            <el-input id="rule" style="width: 80%;" v-model="fromRule.rule" placeholder="添加iptables规则"/>
          </el-form-item>
        </el-form>
        <template #footer>
          <div>
            <el-button type="danger" @click="cancellationRule">取消</el-button>
            <el-button type="warning" @click="resetRuleData">重置</el-button>
            <el-button type="primary" @click="confirmsRule(ruleFrom)">确认</el-button>
          </div>
        </template>
      </el-dialog>
    </div>

    <ul class="infinite-list" style="overflow: auto; margin-top: 10px;">
      <el-table :data="iptablesRuleList" style="width: 100%">
        <el-table-column width="200" prop="num" label="序列号"/>
        <el-table-column prop="rule" label="规则"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="danger" @click="deleteRule(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </ul>

  </div>

</template>

<script>
import {reactive, ref, toRefs} from "vue";
import {getIptablesGet, addRulePost, deleteRuleDel} from "@/utils/apis"
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";

export default {
  name: "SysIptablesView",
  setup() {
    const data = reactive({
      iptablesRuleList: [],
      dialogFormVisible: false,
      fromRule: {
        rule: "",
      },
      rules: {
        rule: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
      },
    })

    const ruleFrom = ref()
    const addRule = () => {
      data.dialogFormVisible = true
    }
    const resetRuleData = () => {
      data.fromRule.rule = '';
    }
    const cancellationRule = () => {
      //重置表单
      resetRuleData()
      data.dialogFormVisible = false
    }
    const router = useRouter();

    function showIptablesRule() {
      if (localStorage.getItem('userToken') === "undefined" || localStorage.getItem('userToken') === null) {
        router.push({name: 'loginView'});
        return
      }
      getIptablesGet().then(
          res => {
            if (res.code != 200) {
              ElMessage(
                  {
                    message: res.msg,
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            data.iptablesRuleList = res.rule_list;
          }
      )

    }

    const confirmsRule = (fromRule) => {
      if (localStorage.getItem('userToken') === "undefined" || localStorage.getItem('userToken') === null) {
        router.push({name: 'loginView'});
        return
      }
      fromRule.validate(
          res => {
            if (!res) {
              return
            }
            addRulePost(data.fromRule).then(
                res => {
                  resetRuleData()
                  data.dialogFormVisible = false
                  showIptablesRule()
                  if (res.code != 200) {
                    ElMessage(
                        {
                          message: res.msg,
                          type: "error",
                          duration: 5000,
                        }
                    )
                    return
                  }
                  ElMessage(
                      {
                        message: res.msg,
                        type: "success",
                        duration: 5000,
                      }
                  )
                }
            )
          }
      )
    }

    const deleteRule = row => {
      if (localStorage.getItem('userToken') === "undefined" || localStorage.getItem('userToken') === null) {
        router.push({name: 'loginView'});
        return
      }
      const {num} = row
      // 请求里必须传入对象
      deleteRuleDel({"ruleNum": num}).then(
          res => {
            showIptablesRule()
            if (res.code != 200) {
              ElMessage(
                  {
                    message: res.msg,
                    type: "error",
                    duration: 5000,
                  }
              )
              return
            }
            ElMessage(
                {
                  message: res.msg,
                  type: "success",
                  duration: 5000,
                }
            )
          }
      )

    }

    showIptablesRule()

    return {
      ...toRefs(data),
      ruleFrom,
      addRule,
      resetRuleData,
      cancellationRule,
      confirmsRule,
      deleteRule,
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