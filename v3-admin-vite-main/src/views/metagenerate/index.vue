<script lang="ts" setup>
import { reactive, ref, watch, onMounted, computed} from "vue"
import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi,getProjectNameApi,getDemandDataApi, CreatDemandDateApi, updateDemandDateApi, deleteDemandDataApi} from "@/api/table"
import { type CreateOrUpdateTableRequestData, type GetTableData ,type CreateOrUpdateDemandRequestData} from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "ElementPlus"
})

const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

//region 增
const DEFAULT_FORM_DATA: CreateOrUpdateDemandRequestData = {
  id: undefined,
  demandname: "",
  category: "",
  demanddescription: "",
  parentD: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateDemandRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateDemandRequestData> = {
  demandname: [{ required: true, trigger: "blur", message: "请输入需求名" }],
  category: [{ required: true, trigger: "blur", message: "请输入需求类别" }],
  demanddescription: [{ required: true, trigger: "blur", message: "请输入需求描述" }],
  parentD: [{ required: true, trigger: "blur", message: "请输入父需求Id" }]
}

const handleCreateOrUpdateDemand = () => {
  formRef.value?.validate((valid: boolean, fields) => {
    if (!valid) return console.error("表单校验不通过", fields)
    if (selectedProject.value.length === 0) {
      ElMessage.success("请先选择一个项目")
      return;
    }
    loading.value = true
    const api = formData.value.id === undefined ? CreatDemandDateApi : updateDemandDateApi
    api(formData.value,selectedProject.value)
      .then(() => {
        ElMessage.success("操作成功")
        dialogVisible.value = false
        fetchProjectData()
      })
      .finally(() => {
        loading.value = false
      })
  })
}
const resetForm = () => {
  formRef.value?.clearValidate()
  formData.value = JSON.parse(JSON.stringify(DEFAULT_FORM_DATA))
}
//endregion

//region 删
const handleDelete = (row) => {
  ElMessageBox.confirm(`正在删除需求：${row.demandname}，确认删除？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    deleteDemandDataApi(row.id,selectedProject.value).then(() => {
      ElMessage.success("删除成功");
      fetchProjectData();
    }).catch((error) => {
      // 这里处理API调用失败的情况
      ElMessage.error("删除失败：" + error.message);
    });
  }).catch(() => {
    // 这里处理取消操作的情况
    console.log("取消删除");
  });
};
//#endregion

//region 改
const handleUpdate = (row: GetTableData) => {
  dialogVisible.value = true
  formData.value = JSON.parse(JSON.stringify(row))
}
//endregion


/** 获取项目名称列表*/
onMounted(() => {
  fetchProjectNames();
});
const projectNames = ref([])
const fetchProjectNames = () =>{
  getProjectNameApi({})
  .then(({ data }) => {
    console.log(data)
    projectNames.value = data
    })
}

// 获取项目对应的需求列表
const demandData = ref([])
const selectedProject = ref([]);
const fetchProjectData = () =>{
  if (selectedProject.value.length === 0) {
    return;
  }
  getDemandDataApi({
    projectname: selectedProject.value,
    currentPage: paginationData.currentPage,
    size: paginationData.size
  })
  .then((data) => {
    console.log(data)
    console.log("here")
    var demandlist = []
    for (let index = 0; index < data.list.length; index++){
      const element = data.list[index];
      var tableRow = {
        "id":element['id'],
        "demandname":element['demandname'],
        "category":element['category'],
        "demanddescription":element['demanddescription'],
        "parentD":element['parentD'],
        "creatTime":element['creatTime']
      }
      demandlist.push(tableRow)
    }
    paginationData.total = data.total
    demandData.value = demandlist
    })
}

/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], fetchProjectData, { immediate: true })

const categoryString = computed({
  get: () => formData.value.category,
  set: (value) => {
    if (Array.isArray(value)) {
      // 如果 value 是数组，取最后一个元素作为 category 值
      formData.value.category = value[value.length - 1] || "";
    } else {
      formData.value.category = value;
    }
  }
});

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="fetchProjectData" @click="fetchProjectNames">
        <el-option
          v-for="name in projectNames"
          :key="name"
          :label="name"
          :value="name">
        </el-option>
      </el-select>
    </el-card>
    <el-card v-loading="loading" shadow="never">
      <div style="margin-bottom: 10px;">
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">生成元语言</el-button>
          <!-- <el-button type="danger" :icon="Delete">批量删除</el-button> -->
      </div>
      <div class="instruction-wrapper" style="margin-bottom: 10px;">
      <el-card class="box-card">
        <div slot="header" class="clearfix custom-header">
          <span style="display: inline-block; margin-bottom: 10px;">元语言生成中...</span><br>
          <span>Traceability角色信息管理合约元语言如下:</span>
        </div>
        <pre class="custom-code"><code>
UserTypes:Admin | Producer | Logistics | Agency | Customer
UserStatus: Legal | Frozen | Invalid
hostAddr:address
userIndex:uint
registerInfo:mapping(address→string)
Condition:importCheck(string)==true
addition Users{
userAddress:address
userName:string
licenseNo:string
power:UserTypes
statu:UserStatus
isAlreadyRegister:bool}
Terms no1: Admin can companyInfoImport(companyName, licenseNo, companyType)
	when !importCheck[licenseNo]
	where WriteCompanyInfo
Terms no2: Users can companyInfoImport(userName, licenseNo, power,userAddress)
	when power!=Customer and UserInfo[licenseNo][power]=power
	where userRegistrationWrite
Terms no3: Customer can customerInfoImport(userName, licenseNo, power,userAddress)
	where CustomerRegistration





        </code></pre>
      </el-card>
      </div>

      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">新增需求</el-button>
          <el-button type="danger" :icon="Delete">批量删除</el-button>
        </div>
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="fetchProjectData" />
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="demandData">
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column prop="id" label="需求Id" align="center" />
          <el-table-column prop="demandname" label="需求名称" align="center" />
          <el-table-column prop="category" label="需求类别" align="center" />
          <el-table-column prop="demanddescription" label="需求描述" align="center" />
          <el-table-column prop="parentD" label="父需求" align="center" />
          <el-table-column prop="creatTime" label="创建时间" align="center" />
          <el-table-column fixed="right" label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small" @click="handleUpdate(scope.row)">修改</el-button>
              <el-button type="danger" text bg size="small" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pager-wrapper">
        <el-pagination
          background
          :layout="paginationData.layout"
          :page-sizes="paginationData.pageSizes"
          :total="paginationData.total"
          :page-size="paginationData.pageSize"
          :currentPage="paginationData.currentPage"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    <!-- 新增/修改 -->
    <el-dialog
      v-model="dialogVisible"
      :title="formData.id === undefined ? '新增需求' : '修改需求'"
      @closed="resetForm"
      width="30%"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px" label-position="left">
        <el-form-item prop="demandname" label="需求名">
          <el-input v-model="formData.demandname" placeholder="请输入" />
        </el-form-item>
        <el-form-item prop="category" label="需求类别">
          <el-cascader
            v-model="categoryString"
            :options="[
              { value: '功能', label: '功能' },
              { value: '执行流程', label: '执行流程' },
              { value: '业务', label: '业务' },
              { value: '智能合约', label: '智能合约' }
            ]"
            placeholder="请选择"
            clearable
            style="width: 100%;"
          ></el-cascader>
        </el-form-item>
        <el-form-item prop="demanddescription" label="需求描述">
          <el-input v-model="formData.demanddescription" placeholder="请输入" />
        </el-form-item>
        <el-form-item prop="parentD" label="父需求Id">
          <el-input v-model="formData.parentD" placeholder="请输入" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrUpdateDemand" :loading="loading">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style lang="scss" scoped>
.search-wrapper {
  align-items: center;
  margin-bottom: 20px;
  height: 75px;
  :deep(.el-card__body) {
    padding-bottom: 2px;
  }
}

.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.table-wrapper {
  margin-bottom: 20px;
}

.pager-wrapper {
  display: flex;
  justify-content: flex-end;
}

.custom-header {
  margin-top: -10px; /* 根据需要调整这个值 */
}

/* 调整代码段行间距 */
.custom-code {
  line-height: 1.5; /* 增加行高来扩大间距，根据需要调整这个值 */
  margin-top: -10px;
  margin-bottom: -10px;
}

</style>
