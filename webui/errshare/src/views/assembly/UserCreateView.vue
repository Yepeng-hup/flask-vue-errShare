<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
    </el-breadcrumb>
  </div>

  <div id="usercreate" style="margin-top: 15px">
    <div class="home-centext">
      <div class="flex">
        <div class="input-box">
          <el-input
              v-model="searchText"
              placeholder="输入关键字"
              class="input-with-select"
          >
            <template #append>
              <el-button @click="searchUser">
                <el-icon>
                  <Search/>
                </el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
        <el-button type="primary" @click="addUser">新建用户</el-button>
        <el-button type="primary" @click="updatePasswd">密码修改</el-button>
        <el-button type="primary" @click="blackListUser">黑名单用户</el-button>
      </div>
      <!-- :data后面是数据源元组加对象 -->
      <ul class="infinite-list" style="overflow: auto">
        <el-table :data="userInfoList">
          <el-table-column prop="user" label="用户名" width="100"/>
          <el-table-column prop="role" label="角色" width="100"/>
          <el-table-column prop="phone" label="电话"/>
          <el-table-column prop="mailbox" label="邮箱"/>
          <el-table-column prop="mg_state" label="状态" >
            <template #default="scope">
              <el-switch v-model="scope.row.mg_state"/>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="primary" @click="editUser(scope.row)">编辑</el-button>
              <el-popconfirm
                  confirm-button-text="确定"
                  confirm-button-type="danger"
                  cancel-button-text="取消"
                  cancel-button-type="primary"
                  :icon="InfoFilled"
                  icon-color="#f3715c"
                  title="确认删除?"
                  @confirm="deleteUser(scope.row)"
                  @cancel="cancelEvent"
              >
                <template #reference>
                  <el-button type="danger">删除</el-button>
                </template>

              </el-popconfirm>
            </template>
          </el-table-column>

        </el-table>
      </ul>

      <!-- 分页 -->
      <el-pagination
          style="margin-top: 20px;"
          small
          background
          layout="prev, pager, next, jumper, sizes, total"
          :total="total"
          v-model:current-page="searchParams.pagenum"
          :page-sizes="[10,20,50]"
          v-model:page-size="searchParams.pagesize"
          @size-change="userFY"
          @current-change="userFY"
      />

    </div>

    <!-- 黑名单-->
    <el-dialog v-model="dialogTableVisibleblack" title="黑名单用户 (即登录失败6次以上)" width="35%">
      <el-table :data="blackUserList" height="300" width="350">
        <el-table-column property="name" label="用户名" width="250"/>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button type="danger" @click="blackUserDel(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 新建弹窗对话框 -->
    <el-dialog v-model="dialogFormVisible" title="新建用户">
      <el-form
          :model="fromData"
          :rules="rules"
          ref="userFrom"
          label-width="120px"
          class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="user">
          <el-input id="user" style="width: 80%;" v-model="fromData.user" placeholder="输入用户名"/>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="fromData.role" placeholder="角色选择">
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" id="password" style="width: 80%;" v-model="fromData.password"
                    placeholder="输入密码"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="password1">
          <el-input type="password" id="password1" style="width: 80%;" v-model="fromData.password1"
                    placeholder="输入密码"/>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input id="phone" style="width: 80%;" v-model="fromData.phone" placeholder="输入手机号"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="mailbox">
          <el-input id="mailbox" style="width: 80%;" v-model="fromData.mailbox" placeholder="输入邮箱"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div>
          <el-button type="danger" @click="cancellation">取消</el-button>
          <el-button type="warning" @click="resetDialogForm">重置</el-button>
          <el-button type="primary" @click="confirms(userFrom)">确认</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 修改密码弹窗对话框 -->
    <el-dialog v-model="dialogFormVisible2" title="密码修改">
      <el-form
          :model="fromPwd"
          :rules="rules2"
          ref="pwdFrom"
          label-width="120px"
          class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="user">
          <el-input id="user" style="width: 80%;" v-model="fromPwd.user" placeholder="输入用户名"/>
        </el-form-item>
        <el-form-item label="密码" prop="passwd">
          <el-input type="password" id="passwd" style="width: 80%;" v-model="fromPwd.passwd" placeholder="输入密码"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="passwd1">
          <el-input type="password" id="passwd1" style="width: 80%;" v-model="fromPwd.passwd1" placeholder="输入密码"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div>
          <el-button type="danger" @click="cancellationPwd">取消</el-button>
          <el-button type="warning" @click="resetDialogPwdForm">重置</el-button>
          <el-button type="primary" @click="confirms2(pwdFrom)">确认</el-button>
        </div>
      </template>
    </el-dialog>


    <!-- 编辑弹窗对话框 -->
    <el-dialog v-model="dialogFormVisible1" title="编辑用户">
      <el-form
          :model="fromData1"
          :rules="rules1"
          ref="userFrom1"
          label-width="120px"
          class="demo-ruleForm"
      >
        <el-form-item label="角色" prop="role">
          <el-select v-model="fromData1.role" placeholder="角色选择">
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div>
          <el-button type="danger" @click="cancellation1">取消</el-button>
          <el-button type="primary" @click="confirms1(userFrom1)">确认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>

</template>


<script>
import {toRefs, reactive, ref} from "vue"
import {ElMessage} from 'element-plus'
import {InfoFilled} from '@element-plus/icons-vue'
import {useRouter} from "vue-router";


import {
  createUserPost,
  showUserGet,
  updateUserPost,
  delUserDelete,
  searchUserGet,
  updateUserPwdPost, getBlackUserDataGet, delBlackUserDelete
} from "@/utils/apis"
import { ArrowRight } from '@element-plus/icons-vue';

export default {
  name: "userCreateView",
  setup() {
    const data = reactive({
      searchText: "",
      searchParams: {
        query: "",
        pagesize: 10,
        pagenum: 1,
      },
      userInfoList: [],
      blackUserList: [],
      total: 0,
      //状态控制
      dialogFormVisible: false,
      dialogFormVisible1: false,
      dialogFormVisible2: false,
      dialogTableVisibleblack: false,
      fromData: {
        user: "",
        role: "",
        password: "",
        password1: "",
        phone: "",
        mailbox: "",
      },
      fromData1: {
        user: "",
        role: "",
        phone: "",
        mailbox: "",
      },
      fromPwd: {
        user: "",
        passwd: "",
        passwd1: "",
      },
      rules: {
        user: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
        role: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
        password: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
        password1: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
        phone: [
          {
            required: true,
            pattern: /^1((34[0-8])|(8\d{2})|(([35][0-35-9]|4[579]|66|7[35678]|9[1389])\d{1}))\d{7}$/,
            message: "请填写正确的手机号",
            trigger: "blur",
          }
        ],
        mailbox: [
          {
            required: true,
            pattern: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
            message: "邮箱格式不正确",
            trigger: "blur",
          }
        ],
      },
      rules1: {
        role: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
      },
      rules2: {
        user: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
        passwd: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
        passwd1: [
          {required: true, message: "必填项", trigger: "blur"}
        ],
      },


    })

    const value = ref('')
    const options = [
      {
        value: 'admin',
        label: 'admin',
      },
      {
        value: 'ordinary',
        label: 'ordinary',
      },
      {
        value: 'view',
        label: 'view',
      },
    ]

    const router = useRouter();

    function showALLUserInfo() {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      showUserGet(data.searchParams).then(
          res => {
            data.userInfoList = res.userlist
            data.total = res.total
          }
      )
    }

    const searchUser = () => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      searchUserGet({"user": data.searchText}).then(
          res => {
            data.userInfoList = res.user_list
            data.total = res.total
            resetSsData()
          }
      )
    }

    const blackListUser = function () {
      if (localStorage.getItem('userToken') === "undefined" || localStorage.getItem('userToken') === null) {
        router.push({name: 'loginView'});
        return
      }
      data.dialogTableVisibleblack = true;
      getBlackUserDataGet().then(
          res => {
              data.blackUserList = res.user_list;
            }
      )
    }

    const blackUserDel = row => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      const {name} = row
      // 请求里必须传入对象
      delBlackUserDelete({"user": name}).then(
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
            data.dialogTableVisibleblack = false;
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


    const addUser = () => {
      data.dialogFormVisible = true
    }
    const updatePasswd = () => {
      data.dialogFormVisible2 = true
    }

    const cancellation1 = () => {
      data.dialogFormVisible1 = false
    }
    const cancellation = () => {
      resetDialogForm()
      data.dialogFormVisible = false
    }

    const cancellationPwd = () => {
      //重置表单
      resetDialogPwdForm()
      data.dialogFormVisible2 = false
    }


    const userFrom = ref()
    const userFrom1 = ref()
    const pwdFrom = ref()

    //新建用户获取弹窗表单数据
    const confirms = (formData) => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      formData.validate(
          res => {
            if (!res) {
              return
            }
            createUserPost(data.fromData).then(
                res => {
                  resetDialogForm()
                  //关闭弹窗
                  data.dialogFormVisible = false
                  //更新页面到最新数据
                  showALLUserInfo()
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

    //重置表单数据
    const resetDialogForm = () => {
      data.fromData.user = ''
      data.fromData.role = ''
      data.fromData.password = ''
      data.fromData.password1 = ''
      data.fromData.phone = ''
      data.fromData.mailbox = ''
    }

    const resetDialogPwdForm = () => {
      data.fromPwd.user = ''
      data.fromPwd.passwd = ''
      data.fromPwd.passwd1 = ''
    }

    const resetSsData = () => {
      data.searchText = ''
    }

    // 禁用选项
    //   const statusUpdate=()=>{

    //   }

    // 编辑用户数据
    const editUser = row => {
      const {user, role, phone, mailbox} = row
      data.dialogFormVisible1 = true
      data.fromData1.user = user
      data.fromData1.role = role
      data.fromData1.phone = phone
      data.fromData1.mailbox = mailbox
    }

    //编辑
    const confirms1 = (formData1) => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      formData1.validate(
          res => {
            //验证表单是否通过
            if (!res) {
              return
            }
            updateUserPost(data.fromData1).then(
                res => {
                  resetDialogForm()
                  data.dialogFormVisible1 = false
                  showALLUserInfo()
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

    // 修改密码
    const confirms2 = (fromPwd) => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      fromPwd.validate(
          res => {
            if (!res) {
              return
            }
            updateUserPwdPost(data.fromPwd).then(
                res => {
                  resetDialogPwdForm()
                  data.dialogFormVisible2 = false
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


    const deleteUser = row => {
      if (localStorage.getItem('userToken') == "undefined" || localStorage.getItem('userToken') == null) {
        router.push({name: 'loginView'});
        return
      }
      const {user} = row
      // 请求里必须传入对象
      delUserDelete({"user": user}).then(
          res => {
            showALLUserInfo()
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

    showALLUserInfo()

    const userFY = () => {
      showUserGet(data.searchParams).then(
          res => {
            data.userInfoList = res.userlist
            data.total = res.total
          }
      )
    }

    return {
      ...toRefs(data),
      searchUser,
      addUser,
      updatePasswd,
      confirms,
      confirms1,
      confirms2,
      resetSsData,
      cancellation,
      cancellation1,
      cancellationPwd,
      resetDialogForm,
      resetDialogPwdForm,
      userFrom,
      userFrom1,
      pwdFrom,
      editUser,
      deleteUser,
      value,
      options,
      InfoFilled,
      userFY,
      blackListUser,
      blackUserDel,
      ArrowRight,
    }
  }
};
</script>


<style scoped>
.input-box {
  width: 300px;
  margin-right: 15px;
}
</style>
