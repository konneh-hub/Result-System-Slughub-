import apiClient from '../api/axios.js'
import { API_ENDPOINTS } from '../api/endpoints.js'

export const listNotifications = (params = {}) => apiClient.get(API_ENDPOINTS.notifications, { params })
export const markNotificationRead = (id, payload = {}) => apiClient.post(API_ENDPOINTS.notificationMarkRead(id), payload)
