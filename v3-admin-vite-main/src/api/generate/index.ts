import { request } from "@/utils/service"
import type * as Table from "./types/table"
import axios from 'axios'
import qs from 'qs'
import { Tracing } from "trace_events";

const BASE_URL = 'http://127.0.0.1:5000';

export function generateApi(projectname:string){
  var param = {
    'projectname':projectname
  }
  console.log("generateApi     "+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/generateApi`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}
