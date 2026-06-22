import apiClient from '../api/axios.js'
import { API_ENDPOINTS } from '../api/endpoints.js'

export const createApprovalRequest = (payload) => apiClient.post(API_ENDPOINTS.approvalRequests, payload)
export const listApprovalRequests = (params = {}) => apiClient.get(API_ENDPOINTS.approvalRequests, { params })
export const createApprovalAction = (payload) => apiClient.post(API_ENDPOINTS.approvalActions, payload)
export const listApprovalActions = (params = {}) => apiClient.get(API_ENDPOINTS.approvalActions, { params })
