import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export function getAccessToken() {
  return localStorage.getItem('access_token') || localStorage.getItem('token') || ''
}

export function authHeaders(extraHeaders = {}) {
  const token = getAccessToken()

  if (!token) {
    return extraHeaders
  }

  return {
    Authorization: `Bearer ${token}`,
    ...extraHeaders,
  }
}

export function isUnauthorized(error) {
  return error?.response?.status === 401
}