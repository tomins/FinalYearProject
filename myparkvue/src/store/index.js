import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    locToken: ''
  },
  mutations: {
    initializeStore(state){
      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem("token")
        state.isAuthenticated = true
      
    } else {
        state.token = ''
        state.isAuthenticated = false
    }
    if (localStorage.getItem("locToken")){
      state.locToken = localStorage.getItem("locToken") 
    } else {
      state.locToken = ''
  } 
  },
    setToken(state, token){
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state){
      state.token = ''
      state.isAuthenticated = false
    },
    setLocToken(state, locToken){
      state.locToken = locToken
    },
    removeLocToken(state){
      state.locToken = ''
    }
  },
  actions: {
  },
  modules: {
  }
})
