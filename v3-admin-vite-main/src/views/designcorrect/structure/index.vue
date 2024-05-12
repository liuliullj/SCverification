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

const verificationResult = ref("Hello World!" + '这里是长文本内容\n，如果行数\n增多\n，滚动条\n会自动\n出现。' +
            '\n可以通过\n在这里添加更多\n的文本\n来测\n试\n滚动条的效果。' +
            '\n文本行数越多，滚动条\n越有\n可能\n出现。');
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


const verifyStructure = (row: GetStructureRequestData) => {
  if (selectedProject.value.length === 0) {
    return;
  }
  verificationResult.value = '正在生成验证结果，请稍等...'
  formData.value = JSON.parse(JSON.stringify(row))
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


//判断是否需要合并属性

const extractPid = (expression) =>{
  const match = expression.match(/^\((\d+),\s*(\d+),\s*(\w+)\)$/);
  return match ? match[2] : null;  // 返回 pid 部分
};

// 计算每个pid的行索引和计数
const pidRows = computed(() => {
  const pidMap = {};
  structureData.value.forEach((row, index) => {
    const pid = extractPid(row.expectedExpression);
    if (pid) {
      if (!pidMap.hasOwnProperty(pid)) {
        pidMap[pid] = { startIndex: index, count: 1 }; // 初始化时直接设置count为1
      } else {
        pidMap[pid].count++;  // 仅在已存在时递增
      }
    }
  });
  return pidMap;
});

const spanMethod = ({ row, column, rowIndex, columnIndex }) => {
  const pid = extractPid(row.expectedExpression);
  console.log("spanMethod called");
  console.log(`Processing row ${rowIndex}, column ${columnIndex} (${column.property}), PID: ${pid}`);

  // 合并目标列的索引可能需要调整，这里用列名称代替固定索引
  const columnsToMerge = ['demandId', 'demandName', '操作'];
  if (columnsToMerge.includes(column.property)) {
    const pidInfo = pidRows.value[pid];
    if (pidInfo && pidInfo.startIndex === rowIndex) {
      console.log(`Merging ${pidInfo.count} rows starting from row ${rowIndex} for column ${column.property}`);
      return pidInfo.count;
    } else {
      return 0;
    }
  }
  return 1;
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
          <el-table-column prop="id" label="性质Id" align="center" />
          <el-table-column prop="demandId" label="需求编号" align="center" />
          <el-table-column prop="demandName" label="需求名称" align="center" />
          <el-table-column prop="expectedExpression" label="期望性质表达式" align="center" />
          <el-table-column fixed="right" label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small" @click="verifyStructure(scope.row)">验证</el-button>
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
