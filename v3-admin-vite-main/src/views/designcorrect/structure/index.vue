<script lang="ts" setup>
import { reactive, ref, watch, onMounted, computed} from "vue"
import { getProjectNameApi, getStructureDataApi, verifyStructureDataApi, verifyAllDataApi} from "@/api/structure/index"
import { type GetStructureRequestData, type VerifyStructureRequestData} from "@/api/structure/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { usePagination } from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "Structure"
})

const verificationResult = ref("请点击验证按钮进行验证" );
const loading = ref<boolean>(false)
const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()

const {
  paginationData: structurePaginationData,
  handleCurrentChange: structurehandleCurrentChange,
  handleSizeChange: structurehandleSizeChange
} = usePagination();

//region 增
const DEFAULT_FORM_DATA: VerifyStructureRequestData = {
  id: "",
  demandId: "",
  demandName: "",
  expectedExpression: ""
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<VerifyStructureRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))


//获取多行待验证数据
const getAllRowsForDemandId = (demandId) => {
  return structureData.value.filter(row => row.demandId === demandId);
};

const verifyStructure = (demandId) => {
  if (selectedProject.value.length === 0) {
    return;
  }
  verificationResult.value = '正在生成验证结果，请稍等...'
  let rowsToVerify = getAllRowsForDemandId(demandId)
  formData.value = JSON.parse(JSON.stringify(rowsToVerify))
  console.log("rows:")
  console.log(formData.value)
  const api = verifyStructureDataApi
  api(formData.value,selectedProject.value)
    .then((data) => {
      console.log('###### verifyStructure ', data)
      verificationResult.value = data['result'];
    })
    .finally(() => {
      loading.value = false
    })
}
// const verifyStructure = (row: GetStructureRequestData) => {
//   if (selectedProject.value.length === 0) {
//     return;
//   }
//   verificationResult.value = '正在生成验证结果，请稍等...'
//   formData.value = JSON.parse(JSON.stringify(row))
//   const api = verifyStructureDataApi
//   api(formData.value,selectedProject.value)
//     .then((data) => {
//       console.log('###### verifyStructure ', data)
//       verificationResult.value = data['result'];
//     })
//     .finally(() => {
//       loading.value = false
//     })
// }




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

// 获取项目对应的需求列表 仅显示执行流程和方法
const structureData = ref([])
const selectedProject = ref([]);
const fetchStructureData = async () => {
  try {
    if (selectedProject.value.length === 0) {
      return;
    }
  const data = await getStructureDataApi({
      projectname: selectedProject.value,
      currentPage: structurePaginationData.currentPage,
      size: structurePaginationData.size
  });
  console.log(data);
  var structurelist = [];
  for (let index = 0; index < data.list.length; index++) {
    const element = data.list[index];
    var tableRow = {
        "id":element['id'],
        "demandId":element['demandId'],
        "demandName":element['demandName'],
        "expectedExpression":element['expectedExpression']
    };
    structurelist.push(tableRow);
  }
  structurePaginationData.total = data.total;
  structureData.value = structurelist;
  } catch (error) {
    console.error('操作失败', error);
  }
};

const verifyAll = () => {
  console.log('verifyAll call')
  if (selectedProject.value.length === 0) {
    return;
  }
  verificationResult.value = '正在生成验证结果，请稍等...'
  console.log('期望性质', JSON.stringify(structureData.value))
  const api = verifyAllDataApi
  api(JSON.stringify(structureData.value), selectedProject.value)
    .then((data) => {
      console.log('###### verifyAll ', data)
      verificationResult.value = data['result'];
    })
    .finally(() => {
      loading.value = false
    })
}


/** 监听分页参数的变化 */
watch([() => structurePaginationData.currentPage, () => structurePaginationData.pageSize], fetchStructureData, { immediate: false })

const spanMethod = ({ row, column, rowIndex, columnIndex }) => {
  // 合并需求编号和需求名称列
  if (column.property === 'demandId' || column.property === 'demandName') {
    if (rowIndex > 0 && structureData.value[rowIndex].demandId === structureData.value[rowIndex - 1].demandId) {
      return [0, 0]; // 当前行与上一行的需求编号相同，则这行不显示
    } else {
      // 查找相同需求编号的行数来合并
      let rowCount = 1;
      for (let i = rowIndex + 1; i < structureData.value.length; i++) {
        if (structureData.value[i].demandId === row.demandId) {
          rowCount++;
        } else {
          break;
        }
      }
      return [rowCount, 1]; // 合并行数
    }
  }
  // 操作列处理，让操作按钮在合并的单元格内居中显示
  if (column.label === '操作') {
    if (rowIndex > 0 && structureData.value[rowIndex].demandId === structureData.value[rowIndex - 1].demandId) {
      return [0, 0]; // 不显示当前行的按钮，因为会在合并中显示
    } else {
      // 查找相同需求编号的行数来合并
      let rowCount = 1;
      for (let i = rowIndex + 1; i < structureData.value.length; i++) {
        if (structureData.value[i].demandId === row.demandId) {
          rowCount++;
        } else {
          break;
        }
      }
      return [rowCount, 1]; // 在这些行中合并按钮
    }
  }
  // 对于其他列，如性质Id和期望性质表达式，返回正常显示
  return [1, 1];
};

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <label for="project-select">请选择一个项目：</label>
      <el-select v-model="selectedProject" placeholder="请选择一个项目" size=“large” style="width: 240px" @change="fetchStructureData" @click="fetchProjectNames">
        <el-option
          v-for="name in projectNames"
          :key="name"
          :label="name"
          :value="name">
        </el-option>
      </el-select>
    </el-card>
    <el-card v-loading="loading" shadow="never">
      <div class="header-with-icon">
        <el-icon class="header-icon"><document /></el-icon>
        <span>期望性质</span>
      </div>
      <div class="table-wrapper">
        <el-table :data="structureData" :span-method="spanMethod">
          <el-table-column type="selection" width="50" align="center" />
          <el-table-column prop="demandId" label="需求编号" align="center" />
          <el-table-column prop="demandName" label="需求名称" align="center" />
          <el-table-column prop="id" label="性质Id" align="center" />
          <el-table-column prop="expectedExpression" label="期望性质表达式" align="center" />
          <el-table-column fixed="right" label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small" @click="verifyStructure(scope.row.demandId)">验证</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pager-wrapper">
        <el-pagination
          background
          :layout="structurePaginationData.layout"
          :page-sizes="structurePaginationData.pageSizes"
          :total="structurePaginationData.total"
          :page-size="structurePaginationData.pageSize"
          :currentPage="structurePaginationData.currentPage"
          @size-change="structurehandleSizeChange"
          @current-change="structurehandleCurrentChange"
        />
      </div>
      <div class="header-with-icon">
        <el-icon class="header-icon"><edit /></el-icon>
        <span>验证结果</span>
      </div>
      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="verifyAll()">验证全部需求</el-button>
        </div>
      </div>
      <div class="app-container">
        <!-- <el-card header="验证结果">
          <div class="text-display">
            {{ verificationResult }}
          </div>
        </el-card> -->
        <el-card class="box-card" header="验证结果">
          <div slot="header" class="clearfix custom-header scoller-display">
            <span>{{ verificationResult }}</span>
          </div>
      </el-card>
      </div>
    </el-card>
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

.header-with-icon {
  display: flex;
  align-items: center; /* 保证文本和图标垂直居中 */
  margin-bottom: 20px; /* 调整下边距 */

}

.header-icon {
  margin-right: 8px; /* 在图标和文本之间添加一些间隔 */
}

.header-with-icon span {
  font-size: 18px; /* 增加文本的字体大小 */
}

.text-display {
  max-height: 300px; /* 最大高度，超过这个高度会显示滚动条 */
  overflow-y: auto; /* 垂直方向上溢出内容时显示滚动条 */
  padding: 10px;
  border: 1px solid #ccc; /* 边框样式 */
  margin: 10px 0;
  background-color: #f9f9f9; /* 背景色 */
  white-space: pre-wrap; /* 保留空白符，允许自动和正常的文本换行 */
}

.scoller-display {
  max-height: 300px; /* 最大高度，超过这个高度会显示滚动条 */
  overflow-y: auto; /* 垂直方向上溢出内容时显示滚动条 */
  padding: 10px;
  border: 1px solid #ccc; /* 边框样式 */
  margin: 10px 0;
  white-space: pre-wrap; /* 保留空白符，允许自动和正常的文本换行 */
}
</style>
