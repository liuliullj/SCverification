<script lang="ts" setup>
import { reactive, ref, watch, onMounted} from "vue"
import { getProjectNameApi,getSmartContractDataApi, CreatSmartContractDataApi, updateSmartContractDataApi, deleteSmartContractDataApi} from "@/api/smartContract/index"
import { type GetSmartContractRequestData ,type CreateOrUpdateSmartContractRequestData} from "@/api/smartContract/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "SmartContract"
})

const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

//region 增
const DEFAULT_FORM_DATA: CreateOrUpdateSmartContractRequestData = {
  id: undefined,
  smartContractName: "",
  smartContractEntryItems: "",
  demandId: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateSmartContractRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateSmartContractRequestData> = {
  smartContractName: [{ required: true, trigger: "blur", message: "请输入智能合约类型名称" }],
  smartContractEntryItems: [{ required: true, trigger: "blur", message: "请输入智能合约类型组成条目" }],
  demandId: [{ required: true, trigger: "blur", message: "请输入对应需求id" }]
}

const handleCreateOrUpdateSmartContract = () => {
  formRef.value?.validate((valid: boolean, fields) => {
    if (!valid) return console.error("表单校验不通过", fields)
    loading.value = true
    const api = formData.value.id === undefined ? CreatSmartContractDataApi : updateSmartContractDataApi
    api(formData.value,selectedProject.value)
      .then(() => {
        ElMessage.success("操作成功")
        dialogVisible.value = false
        fetchSmartContract()
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
  ElMessageBox.confirm(`正在删除智能合约类型：${row.smartContractName}，确认删除？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    deleteSmartContractDataApi(row.id,selectedProject.value).then(() => {
      ElMessage.success("删除成功");
      fetchSmartContract();
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
const handleUpdate = (row: GetSmartContractRequestData) => {
  dialogVisible.value = true
  formData.value = JSON.parse(JSON.stringify(row))
}




/** 获取项目名称列表*/
onMounted(async () => {
  await fetchProjectNames();
});
const projectNames = ref([])
const fetchProjectNames = () =>{
  getProjectNameApi({})
  .then(({ data }) => {
    console.log(data)
    projectNames.value = data
    })
}

// 获取项目对应的智能合约类型列表
const smartContractData = ref([])
const selectedProject = ref([]);
const fetchSmartContract = () =>{
  if (selectedProject.value.length === 0) {
    return;
  }
  getSmartContractDataApi({
    projectname: selectedProject.value,
    currentPage: paginationData.currentPage,
    size: paginationData.size
  })
  .then((data) => {
    console.log(data)
    console.log("here")
    var smartContractlist = []
    for (let index = 0; index < data.list.length; index++){
      const element = data.list[index];
      var tableRow = {
        "id":element['id'],
        "smartContractName":element['smartContractName'],
        "smartContractEntryItems":element['smartContractEntryItems'],
        "demandId":element['demandId'],
        "creatTime":element['creatTime']
      }
      smartContractlist.push(tableRow)
    }
    paginationData.total = data.total
    smartContractData.value = smartContractlist
    })
}

/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], fetchSmartContract, { immediate: true })

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="fetchSmartContract">
        <el-option
          v-for="name in projectNames"
          :key="name"
          :label="name"
          :value="name">
        </el-option>
      </el-select>
    </el-card>
    <el-card v-loading="loading" shadow="never">
      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">新增智能合约类型</el-button>
          <el-button type="danger" :icon="Delete">批量删除</el-button>
        </div>
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="fetchSmartContract" />
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="smartContractData">
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column prop="id" label="智能合约类型Id" align="center" />
          <el-table-column prop="smartContractName" label="智能合约类型名称" align="center" />
          <el-table-column prop="smartContractEntryItems" label="智能合约类型组成条目" align="center" />
          <el-table-column prop="demandId" label="对应需求id" align="center" />
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
      :title="formData.id === undefined ? '新增智能合约类型' : '修改智能合约类型'"
      @closed="resetForm"
      width="30%"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="180px" label-position="left">
        <el-form-item prop="smartContractName" label="智能合约类型名称">
          <el-input v-model="formData.smartContractName" placeholder="请输入" />
        </el-form-item>
        
        <el-form-item prop="smartContractEntryItems" label="智能合约类型组成条目">
          <el-input v-model="formData.smartContractEntryItems" placeholder="请输入" />
        </el-form-item>

        <el-form-item prop="demandId" label="对应需求id">
          <el-input v-model="formData.demandId" placeholder="请输入" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrUpdateSmartContract" :loading="loading">确认</el-button>
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
