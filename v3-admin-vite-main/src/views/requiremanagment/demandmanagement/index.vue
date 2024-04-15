<script lang="ts" setup>
import { reactive, ref, watch, onMounted} from "vue"
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
      <div class="instruction-wrapper" style="margin-bottom: 10px;">
      <el-card class="box-card">
        <div slot="header" class="clearfix custom-header">
          <span>请按照如下智能合约组成结构需求模版录入需求：</span>
        </div>
        <pre class="custom-code"><code>
SmartContract::=ContractItem<sup>+</sup>
ContractItem::=(Condition<sup>*</sup>,Agreement)<sup>+</sup>
Agreement::=Workflow<sup>+</sup> | if Condition then Workflow else Workflow
Workflow::=f<sub>1</sub>([RelevantRole|RelevantGood|RelevantAssets]<sup>+</sup>)
           f<sub>2</sub>([RelevantRole|RelevantGood|RelevantAssets]<sup>+</sup>)...
           f<sub>k</sub>([RelevantRole|RelevantGood|RelevantAssets]<sup>+</sup>)...
RelevantRole::=provider|consumer|trade|...
RelevantGood::=amount|count|...
RelevantAssets::=CER|...
Condition::=[RelevantRole|RelevantGood|RelevantAssets]<sup>+</sup> conditionoperator values
conditionoperator::=&gt;|&lt;|&ge;|&le;|=|&ne;
ContractBasedTransaction::=Transaction<sup>+</sup>
Transaction::=(BlockChain<sub>i</sub>.SmartContract<sub>m</sub>.f<sub>r</sub>),...(BlockChain<sub>j</sub>.SmartContract<sub>n</sub>.f<sub>s</sub>)
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
          <el-select v-model="formData.category" placeholder="请选择">
            <el-option label="附加信息" value="附加信息"></el-option>
            <el-option label="方法" value="方法"></el-option>
            <el-option label="执行流程" value="执行流程"></el-option>
            <el-option label="条件语句" value="条件语句"></el-option>
            <el-option label="约定" value="约定"></el-option>
            <el-option label="合约" value="合约"></el-option>
            <el-option label="事物/交易" value="事物/交易"></el-option>
          </el-select>
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
