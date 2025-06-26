import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/',
  withCredentials: true,
  withXSRFToken: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
})

export default API
