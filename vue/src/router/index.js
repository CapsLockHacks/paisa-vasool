import Vue from 'vue'
import VueRouter from 'vue-router'
import Splits from '../views/Splits.vue'
import CreateSplit from '../views/CreateSplit.vue'
import Contacts from '../views/Contacts.vue'
import CreateContact from '../views/CreateContact.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'splits',
    component: Splits,
    meta: { title: 'All splits' }
  },
  {
    path: '/create',
    name: 'createsplit',
    component: CreateSplit,
    meta: { title: 'Create split' }
  },
  {
    path: '/contacts',
    name: 'contacts',
    component: Contacts,
    meta: { title: 'Contacts' }
  },
  {
    path: '/create-contact',
    name: 'createcontact',
    component: CreateContact,
    meta: { title: 'Add contact' }
  }
]

const router = new VueRouter({
  routes
})

export default router
