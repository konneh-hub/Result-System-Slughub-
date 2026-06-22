import apiClient, { setAuthToken } from '../api/axios.js'
import { API_ENDPOINTS } from '../api/endpoints.js'

export const login = async (payload) => {
  const response = await apiClient.post(API_ENDPOINTS.login, payload)
  if (response.data?.access) {
    setAuthToken(response.data.access)
  }
  return response
}

export const refreshToken = (payload) => apiClient.post(API_ENDPOINTS.refreshToken, payload)
export const me = () => apiClient.get(API_ENDPOINTS.me)

