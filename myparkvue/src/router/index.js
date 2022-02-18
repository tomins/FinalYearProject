import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAccount from '../views/MyAccount'
import store from '../store'
import LocationSearch from '../views/LocationSearch'
import ParkingDetail from '../views/ParkingDetail.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/LocationSearch',
    name: 'LocationSearch',
    component: LocationSearch
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta:{
      requireLogin: true
    }
  },
  {
    path: '/:name',
    name: 'ParkingDetail',
    component: ParkingDetail
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to, from, next)=>{
  if(to.matched.some(record=> record.meta.requiredLogin)&& !store.state.isAuthenticated){
    next({name: 'LogIn', query:{to: to.path}});
  }else{
    next()
  }
})

export default router
