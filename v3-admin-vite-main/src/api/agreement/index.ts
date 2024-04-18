import { request } from "@/utils/service"
import type * as Table from "./types/table"
import axios from 'axios'
import qs from 'qs'
import { Tracing } from "trace_events";

const BASE_URL = 'http://127.0.0.1:5000';

export function getProjectNameApi(){
  console.log("getnames")
  return axios.get(`${BASE_URL}/myapi/getProjectName`)
}


export function getAgreementDataApi(paras: Table.GetAgreementRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getAgreement`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatAgreementDataApi(data:Table.CreateOrUpdateAgreementRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'agreementName':data.agreementName,
    'agreementInterfaces':data.agreementInterfaces,
    'demandId':data.demandId
  }
  console.log("CreatAgreementDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createAgreement`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateAgreementDataApi(data:Table.CreateOrUpdateAgreementRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'agreementName':data.agreementName,
    'agreementInterfaces':data.agreementInterfaces,
    'demandId':data.demandId
  }
  console.log(param)
  // console.log("CreatAgreementDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateAgreement, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateAgreement`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteAgreementDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteAgreement`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
