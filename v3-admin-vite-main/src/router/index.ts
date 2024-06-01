import { type RouteRecordRaw, createRouter } from "vue-router"
import { history, flatMultiLevelRoutes } from "./helper"
import routeSettings from "@/config/route"

const Layouts = () => import("@/layouts/index.vue")

/**
 * 常驻路由
 * 除了 redirect/403/404/login 等隐藏页面，其他页面建议设置 Name 属性
 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: "/redirect",
    component: Layouts,
    meta: {
      hidden: true
    },
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@/views/redirect/index.vue")
      }
    ]
  },
  {
    path: "/403",
    component: () => import("@/views/error-page/403.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/404",
    component: () => import("@/views/error-page/404.vue"),
    meta: {
      hidden: true
    },
    alias: "/:pathMatch(.*)*"
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/",
    component: Layouts,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        name: "Dashboard",
        meta: {
          title: "首页",
          svgIcon: "dashboard",
          affix: true
        }
      }
    ]
  },
  // {
  //   path: "/unocss",
  //   component: Layouts,
  //   redirect: "/unocss/index",
  //   children: [
  //     {
  //       path: "index",
  //       component: () => import("@/views/unocss/index.vue"),
  //       name: "UnoCSS",
  //       meta: {
  //         title: "UnoCSS",
  //         svgIcon: "unocss"
  //       }
  //     }
  //   ]
  // },
  {
    path:"/require",
    component: Layouts,
    redirect: "/require/management",
    name: "Require",
    meta:{
      title:"智能合约需求管理",
      svgIcon:"unocss"
    },
    children:[
      {
        path:"projectmanagement",
        component: () => import("@/views/requiremanagment/projectmanagement/index.vue"),
        name:"Project",
        meta:{
          title: "项目管理",
          keepAlive: true
        }
      },
      {
        path:"demandmanagement",
        component: () => import("@/views/requiremanagment/demandmanagement/index.vue"),
        name:"Demand",
        meta:{
          title: "需求录入",
          keepAlive: true
        }
      },
      {
        path:"designmanagement",
        component: () => import("@/views/requiremanagment/designmanagement/index.vue"),
        name:"Design",
        meta:{
          title: "合约设计",
          keepAlive: true
        }
      }
    ]
  },
  // {
  //   path: "/link",
  //   meta: {
  //     title: "智能合约需求管理",
  //     svgIcon: "link"
  //   },
  //   children: [
  //     {
  //       path: "https://juejin.cn/post/7089377403717287972",
  //       component: () => {},
  //       name: "Link1",
  //       meta: {
  //         title: "中文文档"
  //       }
  //     },
  //     {
  //       path: "https://juejin.cn/column/7207659644487139387",
  //       component: () => {},
  //       name: "Link2",
  //       meta: {
  //         title: "新手教程"
  //       }
  //     }
  //   ]
  // },
  {
    path: "/model",
    component: Layouts,
    redirect: "/model",
    name: "Model",
    meta: {
      title: "可验证智能合约建模",
      elIcon: "Grid"
    },
    children: [
      {
        path: "basic-data",
        component: () => import("@/views/model/basicdata/index.vue"),
        name: "BasicData",
        meta: {
          title: "基础数据类型建模",
          keepAlive: true
        }
      },
      {
        path: "mapping",
        component: () => import("@/views/model/mapping/index.vue"),
        name: "Mapping",
        meta: {
          title: "映射类型建模",
          keepAlive: true
        }
      },
      {
        path: "interface",
        component: () => import("@/views/model/interface/index.vue"),
        name: "Interface",
        meta: {
          title: "接口类型建模",
          keepAlive: true
        }
      },
      {
        path: "condition",
        component: () => import("@/views/model/condition/index.vue"),
        name: "Condition",
        meta: {
          title: "条件类型建模",
          keepAlive: true
        }
      },
      {
        path: "agreement",
        component: () => import("@/views/model/agreement/index.vue"),
        name: "Agreement",
        meta: {
          title: "合约约定类型建模",
          keepAlive: true
        }
      },
      {
        path: "entryItem",
        component: () => import("@/views/model/entryItem/index.vue"),
        name: "EntryItem",
        meta: {
          title: "合约条目类型建模",
          keepAlive: true
        }
      },
      {
        path: "smartContract",
        component: () => import("@/views/model/smartContract/index.vue"),
        name: "SmartContract",
        meta: {
          title: "智能合约类型建模",
          keepAlive: true
        }
      }
    ]
  },
  {
    path: "/designcorrect",
    component: Layouts,
    redirect: "/designcorrect",
    name: "Menu",
    meta: {
      title: "设计正确性验证",
      svgIcon: "menu"
    },
    children: [
      {
        path: "structure",
        component: () => import("@/views/designcorrect/structure/index.vue"),
        name: "Structure",
        meta: {
          title: "结构正确性验证",
          keepAlive: true
        }
      },
      {
        path: "call",
        component: () => import("@/views/designcorrect/call/index.vue"),
        name: "Call",
        meta: {
          title: "调用正确性验证",
          keepAlive: true
        }
      }
    ]
  },
  {
    path: "/security",
    component: Layouts,
    redirect: "/security",
    name: "Security",
    meta: {
      title: "合约安全性验证",
      elIcon: "Menu",
      alwaysShow: true
    },
    children: [
      {
        path: "security",
        component: () => import("@/views/security/index.vue"),
        name: "Security",
        meta: {
          title: "安全性验证",
          keepAlive: true
        }
      }
    ]
  }
]

/**
 * 动态路由
 * 用来放置有权限 (Roles 属性) 的路由
 * 必须带有 Name 属性
 */
export const dynamicRoutes: RouteRecordRaw[] = [
  {
    path: "/permission",
    component: Layouts,
    redirect: "/permission/page",
    name: "Permission",
    meta: {
      title: "合约元语言自动生成",
      svgIcon: "lock",
      roles: ["admin", "editor"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "page",
        component: () => import("@/views/metagenerate/index.vue"),
        name: "PagePermission",
        meta: {
          title: "元语言生成",
        }
      },
      // {
      //   path: "directive",
      //   component: () => import("@/views/permission/directive.vue"),
      //   name: "DirectivePermission",
      //   meta: {
      //     title: "指令权限" // 如果未设置角色，则表示：该页面不需要权限，但会继承根路由的角色
      //   }
      // }
    ]
  },
  {
    path: "/:pathMatch(.*)*", // Must put the 'ErrorPage' route at the end, 必须将 'ErrorPage' 路由放在最后
    redirect: "/404",
    name: "ErrorPage",
    meta: {
      hidden: true
    }
  }
]

const router = createRouter({
  history,
  routes: routeSettings.thirdLevelRouteCache ? flatMultiLevelRoutes(constantRoutes) : constantRoutes
})

/** 重置路由 */
export function resetRouter() {
  // 注意：所有动态路由路由必须带有 Name 属性，否则可能会不能完全重置干净
  try {
    router.getRoutes().forEach((route) => {
      const { name, meta } = route
      if (name && meta.roles?.length) {
        router.hasRoute(name) && router.removeRoute(name)
      }
    })
  } catch {
    // 强制刷新浏览器也行，只是交互体验不是很好
    window.location.reload()
  }
}

export default router

